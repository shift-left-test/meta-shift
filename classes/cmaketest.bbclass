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

EXTRA_OECMAKE += "-DCMAKE_BUILD_TYPE=DEBUG"
EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=ON"
EXTRA_OECMAKE += "-DCMAKE_INSTALL_TESTDIR=/opt/tests/${PN}"
EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${TARGET_ARCH};-L;${STAGING_DIR_TARGET}'"

cmaketest_do_test() {
    cmake --build '${B}' --target test
}

addtask test after do_package

cmaketest_do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    gcovr -r ${WORKDIR} --gcov-ignore-parse-errors
}

addtask coverage after do_test

FILES_${PN} += "/opt/tests/${PN}"

EXPORT_FUNCTIONS do_test do_coverage
