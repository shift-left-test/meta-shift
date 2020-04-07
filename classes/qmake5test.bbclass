inherit qmake5

DEPENDS_prepend = "\
    gcovr-native \
    qemu-native \
    doxygen-native \
    "

EXTRA_QMAKEVARS_PRE += "CONFIG+=gcov"

addtask test after do_compile do_populate_sysroot
qmake5test_do_test() {
    cd ${B}
    export QT_PLUGIN_PATH=${STAGING_DIR_TARGET}${libdir}/plugins
    export QML_IMPORT_PATH=${STAGING_DIR_TARGET}${libdir}/qml
    export QML2_IMPORT_PATH=$QML2_IMPORT_PATH:${STAGING_DIR_TARGET}${libdir}/qml

    export TESTRUNNER="qemu-${TUNE_ARCH} -L '${STAGING_DIR_TARGET}'"

    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        export TESTARGS="-platform offscreen -xunitxml -o test_result.xml"
    else
        export TESTARGS="-platform offscreen"
    fi

    make -k check |
    while read line; do
        bbplain "$line"
    done || true

    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        cd ${B}
        find * -name "test_result.xml" -exec install -m 644 -D "{}" "${TEST_RESULT_OUTPUT}/${PF}/{}" \;
    fi
}
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

addtask coverage after do_test
qmake5test_do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    if [ ! -z "${TEST_COVERAGE_OUTPUT}" ]; then
        local OUTPUT_DIR="${TEST_COVERAGE_OUTPUT}/${PF}"
        if [ -d "${OUTPUT_DIR}" ]; then
            bbplain "Removing: ${OUTPUT_DIR}"
            rm -rf "${OUTPUT_DIR}"
        fi
        mkdir -p "${OUTPUT_DIR}"
        gcovr -r ${WORKDIR} \
              --gcov-ignore-parse-errors \
              --xml "${OUTPUT_DIR}/coverage.xml" \
              --html "${OUTPUT_DIR}/coverage.html"
    fi

    gcovr -r ${WORKDIR} \
          --gcov-ignore-parse-errors |
    while read line; do
        bbplain "$line"
    done

    if [ ! -z "${GCOVR_OUTPUT}" ]; then
        local OUTPUT_DIR="${GCOVR_OUTPUT}/${PF}"
        sed -i "s|<package name=\"|<package name=\"${PN}.|g" "${OUTPUT_DIR}/coverage.xml"
    fi
}
do_coverage[nostamp] = "1"
do_coverage[doc] = "Measures code coverage metrics for the target"

FILES_${PN} += "${OE_QMAKE_PATH_TESTS}"

EXPORT_FUNCTIONS do_test do_coverage
