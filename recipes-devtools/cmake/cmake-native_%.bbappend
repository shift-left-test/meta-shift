FILESEXTRAPATHS_prepend := "${THISDIR}/cmake:"

SRC_URI_append = " \
    file://CMakeUtils.cmake \
    file://FindGMock.cmake \
"

do_install_append() {
    mkdir -p ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules
    install -m 644 ${WORKDIR}/CMakeUtils.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
    install -m 644 ${WORKDIR}/FindGMock.cmake ${D}${datadir}/cmake-${CMAKE_MAJOR_VERSION}/Modules/
}
