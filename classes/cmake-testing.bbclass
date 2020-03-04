DEPENDS_prepend = "\
    gtest \
    gmock \
    cppcheck-native \
    cpplint-native \
    gcovr-native \
    qemu-native \
    doxygen-native \
    "

EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${HOST_ARCH};-L;${STAGING_DIR_TARGET}'"

do_test() {
    bbnote "Running tests"
    cmake --build '${B}' --target test
}

addtask test after do_package before do_packagedata
