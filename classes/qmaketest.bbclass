inherit cpptest


EXTRA_QMAKEVARS_PRE:append:class-target = " CONFIG+=gcov"
EXTRA_QMAKEVARS_PRE:append:class-target = " ${@'CONFIG+=insignificant_test' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_SUPPRESS_FAILURES')) else ''}"

FILES:${PN}:append:class-target = " ${OE_QMAKE_PATH_TESTS}"


qmaketest_do_test() {
    local REPORT_DIR=""

    export QT_PLUGIN_PATH="${STAGING_DIR_TARGET}${OE_QMAKE_PATH_PLUGINS}"
    export QML_IMPORT_PATH="${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}"
    export QML2_IMPORT_PATH="${QML2_IMPORT_PATH}:${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}"
    export QT_QPA_PLATFORM="offscreen"
    export TESTRUNNER="${@shiftutils_qemu_run_cmd(d)}"

    if ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_SHUFFLE')) else 'false'}; then
        export GTEST_SHUFFLE=1
    fi

    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        REPORT_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
        rm -rf "${REPORT_DIR}"
        mkdir -p "${REPORT_DIR}"

        ${@save_metadata(d) or ''}

        bbplain "${PF} do_${BB_CURRENTTASK}: Generating the test result report"
        export GTEST_OUTPUT="xml:${REPORT_DIR}/"
        export TESTARGS=" -o -,txt -o test_result.xml,junitxml"
    fi

    cpptest_reset_coverage_counters

    if [ -n "${SHIFT_TEST_FILTER}" ]; then
        export GTEST_FILTER="${SHIFT_TEST_FILTER}"
    fi

    local TEST_RC=0
    ( cd "${B}" && make --quiet check ) 2>&1 | shiftutils_stream_plain
    TEST_RC=${PIPESTATUS[0]}

    shifttest_handle_test_rc ${TEST_RC} "make check"

    if [ -n "${REPORT_DIR}" ] && [ -d "${REPORT_DIR}" ]; then
        cpptest_prefix_xml_classnames "${REPORT_DIR}"

        # Match testsuite's *first* attribute `name="..."` only: [^>]* would
        # be greedy and land on hostname=, which already contains `${PN}.` in
        # QTest output. Then copy each XML into REPORT_DIR preserving paths.
        find "${B}" -name 'test_result.xml' | while read -r f; do
            sed -E -i "s|(<testsuite[[:space:]]+name=\")(${PN}\.)?|\1${PN}.|g" "${f}"
            rel=$(realpath --relative-to="${B}" "${f}")
            mkdir -p "${REPORT_DIR}/$(dirname "${rel}")"
            cp "${f}" "${REPORT_DIR}/${rel}"
        done
    fi
}

qmaketest_do_coverage() {
    cpptest_do_coverage
}

qmaketest_do_checktest() {
    cpptest_do_checktest
}

EXPORT_FUNCTIONS do_test do_coverage do_checktest
