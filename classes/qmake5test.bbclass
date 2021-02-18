inherit qmake5
inherit shifttest
inherit shiftutils

EXTRA_QMAKEVARS_PRE_append = " CONFIG+=gcov"
EXTRA_QMAKEVARS_PRE_append = " CONFIG+=insignificant_test"

FILES_${PN}_append = " ${OE_QMAKE_PATH_TESTS}"

python qmake5test_do_checkcode() {
    bb.build.exec_func("shifttest_do_checkcode", d)
}

python qmake5test_do_test() {
    dd = d.createCopy()
    env = os.environ.copy()

    # To access the shared libraries of other packages
    env["LD_LIBRARY_PATH"] = dd.expand("${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}")

    # Configure QT test arguments
    env["QT_PLUGIN_PATH"] = dd.expand("${STAGING_DIR_TARGET}${OE_QMAKE_PATH_PLUGINS}")
    env["QML_IMPORT_PATH"] = dd.expand("${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}")
    env["QML2_IMPORT_PATH"] = dd.expand("${QML2_IMPORT_PATH}:${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}")
    env["TESTRUNNER"] = shiftutils_qemu_run_cmd(dd)
    env["TESTARGS"] = "-platform offscreen"

    configured = dd.getVar("SHIFT_REPORT_DIR", True)

    if configured:
        report_dir = dd.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        mkdirhier(report_dir, True)

        plain("Generating the test result report", dd)
        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir
        # Create QT test report files
        env["TESTARGS"] += " -xunitxml -o test_result.xml"

    for gcdaFile in find_files(d.getVar("B", True), "*.gcda"):
        bb.utils.remove(gcdaFile)

    # Prepare for the coverage reports
    check_call(["lcov", "-c", "-i",
                "-d", dd.getVar("B", True),
                "-o", dd.expand("${B}/coverage_base.info"),
                "--ignore-errors", "gcov",
                "--gcov-tool", dd.expand("${TARGET_PREFIX}gcov"),
                "--rc", "lcov_branch_coverage=1"], dd)

    try:
        timeout(exec_proc, "make --quiet check", dd, env=env, cwd=dd.getVar("B", True))
    except bb.process.ExecutionError as e:
        if e.exitcode == 124:
            raise e
        pass

    if configured:
        if os.path.exists(report_dir):
            # Prepend the package name to each of the classname tags for GTest reports
            xml_files = find_files(report_dir, "*.xml")
            replace_files(xml_files, 'classname="', dd.expand('classname="${PN}.'))

            # Prepend the package name to each of the testsuite tags for QTest reports
            xml_files = find_files(dd.getVar("B", True), "test_result.xml")
            replace_files(xml_files, '(<testsuite.*name=")', dd.expand('\g<1>${PN}.'))

            # Copy QTest reports to the report directory
            for xml_file in xml_files:
                rel_path = os.path.relpath(xml_file, dd.getVar("B", True))
                new_path = os.path.join(report_dir, rel_path)
                bb.utils.mkdirhier(os.path.dirname(new_path))
                bb.utils.copyfile(xml_file, new_path)
        else:
            warn("No test report files found at %s" % report_dir, dd)
}

python qmake5test_do_coverage() {
    bb.build.exec_func("shifttest_do_coverage", d)
}

python qmake5test_do_checktest() {
    bb.build.exec_func("shifttest_do_checktest", d)
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest
