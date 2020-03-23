inherit cmake

DEPENDS_prepend = "\
    gtest \
    gmock \
    cppcheck-native \
    cpplint-native \
    gcovr-native \
    qemu-native \
    doxygen-native \
    cmakeutils-native \
    "

EXTRA_OECMAKE += "-DCMAKE_BUILD_TYPE=DEBUG"
EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=ON"
EXTRA_OECMAKE += "-DCMAKE_INSTALL_TESTDIR=/opt/tests/${PF}"
EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${TUNE_ARCH};-L;${STAGING_DIR_TARGET}'"

addtask test after do_compile do_populate_sysroot
cmaketest_do_test() {
    if [ ! -z "${GTEST_OUTPUT}" ]; then
    export GTEST_OUTPUT="xml:${GTEST_OUTPUT}/${PF}/"
        for i in ${GTEST_OUTPUT}/${PF}/*.xml; do
            rm -f $i
        done
    fi
    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
    cmake --build ${B} --target test -- ARGS="--output-on-failure" |
    while read line; do
        bbplain "$line"
    done
}
do_test[nostamp] = "1"

addtask coverage after do_test
cmaketest_do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    if [ ! -z "${GCOVR_OUTPUT}" ]; then
        mkdir -p "${GCOVR_OUTPUT}/${PF}"
        gcovr -r ${WORKDIR} \
              --gcov-ignore-parse-errors \
              --xml "${GCOVR_OUTPUT}/${PF}/coverage.xml" \
              --html-details "${GCOVR_OUTPUT}/${PF}/coverage.html" \
              --json -o "${GCOVR_OUTPUT}/${PF}/coverage.json"
    fi
    gcovr -r ${WORKDIR} --gcov-ignore-parse-errors |
    while read line; do
        bbplain "$line"
    done
}
do_coverage[nostamp] = "1"

FILES_${PN} += "/opt/tests/${PF}"

EXPORT_FUNCTIONS do_test do_coverage
