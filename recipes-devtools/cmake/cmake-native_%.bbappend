# CMakeUtils
# SRC_URI: http://mod.lge.com/hub/yocto/addons/CMakeUtils
# SRCREV: e191e00fdde28612e0232fafdec29224839b4bfe

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
    file://0001-fix-clang-tidy-failure-by-target-option.patch \
    file://CMakeUtils.cmake \
    file://FindGMock.cmake \
"

do_install_append() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}
