inherit cpptest


EXTRA_QMAKEVARS_PRE:append:class-target = " CONFIG+=gcov"
EXTRA_QMAKEVARS_PRE:append:class-target = " ${@bb.utils.contains('SHIFT_TEST_SUPPRESS_FAILURES', '1', 'CONFIG+=insignificant_test', '', d)}"

FILES:${PN}:append:class-target = " ${OE_QMAKE_PATH_TESTS}"


python qmaketest_do_checkcode() {
    cpptest_checkcode(d)
}

python qmaketest_do_test() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    env = os.environ.copy()

    # Configure QT test arguments
    env["QT_PLUGIN_PATH"] = d.expand("${STAGING_DIR_TARGET}${OE_QMAKE_PATH_PLUGINS}")
    env["QML_IMPORT_PATH"] = d.expand("${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}")
    env["QML2_IMPORT_PATH"] = d.expand("${QML2_IMPORT_PATH}:${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}")
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["TESTRUNNER"] = shiftutils_qemu_run_cmd(d)

    # Let tests run in random order
    if bb.utils.to_boolean(d.getVar("SHIFT_TEST_SHUFFLE", True)):
        env["GTEST_SHUFFLE"] = "1"

    configured = d.getVar("SHIFT_REPORT_DIR", True)

    if configured:
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        mkdirhier(report_dir, True)

        save_metadata(d)

        plain("Generating the test result report", d)
        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir
        # Create QT test report files
        env["TESTARGS"] = " -o -,txt -o test_result.xml,xunitxml"

    for gcdaFile in find_files(d.getVar("B", True), "*.gcda"):
        bb.utils.remove(gcdaFile)

    # Prepare for the coverage reports
    check_call(["lcov", "-c", "-i",
                "-d", d.getVar("B", True),
                "-o", d.expand("${B}/coverage_base.info"),
                "--ignore-errors", "gcov",
                "--gcov-tool", d.expand("${TARGET_PREFIX}gcov"),
                shiftutils_get_branch_coverage_option(d, "lcov")], d)

    # Run tests matching regular expression
    if d.getVar("SHIFT_TEST_FILTER", True):
        env["GTEST_FILTER"] = d.getVar("SHIFT_TEST_FILTER", True)

    try:
        timeout(exec_proc, "make --quiet check", d, env=env, cwd=d.getVar("B", True))
    except bb.process.ExecutionError as e:
        if not bb.utils.to_boolean(d.getVar("SHIFT_TEST_SUPPRESS_FAILURES", True)):
            error(str(e), d)
        if d.getVar("SHIFT_TIMEOUT", True) and e.exitcode == 124:
            err = bb.BBHandledException(e)
            err.exitcode = e.exitcode
            raise err

    if configured:
        if os.path.exists(report_dir):
            # Prepend the package name to each of the classname tags for GTest reports
            xml_files = find_files(report_dir, "*.xml")
            replace_files(xml_files, 'classname="', d.expand('classname="${PN}.'))

            # Prepend the package name to each of the testsuite tags for QTest reports
            xml_files = find_files(d.getVar("B", True), "test_result.xml")
            replace_files(xml_files, '(<testsuite(.*?)name=")', d.expand(r'\g<1>${PN}.'))

            # Copy QTest reports to the report directory
            for xml_file in xml_files:
                rel_path = os.path.relpath(xml_file, d.getVar("B", True))
                new_path = os.path.join(report_dir, rel_path)
                bb.utils.mkdirhier(os.path.dirname(new_path))
                bb.utils.copyfile(xml_file, new_path)
        else:
            warn("No test report files found at %s" % report_dir, d)
}

python qmaketest_do_coverage() {
    cpptest_coverage(d)
}

python qmaketest_do_checktest() {
    cpptest_checktest(d)
}

python qmaketest_do_checkrecipe() {
    shifttest_checkrecipe(d)
}

python qmaketest_do_checkcache() {
    shifttest_checkcache(d)
}

python qmaketest_do_report() {
    shifttest_report(d)
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest do_checkrecipe do_checkcache do_report
