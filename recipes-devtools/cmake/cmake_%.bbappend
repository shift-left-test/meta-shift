FILESEXTRAPATHS_prepend := "${THISDIR}/cmake:"

SRC_URI_append_class-nativesdk = " \
    file://CMakeUtils.cmake \
    file://FindGMock.cmake \
"

do_install_append_class-nativesdk() {
    mkdir -p ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/

    echo "SET(CMAKE_CROSSCOMPILING_EMULATOR \"qemu-${TUNE_ARCH};-L;""$""ENV{SDKTARGETSYSROOT}\")" > ${WORKDIR}/crosscompiling_emulator.cmake
    mkdir -p ${D}${datadir}/cmake/OEToolchainConfig.cmake.d
    install -m 644 ${WORKDIR}/crosscompiling_emulator.cmake ${D}${datadir}/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake
}

FILES_${PN} += "${datadir}/cmake/OEToolchainConfig.cmake.d"
