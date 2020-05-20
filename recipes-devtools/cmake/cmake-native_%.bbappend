SRC_URI_append_class-native = " git://mod.lge.com/hub/yocto/CMakeUtils.git;protocol=http;tag=1.0.0;nobranch=1;destsuffix=cmakeutils"

do_install_append() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/cmakeutils/scripts/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/cmakeutils/scripts/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}
