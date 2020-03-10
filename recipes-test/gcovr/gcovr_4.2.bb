SUMMARY = "gcovr"
DESCRIPTION = "generate code coverage reports with gcc/gcov"
AUTHOR = "gcovr authors"
HOMEPAGE = "https://github.com/gcovr/gcovr"
BUGTRACKER = "https://github.com/gcovr/gcovr/issues"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=221e634a1ceafe02ef74462cbff2fb16"

SRC_URI = "git://github.com/gcovr/gcovr.git;protocol=https;tag=${PV};nobranch=1"

S = "${WORKDIR}/git"

inherit setuptools

DEPENDS += "\
    ${PYTHON_PN}-pytest-runner \
    ${PYTHON_PN}-jinja2 \
    ${PYTHON_PN}-lxml \
    ${PYTHON_PN}-markupsafe \
    ${PYTHON_PN}-setuptools \
"

RDEPENDS_${PN}_class-nativesdk += "\
    nativesdk-${PYTHON_PN}-jinja2 \
    nativesdk-${PYTHON_PN}-lxml \
    nativesdk-${PYTHON_PN}-markupsafe \
    nativesdk-${PYTHON_PN}-setuptools \
"

BBCLASSEXTEND = "native nativesdk"
