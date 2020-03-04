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

EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${HOST_ARCH};-L;${STAGING_DIR_TARGET}'"

do_test() {
    bbnote "Run tests"
    cmake --build '${B}' --target test
}

addtask test after do_package before do_packagedata


do_install_append() {
    bbnote "Install test files"
    mkdir -p ${D}/opt/tests/${PN}
    
    for i in `find ${B}/ -type f -regex '.*[tT]est'`; do
      install -m 0755 ${i} ${D}/opt/tests/${PN}
    done
}
