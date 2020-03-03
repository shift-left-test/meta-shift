DEPENDS_prepend = "\
    googletest \
    cppcheck-native \
    cpplint-native \
    gcovr-native \
    qemu-native \
    "

do_test() {
    cd ${B}

    ctest --debug
}

addtask test after do_build

EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${HOST_ARCH};-L;${RECIPE_SYSROOT}'"