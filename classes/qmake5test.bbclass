inherit qmake5
inherit shifttest

DEPENDS_prepend = "\
    gtest \
    gmock \
    "

EXTRA_QMAKEVARS_PRE += "CONFIG+=gcov"
EXTRA_QMAKEVARS_PRE += "CONFIG+=insignificant_test"

FILES_${PN} += "${OE_QMAKE_PATH_TESTS}"

qmake5test_do_test() {
    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        local OUTPUT_DIR="${TEST_RESULT_OUTPUT}/${PF}"
        export GTEST_OUTPUT="xml:${OUTPUT_DIR}/"
        rm -rf "${OUTPUT_DIR}"
    fi

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

    local OUTPUT_DIR="${TEST_RESULT_OUTPUT}/${PF}"

    if [ ! -d "${OUTPUT_DIR}" ]; then
        bbwarn "No test report files generated at ${OUTPUT_DIR}"
        return
    fi

    for i in "${OUTPUT_DIR}/*.xml"; do
        sed -i "s|classname=\"|classname=\"${PN}.|g" $i
    done

    find * -name "test_result.xml" \
        -exec sed -r -i 's|(<testsuite.*name=")(.*")|\1${PN}\.\2|g' {} \; \
        -exec install -m 644 -D "{}" "${OUTPUT_DIR}/{}" \;
}

qmake5test_do_coverage() {
    shifttest_do_coverage
}

qmake5test_do_doc() {
    shifttest_do_doc
}

EXPORT_FUNCTIONS do_test do_coverage do_doc
