inherit cmake
inherit shifttest

DEPENDS_prepend = "\
    cppcheck-native \
    cpplint-native \
    "

OECMAKE_C_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"
OECMAKE_CXX_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"

EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${TUNE_ARCH};-L;${STAGING_DIR_TARGET}'"

cmaketest_do_test() {
    shifttest_prepare_output_dir
    shifttest_prepare_env
    cmake --build ${B} --target test -- ARGS="--output-on-failure" | shifttest_print_lines
    shifttest_gtest_update_xmls
}

cmaketest_do_coverage() {
    shifttest_do_coverage
}

cmaketest_do_doc() {
    shifttest_do_doc
}

EXPORT_FUNCTIONS do_test do_coverage do_doc
