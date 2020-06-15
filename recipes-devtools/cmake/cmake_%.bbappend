SRC_URI_append_class-nativesdk = " git://mod.lge.com/hub/yocto/addons/CMakeUtils.git;protocol=http;nobranch=1;name=cmakeutils;destsuffix=cmakeutils"

SRCREV_cmakeutils = "12a1d74661e824bf5ff90d3e2839555126de1961"

do_install_append_class-nativesdk() {
    QEMU_BIN_NAME="${@d.getVar('QB_SYSTEM_NAME', True).replace('-system', '')}"

    install -d ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/cmakeutils/scripts/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/cmakeutils/scripts/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/

    echo "SET(CMAKE_CROSSCOMPILING_EMULATOR \"${QEMU_BIN_NAME};-L;""$""ENV{SDKTARGETSYSROOT};-E;LD_LIBRARY_PATH=""$""ENV{LD_LIBRARY_PATH}:""$""ENV{SDKTARGETSYSROOT}/${baselib}\")" > ${WORKDIR}/crosscompiling_emulator.cmake
    install -d ${D}${datadir}/cmake/OEToolchainConfig.cmake.d
    install -m 644 ${WORKDIR}/crosscompiling_emulator.cmake ${D}${datadir}/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake
}

FILES_${PN} += "${datadir}/cmake/OEToolchainConfig.cmake.d"
