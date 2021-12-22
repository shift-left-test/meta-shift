#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import getpass
import os
import pytest
import re
import subprocess
import shutil
import time


class Output(object):
    """The output holder class

    This class provides variout output comparison helper functions.
    """

    def __init__(self, output, kwargs={}):
        """ Default constructor

        Args:
          output (str): an output string
        """
        self.output = output.strip()
        self.kwargs = kwargs

    def empty(self):
        """Assert that the output is empty

        Returns:
          True if the output is empty, False otherwise
        """
        return not self.output

    def contains(self, keyword):
        """Assert that the output contains the given keyword

        Args:
          keyword (str): keyword to examine

        Returns:
          True if the output contains the keyword, False otherwise
        """
        return keyword.format(**self.kwargs) in self.output

    def containsAll(self, *keywords):
        """Assert that the output contains all the given keywords

        Args:
          keywords (str): keywords to examine

        Returns:
          True if the output contains all the keywords, False otherwise
        """
        for keyword in keywords:
            if not self.contains(keyword):
                return False
        return True

    def containsAny(self, *keywords):
        """Assert that the output contains any of the given keywords

        Args:
          keywords (str): keywords to examine

        Returns:
          True if the output contains any of the keywords, False otherwise
        """
        for keyword in keywords:
            if self.contains(keyword):
                return True
        return False

    def matches(self, regexp):
        """Assert that the output contains text which the patten matches

        Args:
          regexp (str): search pattern

        Returns:
          True if the output contains matching text, False otherwise
        """
        matcher = re.compile(regexp.format(**self.kwargs), re.MULTILINE)
        return bool(matcher.search(self.output))


    def matchesAll(self, *regexps):
        """Assert that the output contains text which the patterns match

        Args:
          regexp (str): search patterns

        Returns:
          True if the output contains matching text, False otherwise
        """
        for regexp in regexps:
            if not self.matches(regexp):
                return False
        return True

    def __repr__(self):
        """Output string
        """
        return "'{0}'".format(self.output)

    def __str__(self):
        """Output string
        """
        return self.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class FileOutput(Output):
    def __init__(self, filename, kwargs={}):
        self.filename = filename
        with open(os.path.join(filename), "r") as f:
            super(FileOutput, self).__init__(f.read(), kwargs)

    def __repr__(self):
        return "{0}: {1}".format(self.filename, super(FileOutput, self).__repr__())


class Files(object):
    def __init__(self, build_dir, kwargs={}):
        self.build_dir = build_dir
        self.kwargs = kwargs

    def __repr__(self):
        return "Files: ['build_dir': {0}]".format(self.build_dir)

    def exists(self, path):
        return os.path.exists(os.path.join(self.build_dir, path))

    def read(self, path):
        path = path.format(**self.kwargs)
        f = os.path.join(self.build_dir, path)
        assert os.path.exists(f)
        return FileOutput(f, self.kwargs)

    def remove(self, path):
        f = os.path.join(self.build_dir, path)
        if os.path.isfile(f):
            os.remove(f)
        if os.path.isdir(f):
            shutil.rmtree(f)


class Outputs(object):
    def __init__(self, kwargs={}):
        self.outputs = {}
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __setitem__(self, key, value):
        self.outputs[key] = value
        setattr(self, key, self.outputs[key])

    def __getitem__(self, key):
        return self.outputs[key]

    def __delitem__(self, key):
        self.outputs.pop(key)
        delattr(self, key)

    def keys(self):
        return self.outputs.keys()

    def __repr__(self):
        data = ", ".join("'{0}': {1}".format(key, value) for (key, value) in self.outputs.items())
        return "{0}: {{{1}}}".format(type(self).__name__, data)

    def __str__(self):
        return self.__repr__()


class Shell(object):
    def __init__(self, script, build_dir, kwargs={}):
        self.script = script
        self.build_dir = build_dir
        self.kwargs = kwargs

    def __repr__(self):
        return "Shell: ['script': {0}, 'build_dir': {1}]".format(self.script, self.build_dir)

    def cmd(self, command):
        c = 'bash -c "source {0} {1} && {2}"'.format(self.script, self.build_dir, command)
        return c

    def run(self, command):
        subprocess.call(self.cmd(command), shell=True)

    def execute(self, command):
        proc = subprocess.Popen(self.cmd(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        streams = proc.communicate()
        return Outputs({
            "stdout": Output(streams[0].decode("utf-8"), self.kwargs),
            "stderr": Output(streams[1].decode("utf-8"), self.kwargs),
            "returncode": proc.returncode})


class SdkShell(Shell):
    def __init__(self, pre_excute_commands, kwargs={}):
        self.pre_excute_commands = pre_excute_commands
        self.kwargs = kwargs

    def __repr__(self):
        return "SdkShell: {0}".format(self.pre_excute_commands)

    def cmd(self, command):
        c = 'bash -O expand_aliases -c "'
        for cur_command in self.pre_excute_commands:
            c += '{0} \n '.format(cur_command)
        c += '{0}"'.format(command)
        return c


class BuildInfo(object):
    def __init__(self, build_dir):
        def readFile(path):
            with open(path, "r") as f:
                return f.read()

        self.build_dir = build_dir
        self.packages = FileOutput(os.path.join(build_dir, "pn-buildlist"))
        self.tasks = FileOutput(os.path.join(build_dir, "task-depends.dot"))

        @property
        def packages(self):
            return self.packages

        @property
        def tasks(self):
            return self.tasks


class BuildEnvironment(object):
    def __init__(self, conf_file, repo_dir, build_dir):
        self.repo_dir = repo_dir
        self.branch = "krogoth"
        self.conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), conf_file)
        self.build_dir = build_dir
        self.initWorkspace()
        self.parseArguments()

    def initWorkspace(self):
        mini_mcf = os.path.join(os.path.dirname(__file__), "mini-mcf.py")
        cmd = "{} -r {} -b {} -c {} -d {}".format(mini_mcf, self.repo_dir, self.branch, self.conf_file, self.build_dir)
        subprocess.call(cmd, shell=True)

    def parseArguments(self):
        self.kwargs = {}
        f = os.path.join(self.repo_dir, "poky", "oe-init-build-env")
        assert os.path.exists(f)
        source = subprocess.check_output('bash -c "source {0} {1} && bitbake core-image-minimal -c populate_sdk -e"'.format(f, self.build_dir), shell=True).decode("utf-8")
        for key in ("BUILD_ARCH",
                    "TUNE_ARCH",
                    "TUNE_PKGARCH",
                    "SDK_NAME",
                    "SDK_EXT",
                    "SDK_VERSION",
                    "IMAGE_BASENAME",
                    "REAL_MULTIMACH_TARGET_SYS",
                    "SDKTARGETSYSROOT",
                    "SDKPATHNATIVE",
                    "TOOLCHAIN_OUTPUTNAME"):
            regexp = "^(?:{key}=)(?:\")(.*)(?:\")$".format(key=key)
            matcher = re.compile(regexp, re.MULTILINE)
            found = matcher.search(source)
            self.kwargs[key] = matcher.search(source).groups()[0] if found else ""

        # Need to find the proper qemu executable name using TUNE_ARCH.
        tune_arch = self.kwargs["TUNE_ARCH"]
        if tune_arch in ("i486", "i586", "i686"):
            self.kwargs["QEMU_ARCH"] = "i386"
        elif tune_arch in ("powerpc"):
            self.kwargs["QEMU_ARCH"] = "powerpc"
        elif tune_arch in ("powerpc64"):
            self.kwargs["QEMU_ARCH"] = "powerpc64"
        else:
            self.kwargs["QEMU_ARCH"] = tune_arch

    @property
    def shell(self):
        def wait_until(condition, timeout, period=1):
            until = time.time() + timeout
            while time.time() < until:
                if condition:
                    return True
                time.sleep(period)
            return False

        f = os.path.join(self.repo_dir, "poky", "oe-init-build-env")
        assert os.path.exists(f)
        assert wait_until(not os.path.exists(os.path.join(self.build_dir, "hashserve.lock")), 10)
        return Shell(f, self.build_dir, self.kwargs)

    @property
    def files(self):
        return Files(self.build_dir, self.kwargs)

    def parse(self, recipe):
        self.shell.run("bitbake {} -g".format(recipe))
        return BuildInfo(self.build_dir)


class SdkBuildEnvironment(BuildEnvironment):
    def __init__(self, conf_file, repo_dir, build_dir):
        super(SdkBuildEnvironment, self).__init__(conf_file, repo_dir, build_dir)
        self.pre_excute_commands = []
        self.install_sdk()

    @property
    def sdk_shell(self):
        pre_excute_commands = []
        for cur_pre_excute_command in self.pre_excute_commands:
            pre_excute_commands.append(cur_pre_excute_command)
        return SdkShell(pre_excute_commands, self.kwargs)

    def install_sdk(self):
        assert self.shell.execute("bitbake core-image-minimal -c populate_sdk").stderr.empty()

        # Check that the SDK can build a specified module.
        path = "tmp/deploy/sdk/{TOOLCHAIN_OUTPUTNAME}.sh".format(**self.kwargs)
        installer = os.path.join(self.build_dir, path)
        assert os.path.exists(installer)

        self.sdk_dir = os.path.join(self.build_dir, "sdk")
        self.shell.execute("{0} -d {1} -y".format(installer, self.sdk_dir))

        sdk_env_setup_path = '{0}/environment-setup-{1}'.format(self.sdk_dir, self.kwargs["REAL_MULTIMACH_TARGET_SYS"])
        assert os.path.exists(sdk_env_setup_path)

        self.pre_excute_commands.append('cd {0}'.format(self.build_dir))
        self.pre_excute_commands.append('source {0}'.format(sdk_env_setup_path))

        with open(sdk_env_setup_path, "r") as f:
            regexp = "(export {key}=)(?:\")(.*)(?:\")$".format(key='OECORE_NATIVE_SYSROOT')
            matcher = re.compile(regexp, re.MULTILINE)
            source = f.read()
            self.oecore_native_sysroot = matcher.search(source).groups()[1]


@pytest.fixture(scope="session")
def bare_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/bare.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def release_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/release.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def test_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/test.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def report_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/report.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def sdk_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return SdkBuildEnvironment(conf_file="conf/bare.conf", repo_dir=repo_dir, build_dir=build_dir)
