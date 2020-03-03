DEPENDS_prepend = "\
    gtest \
    gmock \
    cppcheck-native \
    cpplint-native \
    gcovr-native \
    qemu-native \
    "

do_test() {
    cd ${B}
    ctest --output-on-failure
}

addtask test after do_build

EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${HOST_ARCH};-L;${STAGING_DIR_TARGET}'"
