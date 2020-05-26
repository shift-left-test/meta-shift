SRC_URI_append_class-nativesdk = " git://mod.lge.com/hub/yocto/addons/CMakeUtils.git;protocol=http;tag=1.0.0;nobranch=1;destsuffix=cmakeutils"

do_install_append_class-nativesdk() {
    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/cmakeutils/scripts/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/cmakeutils/scripts/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/

    echo "SET(CMAKE_CROSSCOMPILING_EMULATOR \"qemu-${TUNE_ARCH};-L;""$""ENV{SDKTARGETSYSROOT}\")" > ${WORKDIR}/crosscompiling_emulator.cmake
    install -d ${D}${datadir}/cmake/OEToolchainConfig.cmake.d
    install -m 644 ${WORKDIR}/crosscompiling_emulator.cmake ${D}${datadir}/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake
}

FILES_${PN} += "${datadir}/cmake/OEToolchainConfig.cmake.d"
