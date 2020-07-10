SRC_URI_append_class-native = " git://mod.lge.com/hub/yocto/addons/CMakeUtils.git;protocol=http;name=cmakeutils;destsuffix=cmakeutils"

SRCREV_cmakeutils = "e191e00fdde28612e0232fafdec29224839b4bfe"

do_install_append() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/cmakeutils/scripts/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/cmakeutils/scripts/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}
