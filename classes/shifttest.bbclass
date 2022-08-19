inherit shiftutils


DEPENDS_prepend_class-target = "\
    gtest \
    gmock \
    lcov-native \
    python-lcov-cobertura-native \
    qemu-native \
    cppcheck-native \
    cpplint-native \
    compiledb-native \
    sage-native \
    oelint-adv-native \
    "

DEBUG_BUILD_class-target = "1"


addtask checkcode after do_compile
do_checkcode[nostamp] = "1"
do_checkcode[doc] = "Runs static analysis for the target"

python shifttest_do_checkcode() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    # Configure default arguments
    cmdline = ["sage", "--verbose",
               "--source-path", d.getVar("S", True),
               "--build-path", d.getVar("B", True),
               "--tool-path", d.expand("${STAGING_DIR_NATIVE}${bindir}"),
               "--target-triple", d.getVar("TARGET_SYS", True)]

    exc_list = shlex_split(d.getVar("SHIFT_CHECKCODE_EXCLUDES", True))
    if len(exc_list) > 0:
        cmdline.append('--exclude-path="%s"' % " ".join(exc_list))

    # Configure the output path argument
    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcode")
        mkdirhier(report_dir, True)

        save_metadata(d)

        cmdline.extend(["--output-path", report_dir])

    # Configure tool options
    debug("Configuring the checkcode tool options")
    for tool in set(["metrix++", "duplo"] + (d.getVar("SHIFT_CHECKCODE_TOOLS", True) or "").split()):
        options = d.getVarFlag("SHIFT_CHECKCODE_TOOL_OPTIONS", tool, True)
        if options:
            cmdline.append(tool + ":" + options.replace(" ", r"\ "))
        else:
            cmdline.append(tool)

    try:
        # Make sure that the compile_commands.json file is available
        json_file = d.expand("${B}/compile_commands.json")
        temporary = False

        if not os.path.exists(json_file):
            plain("Creating the compile_commands.json using compiledb", d)
            try:
                exec_proc("compiledb --command-style -n make", d, cwd=d.getVar("B", True))
                temporary = True
            except bb.process.ExecutionError as e:
                warn("Failed to create the compile_commands.json using compiledb", d)

        # Run sage
        try:
            exec_proc(cmdline, d, cwd=d.getVar("B", True))
        except bb.process.ExecutionError as e:
            error("Failed to run static analysis: %s" % e, d)

    finally:
        if temporary:
            bb.utils.remove(json_file)
}


addtask test after do_compile
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

shifttest_do_test() {
    bbfatal "'inherit shifttest' is not allowed. You should inherit an appropriate bbclass instead."
}


addtask coverage after do_test
do_coverage[nostamp] = "1"
do_coverage[doc] = "Measures code coverage for the target"

python shifttest_do_coverage() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    if d.getVar("SHIFT_REPORT_DIR", True):
        test_result_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        if len(find_files(test_result_dir, "*.[xX][mM][lL]")) == 0:
            warn("No test result files generated at %s" % test_result_dir, d)
            return

    LCOV_DATAFILE_BASE = d.expand("${B}/coverage_base.info")
    LCOV_DATAFILE_TEST = d.expand("${B}/coverage_test.info")
    LCOV_DATAFILE_TOTAL = d.expand("${B}/coverage_total.info")
    LCOV_DATAFILE = d.expand("${B}/coverage.info")
    BRANCH_COVERAGE_OPTION = shiftutils_get_branch_coverage_option(d, "lcov")

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
                BRANCH_COVERAGE_OPTION], d)

    check_call(["lcov",
                "-a", LCOV_DATAFILE_BASE,
                "-a", LCOV_DATAFILE_TEST,
                "-o", LCOV_DATAFILE_TOTAL,
                BRANCH_COVERAGE_OPTION], d)

    check_call(["lcov",
                "--extract", LCOV_DATAFILE_TOTAL,
                BRANCH_COVERAGE_OPTION,
                d.expand('"${S}/*"'),
                "-o", LCOV_DATAFILE], d)

    if d.getVar("SHIFT_COVERAGE_EXCLUDES", True):
        import glob
        cmd = ["lcov", "--remove", LCOV_DATAFILE, "-o", LCOV_DATAFILE,
               BRANCH_COVERAGE_OPTION]
        exc_path_list = []
        source_root = d.getVar("S", True)
        for exc in shlex_split(d.getVar("SHIFT_COVERAGE_EXCLUDES", True)):
            exc_list = glob.glob("%s/%s" % (source_root, exc))
            for exc_path in exc_list:
                if os.path.exists(exc_path):
                    if os.path.isdir(exc_path):
                        exc_path_list += find_files(exc_path, "*")
                    else:
                        exc_path_list.append(exc_path)
            if len(exc_list) == 0:
                warn("SHIFT_COVERAGE_EXCLUDES: no file matches %s" % str(exc), d)
        if len(exc_path_list) > 0:
            check_call(cmd + exc_path_list, d)

    plain("GCC Code Coverage Report", d)
    exec_proc(["lcov", "--list", LCOV_DATAFILE, BRANCH_COVERAGE_OPTION], d)

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/coverage")
        xml_file = os.path.join(report_dir, "coverage.xml")

        mkdirhier(report_dir, True)

        save_metadata(d)

        check_call(["genhtml", LCOV_DATAFILE,
                    "--demangle-tool", d.expand("${TARGET_PREFIX}c++filt"),
                    "--demangle-cpp",
                    "--output-directory", report_dir,
                    "--ignore-errors", "source",
                    shiftutils_get_branch_coverage_option(d, "genhtml")], d)

        check_call(["nativepython", "-m", "lcov_cobertura", LCOV_DATAFILE,
                    "--demangle-tool", d.expand("${TARGET_PREFIX}c++filt"),
                    "--demangle",
                    "--output", xml_file], d, cwd=d.getVar("S", True))

        if os.path.exists(xml_file):
            # Prepend the package name to each of the package tags
            replace_files([xml_file], '(<package.*name=")', d.expand(r'\g<1>${PN}.'))
        else:
            warn("No coverage report files generated at %s" % report_dir, d)
}


addtask checkcache after do_build
do_checkcache[nostamp] = "1"
do_checkcache[doc] = "Check cache availability of the recipe"

python shifttest_do_checkcache() {
    def make_plain_report(print_list):
        def newline(new_str=""):
            return "%s\n" % new_str

        ret = ""
        for title, found, missed in print_list:
            wanted = len(found) + len(missed)
            ret += newline(title)
            ret += newline("-" * len(title))
            if wanted != 0:
                ret += newline("Wanted : %d (%d%%)" % (wanted, 100 * wanted / wanted))
                ret += newline("Found  : %d (%d%%)" % (len(found), 100 * len(found) / wanted))
                ret += newline("Missed : %d (%d%%)" % (len(missed), 100 * len(missed) / wanted))
            else:
                ret += newline("Wanted : %d (-%%)" % (wanted))
                ret += newline("Found  : %d (-%%)" % (len(found)))
                ret += newline("Missed : %d (-%%)" % (len(missed)))
            ret += newline()

        return ret

    def make_json_report(print_list):
        import json
        json_dict = dict()

        for title, found, missed in print_list:
            json_dict[title] = dict()
            json_dict[title]["Summary"] = dict()
            json_dict[title]["Summary"]["Wanted"] = len(found) + len(missed)
            json_dict[title]["Summary"]["Found"] = len(found)
            json_dict[title]["Summary"]["Missed"] = len(missed)
            json_dict[title]["Found"] = [str(x) for x in found]
            json_dict[title]["Missed"] = [str(x) for x in missed]

        return json.dumps(json_dict, indent=2) + "\n"

    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    if "checkcache" not in str(d.getVar("INHERIT", True)):
        fatal("The task needs to inherit checkcache", d)

    try:
        found_sstate, missed_sstate = shiftutils_get_sstate_availability(d, True)
    except Exception as e:
        debug("Handle version with no siginfo parameter: %s" % str(e))
        found_sstate, missed_sstate = shiftutils_get_sstate_availability(d, False)

    found_source, missed_source = shiftutils_get_source_availability(d)

    plain_report_str = str(make_plain_report([("Shared State Availability", found_sstate, missed_sstate), ("Source Availability", found_source, missed_source)]))

    for splited in plain_report_str.splitlines():
        plain(splited, d)

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcache")
        mkdirhier(report_dir, True)

        save_metadata(d)

        with open(os.path.join(report_dir, "caches.json"), "w") as f:
            f.write(make_json_report([("Shared State", found_sstate, missed_sstate), ("Premirror", found_source, missed_source)]))
}


addtask checkrecipe
do_checkrecipe[nostamp] = "1"
do_checkrecipe[depends] += "oelint-adv-native:do_populate_sysroot"
do_checkrecipe[doc] = "Checks the target recipe against the OpenEmbedded style guide"

python shifttest_do_checkrecipe() {
    def lines_of_code(files):
        pairs = []
        for f in files:
            with open(f, "r") as fd:
                pairs.append({
                    "file": os.path.relpath(f, os.getcwd()),
                    "code_lines": sum(1 for line in fd)
                })
        return { "lines_of_code": pairs }

    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    if not d.getVar("FILE", True):
        fatal("Failed to find the recipe file", d)

    cmdline = ["oelint-adv", d.getVar("FILE", True)]

    cmdline.append(d.getVar("__BBAPPEND", True) or "")

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkrecipe")
        mkdirhier(report_dir, True)

        save_metadata(d)

        bb_files = d.getVar("FILE", True) + " " + d.getVar("__BBAPPEND", True) or ""
        bb_files = bb_files.strip().split()
        save_as_json(lines_of_code(bb_files),
                     d.expand("${SHIFT_REPORT_DIR}/${PF}/checkrecipe/files.json"))

        report_path = os.path.join(report_dir, "recipe_violations.json")
        cmdline.append("--output %s" % report_path)

    cmdline += ["--relpaths", "--quiet", "--exit-zero"]

    if d.getVar("SHIFT_CHECKRECIPE_SUPPRESS_RULES", True):
        cmdline.extend(["--suppress %s" % x for x in d.getVar("SHIFT_CHECKRECIPE_SUPPRESS_RULES", True).split()])

    if d.getVar("SHIFT_CHECKRECIPE_ADD_RULES", True):
        cmdline.extend(["--addrules %s" % x for x in d.getVar("SHIFT_CHECKRECIPE_ADD_RULES", True).split()])

    try:
        exec_proc(cmdline, d)
    except bb.process.ExecutionError as e:
        warn("checkrecipe failed: %s" % e, d)
}


addtask report after do_compile
do_report[nostamp] = "1"
do_report[doc] = "Generates reports for the target"

python shifttest_do_report() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    if not d.getVar("SHIFT_REPORT_DIR", True):
        warn("SHIFT_REPORT_DIR is not set. No reports will be generated.", d)

    dd = d.createCopy()

    dd.setVar("BB_CURRENTTASK", "checkcode")
    exec_func("do_checkcode", dd)

    dd.setVar("BB_CURRENTTASK", "test")
    exec_func("do_test", dd)

    dd.setVar("BB_CURRENTTASK", "coverage")
    exec_func("do_coverage", dd)

    if "checkcache" in str(dd.getVar("INHERIT", True)):
        dd.setVar("BB_CURRENTTASK", "checkcache")
        exec_func("do_checkcache", dd)
    else:
        warn("Skipping do_checkcache because checkcache is not inherited", dd)

    dd.setVar("BB_CURRENTTASK", "checkrecipe")
    exec_func("do_checkrecipe", dd)
}


python() {
    # Synchronize the tasks
    if not bb.utils.to_boolean(d.getVar("SHIFT_PARALLEL_TASKS", True)):
        d.appendVarFlag("do_checkcode", "lockfiles", "${TMPDIR}/do_checkcode.lock")
        d.appendVarFlag("do_test", "lockfiles", "${TMPDIR}/do_test.lock")
        d.appendVarFlag("do_coverage", "lockfiles", "${TMPDIR}/do_coverage.lock")
        d.appendVarFlag("do_checktest", "lockfiles", "${TMPDIR}/do_checktest.lock")
        d.appendVarFlag("do_checkcache", "lockfiles", "${TMPDIR}/do_checkcache.lock")
        d.appendVarFlag("do_checkrecipe", "lockfiles", "${TMPDIR}/do_checktest.lock")
        d.appendVarFlag("do_report", "lockfiles", "${TMPDIR}/do_report.lock")
}
