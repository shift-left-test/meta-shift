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

addtask test after do_compile do_populate_sysroot
cmaketest_do_test[nostamp] = "1"
cmaketest_do_test() {
    export GTEST_OUTPUT="${GTEST_OUTPUT}/${PN}/"
    cmake --build '${B}' --target test
}

addtask coverage after do_test
cmaketest_do_coverage[nostamp] = "1"
cmaketest_do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    gcovr -r ${WORKDIR}
}

FILES_${PN} += "/opt/tests/${PN}"

EXPORT_FUNCTIONS do_test do_coverage
