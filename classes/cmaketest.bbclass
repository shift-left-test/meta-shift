inherit cmake
inherit shifttest

DEPENDS_prepend = "\
    gtest \
    gmock \
    cppcheck-native \
    cpplint-native \
    "

OECMAKE_C_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"
OECMAKE_CXX_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"

EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=ON"
EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${TUNE_ARCH};-L;${STAGING_DIR_TARGET}'"

cmaketest_do_test() {
    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        local OUTPUT_DIR="${TEST_RESULT_OUTPUT}/${PF}"
        export GTEST_OUTPUT="xml:${OUTPUT_DIR}/"
        rm -rf "${OUTPUT_DIR}"
    fi

    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
    cmake --build ${B} --target test -- ARGS="--output-on-failure" | shifttest_print_lines

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
}

cmaketest_do_coverage() {
    shifttest_do_coverage
}

cmaketest_do_doc() {
    shifttest_do_doc
}

EXPORT_FUNCTIONS do_test do_coverage do_doc
