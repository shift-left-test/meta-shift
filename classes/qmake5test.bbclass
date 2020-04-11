inherit qmake5
inherit shifttest

EXTRA_QMAKEVARS_PRE += "CONFIG+=gcov"
EXTRA_QMAKEVARS_PRE += "CONFIG+=insignificant_test"

FILES_${PN} += "${OE_QMAKE_PATH_TESTS}"

qmake5test_do_test() {
    export QT_PLUGIN_PATH=${STAGING_DIR_TARGET}${libdir}/plugins
    export QML_IMPORT_PATH=${STAGING_DIR_TARGET}${libdir}/qml
    export QML2_IMPORT_PATH=$QML2_IMPORT_PATH:${STAGING_DIR_TARGET}${libdir}/qml

    export TESTRUNNER="qemu-${TUNE_ARCH} -L '${STAGING_DIR_TARGET}'"
    export TESTARGS="-platform offscreen"

    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        bbplain "Generating the test result report"
        export TESTARGS="${TESTARGS} -platform offscreen -xunitxml -o test_result.xml"
    fi

    cd ${B}

    make --quiet check | shifttest_print_lines

    if [ -z "${TEST_RESULT_OUTPUT}" ]; then
        return
    fi

    find * -name "test_result.xml" \
        -exec sed -r -i 's|(<testsuite.*name=")(.*")|\1${PN}\.\2|g' {} \; \
        -exec install -m 644 -D "{}" "${TEST_RESULT_OUTPUT}/${PF}/{}" \;
}

qmake5test_do_coverage() {
    shifttest_do_coverage
}

qmake5test_do_doc() {
    shifttest_do_doc
}

EXPORT_FUNCTIONS do_test do_coverage do_doc
