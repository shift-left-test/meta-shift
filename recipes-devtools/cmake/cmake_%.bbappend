# CMakeUtils
# SRC_URI: https://github.com/shift-left-test/CMakeUtils
# VERSION: 1.4.0

inherit shiftutils

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append:class-nativesdk = " \
    file://CMakeUtils.cmake \
    file://FindGMock.cmake \
    file://crosscompiling_emulator.cmake \
"

do_install:append:class-nativesdk() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/

    install -d ${D}${datadir}/cmake/OEToolchainConfig.cmake.d
    install -m 644 ${WORKDIR}/crosscompiling_emulator.cmake ${D}${datadir}/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake
}

FILES:${PN} += "${datadir}/cmake/OEToolchainConfig.cmake.d"
