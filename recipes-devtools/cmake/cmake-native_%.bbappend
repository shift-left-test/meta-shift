# CMakeUtils
# SRC_URI: http://mod.lge.com/hub/yocto/addons/CMakeUtils
# SRCREV: 03d482bc80df7ad737e0cbd19c08bc8f0856e0e8

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
    file://CMakeUtils.cmake \
    file://FindGMock.cmake \
"

do_install_append() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}
