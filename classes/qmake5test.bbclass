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

    configured = dd.getVar("TEST_REPORT_OUTPUT", True)

    if configured:
        report_dir = dd.expand("${TEST_REPORT_OUTPUT}/${PF}/test")
        bb.debug(2, "Flushing the test report directory: %s" % report_dir)
        bb.utils.remove(report_dir, True)
        bb.utils.mkdirhier(report_dir)

        plain("Generating the test result report", dd)
        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir
        # Create QT test report files
        env["TESTARGS"] += " -xunitxml -o test_result.xml"

    # Prepare for the coverage reports
    check_call("lcov -c -i " \
               "-d %s " \
               "-o %s " \
               "--ignore-errors %s " \
               "--gcov-tool %s " \
               "--rc %s" % (
                   dd.getVar("B", True),
                   dd.expand("${B}/coverage_base.info"),
                   "gcov",
                   dd.expand("${TARGET_PREFIX}gcov"),
                   "lcov_branch_coverage=1"), dd)

    exec_proc("make --quiet check", dd, env=env, cwd=dd.getVar("B", True))

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

EXPORT_FUNCTIONS do_checkcode do_test do_coverage

# Skip the RPATH sanity check since the QT 5.5 uses an absolute path for RPATH, which is
# prohibited by the yocto QA sanity checker. (This issue is fixed in QT 5.6)
INSANE_SKIP_${PN} += "rpaths"
