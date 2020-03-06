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

do_coverage() {
    export GCOV=${TARGET_PREFIX}gcov
    gcovr -r ${WORKDIR} --gcov-ignore-parse-errors
}

addtask test after do_package
addtask coverage after do_package

do_install_append() {
    bbnote "Install test files"
    mkdir -p ${D}/opt/tests/${PN}
    
    for i in `find ${B}/ -type f -regex '.*[tT]est'`; do
      install -m 0755 ${i} ${D}/opt/tests/${PN}/
    done
}
