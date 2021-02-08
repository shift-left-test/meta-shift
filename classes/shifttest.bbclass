DEPENDS_prepend = "\
    gtest \
    gmock \
    lcov-native \
    python-lcov-cobertura-native \
    qemu-native \
    cppcheck-native \
    cpplint-native \
    compiledb-native \
    sage-native \
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', 'sentinel-native', '', d)} \
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', 'clang-cross-' + d.getVar('TUNE_ARCH', True) + ' ', '', d)} \
    "

DEBUG_BUILD = "1"


def plain(s, d):
    if d.getVar("SHIFT_QUIET", True):
        return
    bb.plain(d.expand("${PF} do_${BB_CURRENTTASK}: ") + s)


def warn(s, d):
    if d.getVar("SHIFT_QUIET", True):
        return
    bb.warn(s)


def error(s, d):
    if d.getVar("SHIFT_QUIET", True):
        return
    bb.error(s)


def fatal(s, d):
    if d.getVar("SHIFT_QUIET", True):
        return
    bb.fatal(s)


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


def exec_func(func, d):
    try:
        cwd = os.getcwd()
        bb.build.exec_func(func, d)
    finally:
        os.chdir(cwd)


def check_call(cmd, d, **options):
    if not "shell" in options:
        options["shell"] = True

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
    kwargs = {
        "source-path": d.getVar("S", True),
        "build-path": d.getVar("B", True),
        "tool-path": d.expand("${STAGING_DIR_NATIVE}${bindir}"),
        "target-triple": d.getVar("TARGET_SYS", True),
        "output-path": "",
        "tool-options": "",
    }

    # Configure the output path argument
    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcode")
        bb.debug(1, "Configuring the checkcode output path: %s" % report_dir)
        bb.utils.remove(report_dir, True)
        bb.utils.mkdirhier(report_dir)
        kwargs["output-path"] = "--output-path=%s" % report_dir

    # Configure tool options
    bb.debug(1, "Configuring the checkcode tool options")
    for tool in (d.getVar("CHECKCODE_TOOLS", True) or "").split():
        kwargs["tool-options"] += " " + tool
        options = d.getVarFlag("CHECKCODE_TOOL_OPTIONS", tool, True)
        if options:
            kwargs["tool-options"] += ":" + options.replace(" ", "\ ")

    try:
        # Make sure that the compile_commands.json file is available
        json_file = d.expand("${B}/compile_commands.json")
        temporary = False

        if not os.path.exists(json_file):
            plain("Creating the compile_commands.json using compiledb", d)
            exec_proc("compiledb --command-style -n make", d, cwd=d.getVar("B", True))
            temporary = True

        # Run sage
        exec_proc("sage --verbose " \
                  "--source-path {source-path} " \
                  "--build-path {build-path} " \
                  "--tool-path {tool-path} " \
                  "--target-triple {target-triple} " \
                  "{output-path} " \
                  "{tool-options}".format(**kwargs), d, cwd=d.getVar("B", True))
    finally:
        if temporary:
            bb.utils.remove(json_file)
}


# In order to overwrite the sstate cache libraries
do_install[nostamp] = "1"


addtask test after do_compile do_populate_sysroot
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
    check_call("lcov -c -d %s -o %s --gcov-tool %s --rc %s" % (
        d.getVar("B", True),
        LCOV_DATAFILE_TEST,
        d.expand("${TARGET_PREFIX}gcov"),
        "lcov_branch_coverage=1"), d)

    check_call("lcov -a %s -a %s -o %s --rc %s" % (
        LCOV_DATAFILE_BASE,
        LCOV_DATAFILE_TEST,
        LCOV_DATAFILE_TOTAL,
        "lcov_branch_coverage=1"), d)

    check_call('lcov --extract %s --rc %s "%s" -o %s' % (
        LCOV_DATAFILE_TOTAL,
        "lcov_branch_coverage=1",
        d.expand("${S}/*"),
        LCOV_DATAFILE), d)

    plain("GCC Code Coverage Report", d)
    exec_proc("lcov --list %s --rc %s" % (
        LCOV_DATAFILE,
        "lcov_branch_coverage=1"), d)

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/coverage")
        xml_file = os.path.join(report_dir, "coverage.xml")

        if os.path.exists(report_dir):
            bb.debug(1, "Removing the existing coverage directory: %s" % report_dir)
            bb.utils.remove(report_dir, True)

        check_call("genhtml %s " \
                   "--demangle-tool %s " \
                   "--demangle-cpp " \
                   "--output-directory %s " \
                   "--ignore-errors %s " \
                   "--rc %s" % (LCOV_DATAFILE,
                                d.expand("${TARGET_PREFIX}c++filt"),
                                report_dir,
                                "source",
                                "genhtml_branch_coverage=1"), d)

        check_call("nativepython -m lcov_cobertura %s " \
                   "--demangle-tool=%s " \
                   "--demangle " \
                   "--output %s" % (LCOV_DATAFILE,
                                    d.expand("${TARGET_PREFIX}c++filt"),
                                    xml_file), d, cwd=d.getVar("S", True))

        if os.path.exists(xml_file):
            # Prepend the package name to each of the package tags
            replace_files([xml_file], '(<package.*name=")', d.expand('\g<1>${PN}.'))
        else:
            warn("No coverage report files generated at %s" % report_dir, dd)
}


addtask checktest after do_compile do_populate_sysroot
do_checktest[nostamp] = "1"
do_checktest[doc] = "Runs mutation tests for the target"

python shifttest_do_checktest() {
    dd = d.createCopy()

    if "clang-layer" not in dd.getVar("BBFILE_COLLECTIONS", True).split():
        bb.fatal("the task requires meta-clang to be present")

    if dd.getVar("EXTERNALSRC", True):
        bb.fatal("the task does not support the external source tree")

    work_dir = dd.expand("${WORKDIR}/mutation_test_tmp")
    expected_dir = os.path.join(work_dir, "original")
    actual_dir = os.path.join(work_dir, "actual")
    backup_dir = os.path.join(work_dir, "backup")
    eval_dir = os.path.join(work_dir, "eval")

    # Prepare the work directory
    if os.path.exists(work_dir):
        bb.debug(1, "Removing the existing work directory: %s" % work_dir)
        bb.utils.remove(work_dir, True)
    bb.utils.mkdirhier(work_dir)

    json_file = dd.expand("${B}/compile_commands.json")
    new_file = os.path.join(work_dir, "compile_commands.json")

    # Make sure that compile_commands.json is available
    if os.path.exists(json_file):
        bb.utils.copyfile(json_file, new_file)
    else:
        bb.debug(1, "Creating compile_commands.json using compiledb")
        check_call("compiledb --command-style make", dd, cwd=dd.getVar("B", True))
        bb.utils.movefile(json_file, new_file)

    # Insert the target option to the file
    replace_files([new_file],
                  '("command": ".*)(")',
                  dd.expand('\g<1> --target=${TARGET_SYS}\g<2>'))

    # Create test reports
    dd.setVar("SHIFT_REPORT_DIR", expected_dir)
    exec_func("do_test", dd)

    bb.debug(1, "Creating the mutation database")
    mutant_file = os.path.join(work_dir, "mutables.db")
    extensions = " ".join(["--extensions=" + ext for ext in dd.getVar("CHECKTEST_EXTENSIONS", True).split()])
    excludes = " ".join(["--exclude=" + ext for ext in dd.getVar("CHECKTEST_EXCLUDES", True).split()])
    verbose = "--verbose" if bb.utils.to_boolean(dd.getVar("CHECKTEST_VERBOSE", True)) else ""
    seed = ""
    if dd.getVar("CHECKTEST_SEED", True):
        seed = "--seed {}".format(dd.getVar("CHECKTEST_SEED", True))
    exec_proc("sentinel populate " \
              "--work-dir {work_dir} " \
              "--build-dir {work_dir} " \
              "--output-dir {work_dir} " \
              "--generator {generator} " \
              "--scope {scope} " \
              "--limit {limit} " \
              "--mutants-file-name {filename} " \
              "{extensions} " \
              "{excludes} " \
              "{verbose} " \
              "{seed} " \
              "{source_dir} ".format(work_dir=work_dir,
                                     generator=dd.getVar("CHECKTEST_GENERATOR", True),
                                     scope=dd.getVar("CHECKTEST_SCOPE", True),
                                     limit=dd.getVar("CHECKTEST_LIMIT", True),
                                     filename=os.path.basename(mutant_file),
                                     extensions=extensions,
                                     excludes=excludes,
                                     verbose=verbose,
                                     seed=seed,
                                     source_dir=dd.getVar("S", True)), dd)

    for line in readlines(mutant_file):
        try:
            bb.debug(1, "Mutating the source")
            exec_proc('sentinel mutate ' \
                      '--mutant "{mutant}" ' \
                      '--work-dir {work_dir} ' \
                      '{verbose} ' \
                      '{source_dir} '.format(mutant=line,
                                             work_dir=backup_dir,
                                             verbose=verbose,
                                             source_dir=dd.getVar("S", True)), dd)
            try:
                test_state = "success"
                exec_func("do_configure", dd)
                exec_func("do_compile", dd)
                exec_func("do_install", dd)
                exec_func("do_populate_sysroot", dd)

                dd.setVar("SHIFT_REPORT_DIR", actual_dir)
                bb.utils.remove(actual_dir, True)
                bb.utils.mkdirhier(actual_dir)
                try:
                    if not bb.utils.to_boolean(dd.getVar("CHECKTEST_VERBOSE", True)):
                        dd.setVar("SHIFT_QUIET", True)
                    exec_func("do_test", dd)
                finally:
                    if not bb.utils.to_boolean(dd.getVar("CHECKTEST_VERBOSE", True)):
                        dd.delVar("SHIFT_QUIET")
            except bb.process.ExecutionError as e:
                bb.debug(1, "do_checktest failed: %s" % e)
                test_state = "build_failure"

            bb.debug(1, "Evaluating the test result")
            exec_proc('sentinel evaluate ' \
                      '--mutant "{mutant}" ' \
                      '--expected {expected_dir} ' \
                      '--actual {actual_dir} ' \
                      '--output-dir {eval_dir} ' \
                      '--test-state {test_state} ' \
                      '{verbose} ' \
                      '{source_dir} '.format(mutant=line,
                                             expected_dir=expected_dir,
                                             actual_dir=actual_dir,
                                             eval_dir=eval_dir,
                                             test_state=test_state,
                                             verbose=verbose,
                                             source_dir=dd.getVar("S", True)), dd)
        finally:
            bb.debug(1, "Restoring the mutated source")
            for filename in oe.path.find(backup_dir):
                os.utime(filename, None)
            oe.path.copytree(backup_dir, dd.getVar("S", True))
            bb.utils.remove(backup_dir, True)

    # Create the mutation test report if necessary
    output_option = ""
    if d.getVar("SHIFT_REPORT_DIR", True):  # Use original datastore
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checktest")
        bb.utils.remove(report_dir, True)
        bb.utils.mkdirhier(report_dir)
        output_option = "--output-dir %s" % report_dir

    exec_proc("sentinel report " \
              "--evaluation-file {eval_file} " \
              "{output_option} " \
              "{verbose} " \
              "{source_dir} ".format(eval_file=os.path.join(eval_dir, "EvaluationResults"),
                                     output_option=output_option,
                                     verbose=verbose,
                                     source_dir=d.getVar("S", True)), d)

    exec_func("do_configure", dd)
    exec_func("do_compile", dd)
    exec_func("do_install", dd)
}


python() {
    if not bb.utils.to_boolean(d.getVar("SHIFT_PARALLEL_TASKS", True)):
        # Synchronize the tasks
        d.appendVarFlag("do_checkcode", "lockfiles", "${TMPDIR}/do_checkcode.lock")
        d.appendVarFlag("do_test", "lockfiles", "${TMPDIR}/do_test.lock")
        d.appendVarFlag("do_coverage", "lockfiles", "${TMPDIR}/do_coverage.lock")
        d.appendVarFlag("do_checktest", "lockfiles", "${TMPDIR}/do_checktest.lock")
}
