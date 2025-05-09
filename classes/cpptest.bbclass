inherit shifttest


DEPENDS:prepend:class-target = "\
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', bb.utils.contains('SHIFT_CHECKTEST_ENABLED', '1', 'sentinel-native', '', d), '', d)} \
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', bb.utils.contains('SHIFT_CHECKCODE_TOOLS', 'clang-tidy', d.expand('clang-cross-${TUNE_ARCH}'), '', d), '', d)} \
    compiledb-native \
    coreutils-native \
    cppcheck-native \
    cpplint-native \
    gmock \
    gtest \
    lcov-native \
    python3-lcov-cobertura-native \
    qemu-native \
    sage-native \
    "

# Fix an issue caused by the '-ffile-prefix-map' option, which modifies source paths in .gcno files, leading to lcov failures
DEBUG_PREFIX_MAP:class-target := "-fcanon-prefix-map \
-fmacro-prefix-map=${S}=${TARGET_DBGSRC_DIR} \
-fdebug-prefix-map=${S}=${TARGET_DBGSRC_DIR} \
-fmacro-prefix-map=${B}=${TARGET_DBGSRC_DIR} \
-fdebug-prefix-map=${B}=${TARGET_DBGSRC_DIR} \
-fdebug-prefix-map=${STAGING_DIR_HOST}= \
-fmacro-prefix-map=${STAGING_DIR_HOST}= \
-fdebug-prefix-map=${STAGING_DIR_NATIVE}= \
-fmacro-prefix-map=${STAGING_DIR_NATIVE}= \
"

# Coverage flag causes the binary to store the absolute path to the gcda file, resulting in a 'buildpaths' QA Issue.
python do_package_qa:prepend() {
    for package in set((d.getVar('PACKAGES', True) or '').split()):
        d.appendVar("INSANE_SKIP:%s" % package, " buildpaths")
}

def cpptest_checkcode(d):
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


# Execute the do_coverage task after the do_test task completes
do_coverage[recrdeptask] += "do_test"

def cpptest_coverage(d):
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
                '"%s"' % os.path.normpath(d.expand('${S}/*')),
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
                    "--demangle-cpp",
                    "--rc", "genhtml_demangle_cpp_tool=%s" % d.expand("${TARGET_PREFIX}c++filt"),
                    "--output-directory", report_dir,
                    "--ignore-errors", "source",
                    shiftutils_get_branch_coverage_option(d, "genhtml")], d)

        check_call(["lcov_cobertura", LCOV_DATAFILE,
                    "--demangle-tool", d.expand("${TARGET_PREFIX}c++filt"),
                    "--demangle",
                    "--output", xml_file], d, cwd=d.getVar("S", True))

        if os.path.exists(xml_file):
            # Prepend the package name to each of the package tags
            replace_files([xml_file], '(<package.*name=")', d.expand(r'\g<1>${PN}.'))
        else:
            warn("No coverage report files generated at %s" % report_dir, d)


def cpptest_checktest(d):
    if not bb.utils.to_boolean(d.getVar("SHIFT_CHECKTEST_ENABLED", True)):
        return

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
    del_stamp("do_configure", dd)

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
                  dd.expand(r'\g<1> --target=${TARGET_SYS}\g<2>'))

    # Create test reports
    dd.setVar("SHIFT_REPORT_DIR", expected_dir)

    import time
    started = time.time()
    exec_func("do_test", dd)
    elapsed = max(int(dd.getVar("SHIFT_CHECKTEST_MAX_TIMEOUT", True)), round(time.time() - started) * 2.0)

    test_result_dir = dd.expand("${SHIFT_REPORT_DIR}/${PF}/test")
    if len(find_files(test_result_dir, "*.[xX][mM][lL]")) == 0:
        warn("No test result files generated at %s" % test_result_dir, dd)
        return

    try:
        exec_func("do_coverage", dd)
        coverage_file = dd.expand("${B}/coverage.info")
        coverage_info = shiftutils_get_coverage_info(dd, coverage_file)
    except Exception as e:
        warn("Failed to read %s: %s" % (coverage_file, str(e)), dd)
        coverage_info = dict()

    debug("coverage_info: %s" % str(coverage_info))

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
        error("Populating failed: %s" % e, dd)
        return

    for line in readlines(mutant_file):
        mutated_file = line.split(",")[1]
        mutated_line = line.split(",")[3]
        if not (mutated_file in coverage_info and mutated_line in coverage_info[mutated_file]):
            debug("Mutated code line uncovered by test cases - ignore (%s)" % str(line))
            try:
                exec_proc(["sentinel", "evaluate",
                           "--mutant", '"%s"' % line,
                           "--expected", expected_dir,
                           "--actual", actual_dir,
                           "--output-dir", eval_dir,
                           "--test-state", "uncovered",
                           verbose,
                           dd.getVar("S", True)], dd)
            except:
                pass
            continue

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

        save_metadata(d)

        cmdline.extend(["--output-dir", report_dir])

    try:
        exec_proc(cmdline, dd)
    except bb.process.ExecutionError as e:
        warn("Reporting failed: %s" % e, dd)
        return
