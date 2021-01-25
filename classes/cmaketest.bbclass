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

cmaketest_do_test() {
    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        cmaketest_run_test "PRINT" ${TEST_REPORT_OUTPUT}/${PF}/test
        shifttest_gtest_update_xmls
        shifttest_check_output_dir
    else
        cmaketest_run_test "PRINT"
    fi
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
