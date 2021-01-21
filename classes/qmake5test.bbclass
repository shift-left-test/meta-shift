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

qmake5test_do_test() {
    shifttest_prepare_output_dir
    shifttest_prepare_env

    export QT_PLUGIN_PATH=${STAGING_DIR_TARGET}${OE_QMAKE_PATH_PLUGINS}
    export QML_IMPORT_PATH=${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}
    export QML2_IMPORT_PATH=$QML2_IMPORT_PATH:${STAGING_DIR_TARGET}${OE_QMAKE_PATH_QML}

    export TESTRUNNER="${@shiftutils_qemu_run_cmd(d)}"
    export TESTARGS="-platform offscreen"

    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        bbplain "Generating the test result report"
        export TESTARGS="${TESTARGS} -platform offscreen -xunitxml -o test_result.xml"
    fi

    cd ${B}
    make --quiet check | shifttest_print_lines

    shifttest_gtest_update_xmls
    qmake5test_qtest_update_xmls
    shifttest_check_output_dir
}

qmake5test_do_coverage() {
    shifttest_do_coverage
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage
