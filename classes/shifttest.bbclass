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
    metrixpp-native \
    duplo-native \
    flawfinder-native \
    sage-native \
    oelint-adv-native \
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', 'sentinel-native', '', d)} \
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', d.expand('clang-cross-${TUNE_ARCH}'), '', d)} \
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

        save_as_json({"S": d.getVar("S", True) or ""},
                     d.expand("${SHIFT_REPORT_DIR}/${PF}/metadata.json"))

        cmdline.extend(["--output-path", report_dir])

    # Configure tool options
    debug("Configuring the checkcode tool options")
    for tool in (d.getVar("SHIFT_CHECKCODE_TOOLS", True) or "").split():
        options = d.getVarFlag("SHIFT_CHECKCODE_TOOL_OPTIONS", tool, True)
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
            try:
                exec_proc("compiledb --command-style -n make", d, cwd=d.getVar("B", True))
                temporary = True
            except bb.process.ExecutionError as e:
                warn("Failed to create the compile_commands.json using compiledb", d)

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
do_coverage[doc] = "Measures code coverage for the target"

python shifttest_do_coverage() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

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

    if d.getVar("SHIFT_COVERAGE_EXCLUDES", True):
        cmd = ["lcov", "--remove", LCOV_DATAFILE, "-o", LCOV_DATAFILE]
        exc_path_list = []
        for exc in shlex_split(d.getVar("SHIFT_COVERAGE_EXCLUDES", True)):
            exc_path = os.path.join(d.getVar("S", True), exc)
            if os.path.exists(exc_path):
                if os.path.isdir(exc_path):
                    exc_path_list += find_files(exc_path, "*")
                else:
                    exc_path_list.append(exc_path)
            else:
                warn("SHIFT_COVERAGE_EXCLUDES: %s doesn't exist" % str(exc_path), d)
        if len(exc_path_list) > 0:
            check_call(cmd + exc_path_list, d)

    plain("GCC Code Coverage Report", d)
    exec_proc(["lcov", "--list", LCOV_DATAFILE, "--rc", "lcov_branch_coverage=1"], d)

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/coverage")
        xml_file = os.path.join(report_dir, "coverage.xml")

        mkdirhier(report_dir, True)

        save_as_json({"S": d.getVar("S", True) or ""},
                     d.expand("${SHIFT_REPORT_DIR}/${PF}/metadata.json"))

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
            warn("No coverage report files generated at %s" % report_dir, d)
}


addtask checktest after do_compile do_install do_populate_sysroot
do_checktest[nostamp] = "1"
do_checktest[doc] = "Runs mutation tests for the target"

python shifttest_do_checktest() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    dd = d.createCopy()

    if "clang-layer" not in dd.getVar("BBFILE_COLLECTIONS", True).split():
        fatal("The task requires meta-clang to be present", dd)

    dot_git_path = dd.expand("${S}/.git")
    if not os.path.exists(dot_git_path) or not os.path.isdir(dot_git_path):
        warn("No .git directory in source directory", dd)
        return

    work_dir = dd.expand("${WORKDIR}/mutation_test_tmp")
    expected_dir = os.path.join(work_dir, "original")
    actual_dir = os.path.join(work_dir, "actual")
    backup_dir = os.path.join(work_dir, "backup")
    eval_dir = os.path.join(work_dir, "eval")

    # Invalidate the pseudo database and the stamp to keep the build state safe
    if dd.getVar("PSEUDO_LOCALSTATEDIR", True):
        bb.utils.remove(dd.getVar("PSEUDO_LOCALSTATEDIR", True), True)
    bb.build.del_stamp("do_configure", dd)

    # Prepare the work directory
    mkdirhier(work_dir, True)

    json_file = dd.expand("${B}/compile_commands.json")
    new_file = os.path.join(work_dir, "compile_commands.json")

    # Make sure that compile_commands.json is available
    if os.path.exists(json_file):
        bb.utils.copyfile(json_file, new_file)
    else:
        debug("Creating compile_commands.json using compiledb")
        try:
            check_call("compiledb --command-style make", dd, cwd=dd.getVar("B", True))
            bb.utils.movefile(json_file, new_file)
        except bb.process.ExecutionError as e:
            warn("Failed to create the compile_commands.json using compiledb", dd)
            return

    # Insert the target option to the file
    replace_files([new_file],
                  '("command": ".*)(")',
                  dd.expand('\g<1> --target=${TARGET_SYS}\g<2>'))

    # Create test reports
    dd.setVar("SHIFT_REPORT_DIR", expected_dir)

    import time
    started = time.time()
    exec_func("do_test", dd)
    elapsed = max(30, round(time.time() - started) * 2.0)

    test_result_dir = dd.expand("${SHIFT_REPORT_DIR}/${PF}/test")
    if len(find_files(test_result_dir, "*.[xX][mM][lL]")) == 0:
        warn("No test result files generated at %s" % test_result_dir, dd)
        return

    debug("Creating the mutation database")
    mutant_file = os.path.join(work_dir, "mutables.db")
    verbose = "--verbose" if bb.utils.to_boolean(dd.getVar("SHIFT_CHECKTEST_VERBOSE", True)) else ""

    try:
        exec_proc(["sentinel", "populate",
                   "--work-dir", work_dir,
                   "--build-dir", work_dir,
                   "--output-dir", work_dir,
                   "--generator", dd.getVar("SHIFT_CHECKTEST_GENERATOR", True),
                   "--scope", dd.getVar("SHIFT_CHECKTEST_SCOPE", True),
                   "--limit", dd.getVar("SHIFT_CHECKTEST_LIMIT", True),
                   "--mutants-file-name", os.path.basename(mutant_file),
                   " ".join(["--extensions=" + ext for ext in dd.getVar("SHIFT_CHECKTEST_EXTENSIONS", True).split()]),
                   " ".join(['--exclude="%s"' % exc for exc in shlex_split(dd.getVar("SHIFT_CHECKTEST_EXCLUDES", True))]),
                   verbose,
                   dd.expand("--seed ${SHIFT_CHECKTEST_SEED}") if dd.getVar("SHIFT_CHECKTEST_SEED", True) else "",
                   dd.getVar("S", True)], dd)
    except bb.process.ExecutionError as e:
        warn("Populating failed: %s" % e)
        return

    for line in readlines(mutant_file):
        try:
            debug("Mutating the source")
            exec_proc(["sentinel", "mutate",
                       "--mutant", '"%s"' % line,
                       "--work-dir", backup_dir,
                       verbose,
                       dd.getVar("S", True)], dd)
            try:
                test_state = "success"
                exec_func("do_configure", dd)
                exec_func("do_compile", dd)
                exec_func("do_install", dd)
                exec_func("do_populate_sysroot", dd)

                dd.setVar("SHIFT_REPORT_DIR", actual_dir)
                bb.utils.remove(actual_dir, True)
                bb.utils.mkdirhier(actual_dir)
                exec_func("do_test", dd,
                          bb.utils.to_boolean(dd.getVar("SHIFT_CHECKTEST_VERBOSE", True)),
                          timeout=elapsed)
            except (bb.BBHandledException, bb.process.ExecutionError) as e:
                debug("Failed to run do_checktest: %s" % e)
                test_state = "timeout" if e.exitcode == 124 else "build_failure"

            debug("Evaluating the test result")
            exec_proc(["sentinel", "evaluate",
                       "--mutant", '"%s"' % line,
                       "--expected", expected_dir,
                       "--actual", actual_dir,
                       "--output-dir", eval_dir,
                       "--test-state", test_state,
                       verbose,
                       dd.getVar("S", True)], dd)
        finally:
            debug("Restoring the mutated source")
            for filename in oe.path.find(backup_dir):
                os.utime(filename, None)
            oe.path.copytree(backup_dir, dd.getVar("S", True))
            bb.utils.remove(backup_dir, True)

    # Create the mutation test report if necessary
    cmdline = ["sentinel", "report",
               "--evaluation-file", os.path.join(eval_dir, "EvaluationResults"),
               verbose,
               dd.getVar("S", True)]

    if d.getVar("SHIFT_REPORT_DIR", True):  # Use original datastore
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checktest")
        mkdirhier(report_dir, True)

        save_as_json({"S": d.getVar("S", True) or ""},
                     d.expand("${SHIFT_REPORT_DIR}/${PF}/metadata.json"))

        cmdline.extend(["--output-dir", report_dir])

    try:
        exec_proc(cmdline, dd)
    except bb.process.ExecutionError as e:
        warn("Reporting failed: %s" % e)
        return
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
                for task in found:
                    ret += newline("    %s" % task)
                ret += newline("Missed : %d (%d%%)" % (len(missed), 100 * len(missed) / wanted))
                for task in missed:
                    ret += newline("    %s" % task)
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

    found_source = list()
    missed_source = list()

    total_depends = set()
    taskdepdata = shiftutils_get_taskdepdata(d)
    if taskdepdata:
        for td in taskdepdata:
            total_depends.add(taskdepdata[td][0])

    total_depends_remove_virtual = set()
    
    for dep in total_depends:
        if dep.startswith("virtual/"):
            dep = d.getVar("PREFERRED_PROVIDER_%s" % dep, True)

        if dep:
            total_depends_remove_virtual.add(dep)

    for dep in total_depends_remove_virtual:
        try:
            path = d.expand("${TOPDIR}/checkcache/%s" % dep)

            with open(os.path.join(path,"source_availability"), "r") as f:
                source_availability = bool(f.read())
                if source_availability:
                    found_source.append(dep)
                else:
                    missed_source.append(dep)

        except Exception as e:
            debug("Failed to read information of %s:%s" % (dep, str(e)))

    found_source.sort()
    missed_source.sort()

    plain(make_plain_report([("Source Availability", found_source, missed_source)]), d)

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcache")
        mkdirhier(report_dir, True)

        save_as_json({"S": d.getVar("S", True) or ""},
                     d.expand("${SHIFT_REPORT_DIR}/${PF}/metadata.json"))

        with open(os.path.join(report_dir, "caches.json"), "w") as f:
            f.write(make_json_report([("Shared State", [], []), ("Premirror", found_source, missed_source)]))
}

addtask checkrecipe
do_checkrecipe[nostamp] = "1"
do_checkrecipe[depends] += "oelint-adv-native:do_populate_sysroot"
do_checkrecipe[doc] = "Checks the target recipe against the OpenEmbedded style guide"

python shifttest_do_checkrecipe() {
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

        save_as_json({"S": d.getVar("S", True) or ""},
                     d.expand("${SHIFT_REPORT_DIR}/${PF}/metadata.json"))

        report_path = os.path.join(report_dir, "recipe_violations.json")
        cmdline.append("--output %s" % (report_path))

    cmdline.append("--quiet --addrules jetm")
    exec_proc(cmdline, d)
}


addtask report after do_compile do_install do_populate_sysroot
do_report[nostamp] = "1"
do_report[doc] = "Makes reports for the target"

python shifttest_do_report() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    if not d.getVar("SHIFT_REPORT_DIR", True):
        fatal("You should set SHIFT_REPORT_DIR to make reports", d)

    plain("Making a report for do_checkcode", d)
    exec_func("do_checkcode", d)

    plain("Making a report for do_test", d)
    exec_func("do_test", d)

    plain("Making a report for do_coverage", d)
    exec_func("do_coverage", d)

    if "checkcache" in str(d.getVar("INHERIT", True)):
        plain("Making a report for do_checkcache", d)
        exec_func("do_checkcache", d)
    else:
        warn("Skipping do_checkcache because checkcache is not inherited", d)
        

    plain("Making a report for do_checkrecipe", d)
    exec_func("do_checkrecipe", d)

    if "clang-layer" in d.getVar("BBFILE_COLLECTIONS", True).split():
        plain("Making a report for do_checktest", d)
        exec_func("do_checktest", d)
    else:
        warn("Skipping do_checktest because there is no clang-layer", d)
}


python() {
    if d.getVar("SHIFT_TIMEOUT", True):
        fatal("You cannot use SHIFT_TIMEOUT as it is internal to shifttest.bbclass.", d)

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
