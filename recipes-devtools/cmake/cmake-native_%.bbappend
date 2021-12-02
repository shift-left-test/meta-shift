# CMakeUtils
# SRC_URI: http://mod.lge.com/hub/yocto/CMakeUtils
# SRCREV: 1d8aeafaafb504ab30ef5708479d749bfc6b74eb

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " \
    file://CMakeUtils.cmake \
    file://FindGMock.cmake \
"

do_install:append() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}
