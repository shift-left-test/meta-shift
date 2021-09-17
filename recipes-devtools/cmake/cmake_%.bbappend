# CMakeUtils
# SRC_URI: http://mod.lge.com/hub/yocto/CMakeUtils
# SRCREV: 1d8aeafaafb504ab30ef5708479d749bfc6b74eb

inherit shiftutils

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append_class-nativesdk = " \
    file://CMakeUtils.cmake \
    file://FindGMock.cmake \
"

do_install_append_class-nativesdk() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/

    echo "SET(CMAKE_CROSSCOMPILING_EMULATOR \"${@shiftutils_qemu_cmake_emulator_sdktarget(d)}\")" > ${WORKDIR}/crosscompiling_emulator.cmake
    install -d ${D}${datadir}/cmake/OEToolchainConfig.cmake.d
    install -m 644 ${WORKDIR}/crosscompiling_emulator.cmake ${D}${datadir}/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake
}

FILES_${PN} += "${datadir}/cmake/OEToolchainConfig.cmake.d"
