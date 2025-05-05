inherit shiftutils

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append:class-nativesdk = " \
    file://crosscompiling_emulator.cmake \
"

do_install:append:class-nativesdk() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -d ${D}${datadir}/cmake/OEToolchainConfig.cmake.d
    install -m 644 ${WORKDIR}/crosscompiling_emulator.cmake ${D}${datadir}/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake
}

FILES:${PN} += "${datadir}/cmake/OEToolchainConfig.cmake.d"
