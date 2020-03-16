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
EXTRA_OECMAKE += "-DCMAKE_INSTALL_TESTDIR=/opt/tests/${PN}"
EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${TARGET_ARCH};-L;${STAGING_DIR_TARGET}'"

addtask test after do_compile do_populate_sysroot
cmaketest_do_test() {
    export GTEST_OUTPUT="${GTEST_OUTPUT}/${PN}/"
    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
    cmake --build '${B}' --target test
}
do_test[nostamp] = "1"

addtask coverage after do_test
cmaketest_do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    gcovr -r ${WORKDIR}
}
do_coverage[nostamp] = "1"

FILES_${PN} += "/opt/tests/${PN}"

EXPORT_FUNCTIONS do_test do_coverage
