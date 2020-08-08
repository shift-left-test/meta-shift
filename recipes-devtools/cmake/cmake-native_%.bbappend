# CMakeUtils
# SRC_URI: http://mod.lge.com/hub/yocto/addons/CMakeUtils
# SRCREV: 412b8559d829b984836bcd803df052efa065d4b5

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
