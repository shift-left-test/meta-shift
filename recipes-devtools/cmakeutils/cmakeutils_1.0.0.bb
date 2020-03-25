SUMMARY = "CMakeUtils - A set of CMake macro extensions for a C/C++ project"
DESCRIPTION = "A set of CMake macro extensions for a C/C++ project"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "http://mod.lge.com/hub/yocto/CMakeUtils"
BUGTRACKER = "http://mod.lge.com/hub/yocto/CMakeUtils/issues"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e5b34fb28d5adc2108f3317d97f59937"

SRC_URI = "git://mod.lge.com/hub/yocto/CMakeUtils.git;protocol=http;tag=${PV};nobranch=1"

S = "${WORKDIR}/git"

DEPENDS = "cmake-native"

do_configure[noexec] = "1"
do_compile[noexec] = "1"

do_install() {
    eval "$(cmake --system-information |sed -n 's/^CMAKE_ROOT /CMAKE_ROOT=/p')"
    CMAKE_MAJOR_VERSION="${CMAKE_ROOT##*cmake-}"

    mkdir -p ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/git/scripts/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/git/scripts/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}

do_install_append_class-nativesdk() {
    echo "SET(CMAKE_CROSSCOMPILING_EMULATOR \"qemu-${TUNE_ARCH};-L;""$""ENV{SDKTARGETSYSROOT}\")" > ${WORKDIR}/crosscompiling_emulator.cmake
    mkdir -p ${D}${datadir}/cmake/OEToolchainConfig.cmake.d
    install -m 644 ${WORKDIR}/crosscompiling_emulator.cmake ${D}${datadir}/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake
}

FILES_${PN} = "\
    ${datadir} \
    "

BBCLASSEXTEND = "native nativesdk"
