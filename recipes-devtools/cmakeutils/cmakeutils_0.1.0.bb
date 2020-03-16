SUMMARY = "CMakeUtils - A set of CMake macro extensions for a C/C++ project"
DESCRIPTION = "A set of CMake macro extensions for a C/C++ project"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "http://mod.lge.com/hub/yocto/CMakeUtils"
BUGTRACKER = "http://mod.lge.com/hub/yocto/CMakeUtils/issues"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e5b34fb28d5adc2108f3317d97f59937"

SRC_URI = "git://mod.lge.com/hub/yocto/CMakeUtils.git;protocol=http;tag=${PV};nobranch=1"

S = "${WORKDIR}/git"

DEPENDS = "cmake"

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
    mkdir -p ${D}${SDKPATHNATIVE}/environment-setup.d
    echo "export CROSSCOMPILING_EMULATOR=qemu-${TARGET_ARCH}" > ${WORKDIR}/git/scripts/CMakeUtils.sh
    install -m 644 ${WORKDIR}/git/scripts/CMakeUtils.sh ${D}${SDKPATHNATIVE}/environment-setup.d/
}

FILES_${PN} = "\
    ${datadir} \
    ${SDKPATHNATIVE}/environment-setup.d/ \
    "

BBCLASSEXTEND = "native nativesdk"
