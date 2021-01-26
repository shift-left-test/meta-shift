inherit cmake
inherit shifttest
inherit shiftutils

OECMAKE_C_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"
OECMAKE_CXX_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"

EXTRA_OECMAKE_append = " -DCMAKE_CROSSCOMPILING_EMULATOR='${@shiftutils_qemu_cmake_emulator(d)}'"
EXTRA_OECMAKE_append = " -DCMAKE_EXPORT_COMPILE_COMMANDS=ON"

cmake_do_compile_prepend() {
    export TARGET_SYS="${TARGET_SYS}"
}

python cmaketest_do_checkcode() {
    bb.build.exec_func("shifttest_do_checkcode", d)
}

# $1 : print stdout if "PRINT"
# $2 : report save path
cmaketest_run_test() {
    PRINT_LINES=$1
    OUTPUT_DIR=$2
    TIMEOUT_STATUS=0

    if [ ! -z "${OUTPUT_DIR}" ]; then
        shifttest_prepare_output_dir ${OUTPUT_DIR}
    fi
    shifttest_prepare_env

    cd ${B}
    if [ "${PRINT_LINES}" = "PRINT" ]; then
        echo "Running tests..." | shifttest_print_lines
        timeout ${TEST_TIMEOUT} ctest --output-on-failure | shifttest_print_lines

        if [ "${PIPESTATUS[0]}" = "124" ]; then
            TIMEOUT_STATUS=1
            echo "Test timeout after ${TEST_TIMEOUT} ..." | shifttest_print_lines
        fi
    else
        echo "Running tests..." | shifttest_print_lines
        local TEST_EXIT_CODE=0
        timeout ${TEST_TIMEOUT} ctest --output-on-failure || TEST_EXIT_CODE=$?

        if [ "$TEST_EXIT_CODE" = "124" ]; then
            TIMEOUT_STATUS=1
        fi
    fi
}

python cmaketest_do_test() {
    dd = d.createCopy()
    env = os.environ.copy()

    # To access the shared libraries of other packages
    env["LD_LIBRARY_PATH"] = dd.expand("${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}")

    configured = dd.getVar("TEST_REPORT_OUTPUT", True)

    if configured:
        report_dir = dd.expand("${TEST_REPORT_OUTPUT}/${PF}/test")
        if os.path.exists(report_dir):
            bb.debug(2, "Removing the existing test report directory: %s" % report_dir)
            bb.utils.remove(report_dir, True)
        bb.utils.mkdirhier(report_dir)

        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir

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

    plain("Running tests...", dd)
    exec_proc("ctest --output-on-failure", dd, env=env, cwd=d.getVar("B", True))

    if configured:
        if os.path.exists(report_dir):
            # Prepend the package name to each of the classname tags for GTest reports
            xml_files = find_files(report_dir, "*.xml")
            replace_files(xml_files, 'classname="', d.expand('classname="${PN}.'))
        else:
            warn("No test report files found at %s" % report_dir, dd)
}

python cmaketest_do_coverage() {
    bb.build.exec_func("shifttest_do_coverage", d)
}

cmaketest_do_checktest() {
    if [ ! -z "${CHECKTEST_DISABLED}" ]; then
        bbfatal ${CHECKTEST_DISABLED}
    fi

    shifttest_checktest_prepare
    cmaketest_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ORIGINAL}

    shifttest_checktest_populate
    cat ${CHECKTEST_WORKDIR}/mutables.db | while read line
    do
        shifttest_checktest_mutate "${line}"
        TEST_STATE="success"
        cd ${B} && do_compile && do_install || TEST_STATE="build_failure"
        if [ "${TEST_STATE}" = "success" ]; then
            rm -rf ${CHECKTEST_WORKDIR_ACTUAL}/*
            cmaketest_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ACTUAL}
            if [ "$TIMEOUT_STATUS" = "1" ]; then
                TEST_STATE="timeout"
            fi
        else
            bbdebug 1 "build failed"
        fi
        shifttest_checktest_evaluate "${line}" "${TEST_STATE}"
        shifttest_checktest_restore_from_backup
        unset TEST_STATE
    done

    shifttest_checktest_report

    # restore original build
    shifttest_checktest_build
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest
