DEPENDS_prepend = "\
    gtest \
    gmock \
    lcov-native \
    python-lcov-cobertura-native \
    qemu-native \
    cppcheck-native \
    cpplint-native \
    compiledb-native \
    metrixpp-native \
    duplo-native \
    flawfinder-native \
    sage-native \
    oelint-adv-native \
    "

DEBUG_BUILD = "1"


def plain(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.plain(s)


def warn(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.warn(s)


def error(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.error(s)


def fatal(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.fatal(s)


def mkdirhier(path, clean=False):
    if clean and os.path.exists(path):
        bb.debug(1, "Removing the existing directory: %s" % path)
        bb.utils.remove(path, True)
    bb.utils.mkdirhier(path)


def find_files(directory, pattern):
    import fnmatch
    found = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                found.append(os.path.join(root, filename))
    return found


def replace_files(files, pattern, repl):
    import fileinput
    import re
    for filename in files:
        bb.debug(1, "Replacing contents: %s" % filename)
        for line in fileinput.input(filename, inplace=True):
            print(re.sub(pattern, repl, line).rstrip())


def readlines(path):
    import io
    with io.open(path, "r", encoding="utf-8") as f:
        for line in f.read().splitlines():
            yield line


def exec_func(func, d, verbose=True, timeout=0):
    try:
        cwd = os.getcwd()
        dd = d.createCopy()
        if not verbose:
            dd.setVar("SHIFT_SUPPRESS_OUTPUT", True)
        if timeout > 0:
            dd.setVar("SHIFT_TIMEOUT", timeout)
        bb.build.exec_func(func, dd)
    finally:
        os.chdir(cwd)


def clamp(value, smallest, largest):
    return sorted((value, smallest, largest))[1]


def timeout(func, cmd, d, **options):
    if not isinstance(cmd, str):
        cmd = " ".join(map(str, cmd))

    period = d.getVar("SHIFT_TIMEOUT", True)
    if period and not cmd.startswith("timeout"):
        cmd = "timeout %d %s" % (int(round(period)), cmd)

    return func(cmd, d, **options)


def check_call(cmd, d, **options):
    if not "shell" in options:
        options["shell"] = True

    if not isinstance(cmd, str):
        cmd = " ".join(map(str, cmd))

    bb.debug(1, 'Executing: "%s"' % cmd)
    import subprocess
    try:
        subprocess.check_call(cmd, **options)
    except subprocess.CalledProcessError as e:
        raise bb.process.ExecutionError(cmd, e.returncode, None, None)


def exec_proc(cmd, d, **options):
    import subprocess

    class Popen(bb.process.Popen):
        defaults = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "stdin": None,
            "shell": True,
        }

        def __init__(self, *args, **kwargs):
            options = dict(self.defaults)
            options.update(kwargs)
            bb.process.Popen.__init__(self, *args, **options)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, value, traceback):
            if self.stdout:
                self.stdout.close()
            if self.stderr:
                self.stderr.close()

    if not isinstance(cmd, str):
        cmd = " ".join(map(str, cmd))

    bb.debug(1, 'Executing: "%s"' % cmd)
    with Popen(cmd, **options) as proc:
        for line in proc.stdout:
            plain(line.decode("utf-8").rstrip(), d)

        proc.wait()
        if proc.returncode != 0:
            raise bb.process.ExecutionError(cmd, proc.returncode, None, None)


addtask checkcode after do_compile
do_checkcode[nostamp] = "1"
do_checkcode[doc] = "Runs static analysis for the target"

python shifttest_do_checkcode() {

    # Configure default arguments
    cmdline = ["sage", "--verbose",
               "--source-path", d.getVar("S", True),
               "--build-path", d.getVar("B", True),
               "--tool-path", d.expand("${STAGING_DIR_NATIVE}${bindir}"),
               "--target-triple", d.getVar("TARGET_SYS", True)]

    # Configure the output path argument
    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcode")
        mkdirhier(report_dir, True)
        cmdline.extend(["--output-path", report_dir])

    # Configure tool options
    bb.debug(1, "Configuring the checkcode tool options")
    for tool in (d.getVar("CHECKCODE_TOOLS", True) or "").split():
        options = d.getVarFlag("CHECKCODE_TOOL_OPTIONS", tool, True)
        if options:
            cmdline.append(tool + ":" + options.replace(" ", "\ "))
        else:
            cmdline.append(tool)

    try:
        # Make sure that the compile_commands.json file is available
        json_file = d.expand("${B}/compile_commands.json")
        temporary = False

        if not os.path.exists(json_file):
            plain("Creating the compile_commands.json using compiledb", d)
            exec_proc("compiledb --command-style -n make", d, cwd=d.getVar("B", True))
            temporary = True

        # Run sage
        exec_proc(cmdline, d, cwd=d.getVar("B", True))

    finally:
        if temporary:
            bb.utils.remove(json_file)
}


# To overwrite the sstate cache libraries for autotools projects
do_install[nostamp] = "1"


addtask test after do_compile do_install do_populate_sysroot
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

shifttest_do_test() {
    bbfatal "'inherit shifttest' is not allowed. You should inherit an appropriate bbclass instead."
}


addtask coverage after do_test
do_coverage[nostamp] = "1"
do_coverage[doc] = "Measures code coverage metrics for the target"

python shifttest_do_coverage() {
    LCOV_DATAFILE_BASE = d.expand("${B}/coverage_base.info")
    LCOV_DATAFILE_TEST = d.expand("${B}/coverage_test.info")
    LCOV_DATAFILE_TOTAL = d.expand("${B}/coverage_total.info")
    LCOV_DATAFILE = d.expand("${B}/coverage.info")

    # Remove files if exist
    bb.utils.remove(LCOV_DATAFILE_TOTAL)
    bb.utils.remove(LCOV_DATAFILE)

    if not find_files(d.getVar("B", True), "*.gcda"):
        warn(d.expand("No .gcda files found at ${B}"), d)
        return

    # Prepare for the coverage reports
    check_call(["lcov", "-c",
                "-d", d.getVar("B", True),
                "-o", LCOV_DATAFILE_TEST,
                "--gcov-tool", d.expand("${TARGET_PREFIX}gcov"),
                "--rc", "lcov_branch_coverage=1"], d)

    check_call(["lcov",
                "-a", LCOV_DATAFILE_BASE,
                "-a", LCOV_DATAFILE_TEST,
                "-o", LCOV_DATAFILE_TOTAL,
                "--rc", "lcov_branch_coverage=1"], d)

    check_call(["lcov",
                "--extract", LCOV_DATAFILE_TOTAL,
                "--rc", "lcov_branch_coverage=1",
                d.expand('"${S}/*"'),
                "-o", LCOV_DATAFILE], d)

    plain("GCC Code Coverage Report", d)
    exec_proc(["lcov", "--list", LCOV_DATAFILE, "--rc", "lcov_branch_coverage=1"], d)

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/coverage")
        xml_file = os.path.join(report_dir, "coverage.xml")

        mkdirhier(report_dir, True)

        check_call(["genhtml", LCOV_DATAFILE,
                    "--demangle-tool", d.expand("${TARGET_PREFIX}c++filt"),
                    "--demangle-cpp",
                    "--output-directory", report_dir,
                    "--ignore-errors", "source",
                    "--rc", "genhtml_branch_coverage=1"], d)

        check_call(["nativepython", "-m", "lcov_cobertura", LCOV_DATAFILE,
                    "--demangle-tool", d.expand("${TARGET_PREFIX}c++filt"),
                    "--demangle",
                    "--output", xml_file], d, cwd=d.getVar("S", True))

        if os.path.exists(xml_file):
            # Prepend the package name to each of the package tags
            replace_files([xml_file], '(<package.*name=")', d.expand('\g<1>${PN}.'))
        else:
            warn("No coverage report files generated at %s" % report_dir, dd)
}


addtask checkrecipe
do_checkrecipe[nostamp] = "1"
do_checkrecipe[depends] += "oelint-adv-native:do_populate_sysroot"
do_checkrecipe[doc] = "Check target recipe for the OpenEmbedded Style Guide issues."

python shifttest_do_checkrecipe() {
    dd = d.createCopy()

    if not dd.getVar("FILE", True):
        bb.fatal("Fail to find recipe file")

    cmdline = ["oelint-adv", dd.getVar("FILE", True)]

    bbapend = dd.getVar("__BBAPPEND", True)
    if bbapend:
        cmdline.append(bbapend)


    if dd.getVar("SHIFT_REPORT_DIR", True):
        report_dir = dd.expand("${SHIFT_REPORT_DIR}/${PF}/checkrecipe")
        mkdirhier(report_dir, True)
        report_path = os.path.join(report_dir, "recipe_violations.json")
        cmdline.append("--output %s" % (report_path))

    cmdline.append("--quiet --addrules jetm")
    exec_proc(cmdline, dd)
}


addtask report after do_compile do_install do_populate_sysroot
do_report[nostamp] = "1"
do_report[doc] = "Makes reports for the target"

python shifttest_do_report() {
    dd = d.createCopy()

    if not dd.getVar("SHIFT_REPORT_DIR", True):
        bb.fatal("You should set SHIFT_REPORT_DIR for making reports")

    plain("Making report for do_checkcode", dd)
    exec_func("do_checkcode", dd)

    plain("Making report for do_test", dd)
    exec_func("do_test", dd)

    plain("Making report for do_coverage", dd)
    exec_func("do_coverage", dd)

    plain("Making report for do_checkrecipe", dd)
    exec_func("do_checkrecipe", dd)

}


python() {
    if not bb.utils.to_boolean(d.getVar("SHIFT_PARALLEL_TASKS", True)):
        # Synchronize the tasks
        d.appendVarFlag("do_checkcode", "lockfiles", "${TMPDIR}/do_checkcode.lock")
        d.appendVarFlag("do_test", "lockfiles", "${TMPDIR}/do_test.lock")
        d.appendVarFlag("do_coverage", "lockfiles", "${TMPDIR}/do_coverage.lock")
        d.appendVarFlag("do_checktest", "lockfiles", "${TMPDIR}/do_checktest.lock")
        d.appendVarFlag("do_checkrecipe", "lockfiles", "${TMPDIR}/do_checktest.lock")
        d.appendVarFlag("do_report", "lockfiles", "${TMPDIR}/do_report.lock")
}

