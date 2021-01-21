inherit qmake5
inherit shifttest
inherit shiftutils

EXTRA_QMAKEVARS_PRE_append = " CONFIG+=gcov"
EXTRA_QMAKEVARS_PRE_append = " CONFIG+=insignificant_test"

FILES_${PN}_append = " ${OE_QMAKE_PATH_TESTS}"

python qmake5test_do_checkcode() {
    bb.build.exec_func("shifttest_do_checkcode", d)
}

qmake5test_qtest_update_xmls() {
    [ -z "${TEST_REPORT_OUTPUT}" ] && return
    find * -name "test_result.xml" \
      -exec sed -r -i 's|(<testsuite.*name=")(.*")|\1${PN}\.\2|g' {} \; \
      -exec install -m 644 -D "{}" "${TEST_REPORT_OUTPUT}/${PF}/test/{}" \;
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

qmake5test_do_test() {
    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        qmake5test_run_test "PRINT" ${TEST_REPORT_OUTPUT}/${PF}/test
        shifttest_gtest_update_xmls
        qmake5test_qtest_update_xmls
        shifttest_check_output_dir
    else
        qmake5test_run_test "PRINT"
    fi
}

qmake5test_do_coverage() {
    shifttest_do_coverage
}

qmake5test_do_checktest() {
    if [ ! -z "${CHECKTEST_DISABLED}" ]; then
        bbfatal ${CHECKTEST_DISABLED}
    fi

    shifttest_checktest_prepare
    qmake5test_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ORIGINAL}

    shifttest_checktest_populate
    cat ${CHECKTEST_WORKDIR}/mutables.db | while read line
    do
        shifttest_checktest_mutate "${line}"
        TEST_STATE="success"
        cd ${B} && do_compile && do_install || TEST_STATE="build_failure"
        if [ "${TEST_STATE}" = "success" ]; then
            rm -rf ${CHECKTEST_WORKDIR_ACTUAL}/*
            qmake5test_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ACTUAL}
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
