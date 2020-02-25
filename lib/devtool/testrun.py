# Development tool - run test command plugin
#
#
"""Devtool plugin containing the run-test subcommands"""

import logging
import os
import shutil
import subprocess
import tempfile

import bb.utils
import argparse_oe
import oe.types

from devtool import exec_fakeroot, setup_tinfoil, check_workspace_recipe, DevtoolError

logger = logging.getLogger('devtool')

class RemoteShell():
    def __init__(self, ssh_sshexec, scp_sshexec, ssh_port, extraoptions, target):
        self.ssh_sshexec = ssh_sshexec
        self.scp_sshexec = scp_sshexec
        self.ssh_port = ssh_port
        self.extraoptions = extraoptions
        self.target = target
        pass

    def exec(self, cmd):
        testfindproc = subprocess.Popen("%s %s %s %s -t %s" % (self.ssh_sshexec, self.ssh_port, self.extraoptions, self.target, cmd),
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = testfindproc.communicate()
        exitcode = testfindproc.returncode
        return exitcode, out, err

    def get_file(self, src, target):
        return subprocess.call("scp %s %s %s %s:%s %s" % (self.scp_sshexec, self.ssh_port, self.extraoptions, self.target, src, target), shell=True)


def _merge_testsuites(base_suit, apnd_suit):
    ATTRIB_NAMES = ['tests', 'failures', 'disabled', 'errors']
    for attrib_name in ATTRIB_NAMES:
        base_suit.set(attrib_name, str(int(base_suit.attrib[attrib_name]) + int(apnd_suit.attrib[attrib_name])))


def run_target_test(args, config, basepath, workspace):
    print("target test begin")
    extraoptions = ''
    if args.no_host_check:
        extraoptions += '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
    if not args.show_status:
        extraoptions += '-q'

    scp_sshexec = ''
    ssh_sshexec = 'ssh'
    if args.ssh_exec:
        scp_sshexec = "-S %s" % args.ssh_exec
        ssh_sshexec = args.ssh_exec
    scp_port = ''
    ssh_port = ''
    if args.port:
        scp_port = "-P %s" % args.port
        ssh_port = "-P %s" % args.port

    if args.key:
        extraoptions += ' -i %s' % args.key

    remote_shell = RemoteShell(ssh_sshexec, scp_sshexec, ssh_port, extraoptions, args.target)

    # get executable list from /opt/tests
    exitcode, out, err = remote_shell.exec('find /opt/tests -executable -type f')

    if exitcode != 0:
        print(err)
        return

    testlist = out.split()

    reportfiles = []
    # execute tests
    for test in testlist:
        executablename = test.decode('utf-8')
        reportfilename = executablename + ".xml"
        exitcode, out, err = remote_shell.exec('%s --gtest_output=xml:%s' % (executablename, reportfilename))
        # print(out)
        reportfiles.append(reportfilename)

    # get reportfiles
    tmpdir = tempfile.mkdtemp(prefix='run-target-test')
    try:
        from xml.dom import minidom

        impl = minidom.getDOMImplementation()
        report = impl.createDocument(None, None, None)
        merged_testsuites = report.createElement("testsuites")
        report.appendChild(merged_testsuites)
        
        attr_disabled = 0
        attr_errors = 0
        attr_failures = 0
        attr_tests = 0
        # attr_time = 0

        for reportfile in reportfiles:
            # copy remote reportfile to local
            localreportfile = os.path.join(tmpdir, os.path.basename(reportfile))
            exitcode = remote_shell.get_file(reportfile, localreportfile)
            if exitcode == 0:
                # parse report
                report_current = minidom.parse(localreportfile)
                # merge every test suit to result.xml
                current_testsuitelist = report_current.getElementsByTagName("testsuite")
                for current_testsuit in current_testsuitelist:
                    merged_testsuites.appendChild(current_testsuit)
                    attr_disabled += int(current_testsuit.getAttribute("disabled"))
                    attr_errors += int(current_testsuit.getAttribute("errors"))
                    attr_failures += int(current_testsuit.getAttribute("failures"))
                    attr_tests += int(current_testsuit.getAttribute("tests"))
                    # attr_time += float(current_testsuit.getAttribute("time"))

                merged_testsuites.setAttribute("disabled", str(attr_disabled))
                merged_testsuites.setAttribute("errors", str(attr_errors))
                merged_testsuites.setAttribute("failures", str(attr_failures))
                merged_testsuites.setAttribute("tests", str(attr_tests))
                # merged_testsuites.setAttribute("time", str(attr_time))
        with open("report.xml", "w") as f:
            report.writexml(f)
        
    finally:
        #shutil.rmtree(tmpdir)
        print(tmpdir)

    print("target test end")

def register_commands(subparsers, context):
    parser_build = subparsers.add_parser('run-target-test', 
                                        help='Run test code in target(/opt/tests)',
                                        description='Run test binaries which are located at /opt/tests',
                                        group='target-test')
    parser_build.add_argument('target', help='Live target machine running an ssh server: user@hostname')
    parser_build.add_argument('-c', '--no-host-check', help='Disable ssh host key checking', action='store_true')
    parser_build.add_argument('-s', '--show-status', help='Show progress/status output', action='store_true')
    parser_build.add_argument('-e', '--ssh-exec', help='Executable to use in place of ssh')
    parser_build.add_argument('-P', '--port', help='Specify port to use for connection to the target')
    parser_build.add_argument('-I', '--key', help='Specify ssh private key for connection to the target')
    parser_build.set_defaults(func=run_target_test)
