# CMakeUtils
# SRC_URI: http://mod.lge.com/hub/yocto/addons/CMakeUtils
# SRCREV: e0a3dab882abd327c4930bb6b8060fb09b3f020f

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
