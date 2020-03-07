inherit cmake

DEPENDS_prepend = "\
    gtest \
    gmock \
    cppcheck-native \
    cpplint-native \
    gcovr-native \
    qemu-native \
    doxygen-native \
    "

EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=ON"
EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${HOST_ARCH};-L;${STAGING_DIR_TARGET}'"

cmaketest_do_test() {
    bbnote "Run tests"
    cmake --build '${B}' --target test
}

cmaketest_do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    gcovr -r ${WORKDIR} --gcov-ignore-parse-errors
}

addtask test after do_package
addtask coverage after do_package

EXPORT_FUNCTIONS do_test do_coverage
