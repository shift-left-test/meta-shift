inherit cmake

DEPENDS_prepend = "\
    gtest \
    gmock \
    cppcheck-native \
    cpplint-native \
    gcovr-native \
    qemu-native \
    doxygen-native \
    cmake-native \
    "

EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=ON"
EXTRA_OECMAKE += "-DCMAKE_INSTALL_TESTDIR=/opt/tests/${PF}"
EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${TUNE_ARCH};-L;${STAGING_DIR_TARGET}'"

addtask test after do_compile do_populate_sysroot
cmaketest_do_test() {
    if [ ! -z "${GTEST_OUTPUT}" ]; then
        local OUTPUT_DIR="${GTEST_OUTPUT}/${PF}"
        export GTEST_OUTPUT="xml:${OUTPUT_DIR}/"
        if [ -d "${OUTPUT_DIR}" ]; then
            bbplain "Removing: ${OUTPUT_DIR}"
            rm -rf "${OUTPUT_DIR}"
        fi
    fi

    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
    cmake --build ${B} --target test -- ARGS="--output-on-failure" |
    while read line; do
        bbplain "$line"
    done

    if [ ! -z "${GTEST_OUTPUT}" ]; then
        local OUTPUT_DIR="${GTEST_OUTPUT}/${PF}"
        if [ ! -d "${OUTPUT_DIR}" ]; then
          bbwarn "No test report files generated at ${OUTPUT_DIR}"
          return
        fi
        for i in "${OUTPUT_DIR}/*.xml"; do
            sed -i "s|classname=\"|classname=\"${PN}.|g" $i
        done
    fi
}
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

addtask coverage after do_test
cmaketest_do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    if [ ! -z "${GCOVR_OUTPUT}" ]; then
        local OUTPUT_DIR="${GCOVR_OUTPUT}/${PF}"
        if [ -d "${OUTPUT_DIR}" ]; then
            bbplain "Removing: ${OUTPUT_DIR}"
            rm -rf "${OUTPUT_DIR}"
        fi
        mkdir -p "${OUTPUT_DIR}"
        gcovr -r ${WORKDIR} --gcov-ignore-parse-errors \
              --xml "${OUTPUT_DIR}/coverage.xml" \
              --html-details "${OUTPUT_DIR}/coverage.html"
    fi

    gcovr -r ${WORKDIR} --gcov-ignore-parse-errors |
    while read line; do
        bbplain "$line"
    done

    if [ ! -z "${GCOVR_OUTPUT}" ]; then
        local OUTPUT_DIR="${GCOVR_OUTPUT}/${PF}"
        if [ ! -f "${OUTPUT_DIR}/coverage.xml" ]; then
          bbwarn "No coverage report files generated at ${OUTPUT_DIR}"
          return
        fi
        sed -i "s|<package name=\"|<package name=\"${PN}.|g" "${OUTPUT_DIR}/coverage.xml"
    fi
}
do_coverage[nostamp] = "1"
do_coverage[doc] = "Measures code coverage metrics for the target"

FILES_${PN} += "/opt/tests/${PF}"

EXPORT_FUNCTIONS do_test do_coverage
