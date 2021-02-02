inherit qmake5
inherit shifttest
inherit shiftutils

EXTRA_QMAKEVARS_PRE_append = " CONFIG+=gcov"
EXTRA_QMAKEVARS_PRE_append = " CONFIG+=insignificant_test"

FILES_${PN}_append = " ${OE_QMAKE_PATH_TESTS}"

python qmake5test_do_checkcode() {
    bb.build.exec_func("shifttest_do_checkcode", d)
}

# $1 : print stdout if "PRINT"
# $2 : report save path
qmake5test_run_test() {
    PRINT_LINES=$1
    OUTPUT_DIR=$2
    TIMEOUT_STATUS=0

    if [ ! -z "${OUTPUT_DIR}" ]; then
        shifttest_prepare_output_dir ${OUTPUT_DIR}
    fi
    shifttest_prepare_env

    export QT_PLUGIN_PATH=${STAGING_DIR_TARGET}${OE_QMAKE_PATH_PLUGINS}
    export QML_IMPORT_PATH=${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}
    export QML2_IMPORT_PATH=$QML2_IMPORT_PATH:${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}

    export TESTRUNNER="${@shiftutils_qemu_run_cmd(d)}"
    export TESTARGS="-platform offscreen"

    if [ ! -z "${OUTPUT_DIR}" ]; then
        bbplain "${PF} do_${BB_CURRENTTASK}: Generating the test result report"
        export TESTARGS="${TESTARGS} -platform offscreen -xunitxml -o test_result.xml"
    fi

    cd ${B}
    local TEST_EXIT_CODE=0
    if [ "${PRINT_LINES}" = "PRINT" ]; then
        timeout ${TEST_TIMEOUT} make --quiet check | shifttest_print_lines
        TEST_EXIT_CODE=${PIPESTATUS[0]}
    else
        timeout ${TEST_TIMEOUT} make --quiet check || TEST_EXIT_CODE=$?
    fi

    if [ "$TEST_EXIT_CODE" = "124" ]; then
        TIMEOUT_STATUS=1
        if [ "${PRINT_LINES}" = "PRINT" ]; then
            echo "Test timeout after ${TEST_TIMEOUT} ..." | shifttest_print_lines
        fi
    fi
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

    try:
        exec_proc("make --quiet check", dd, env=env, cwd=dd.getVar("B", True))
    except bb.process.ExecutionError:
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

# qmake5test_do_checktest() {
#     if [ ! -z "${CHECKTEST_DISABLED}" ]; then
#         bbfatal ${CHECKTEST_DISABLED}
#     fi
#
#     shifttest_checktest_prepare
#     qmake5test_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ORIGINAL}
#
#     shifttest_checktest_populate
#     cat ${CHECKTEST_WORKDIR}/mutables.db | while read line
#     do
#         shifttest_checktest_mutate "${line}"
#         TEST_STATE="success"
#         cd ${B} && do_compile && do_install || TEST_STATE="build_failure"
#         if [ "${TEST_STATE}" = "success" ]; then
#             rm -rf ${CHECKTEST_WORKDIR_ACTUAL}/*
#             qmake5test_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ACTUAL}
#             if [ "$TIMEOUT_STATUS" = "1" ]; then
#               TEST_STATE="timeout"
#             fi
#         else
#             bbdebug 1 "build failed"
#         fi
#         shifttest_checktest_evaluate "${line}" "${TEST_STATE}"
#         shifttest_checktest_restore_from_backup
#         unset TEST_STATE
#     done
#
#     shifttest_checktest_report
#
#     # restore original build
#     shifttest_checktest_build
# }

python qmake5test_do_checktest() {
    bb.build.exec_func("shifttest_do_checktest", d)
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest
