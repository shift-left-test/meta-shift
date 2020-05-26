SRC_URI_append_class-native = " git://mod.lge.com/hub/yocto/addons/CMakeUtils.git;protocol=http;nobranch=1;name=cmakeutils;destsuffix=cmakeutils"

SRCREV_cmakeutils = "12a1d74661e824bf5ff90d3e2839555126de1961"

do_install_append() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/cmakeutils/scripts/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/cmakeutils/scripts/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}
