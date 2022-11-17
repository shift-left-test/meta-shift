SUMMARY = "gcovr"
DESCRIPTION = "generate code coverage reports with gcc/gcov"
AUTHOR = "gcovr authors"
HOMEPAGE = "https://github.com/gcovr/gcovr"
BUGTRACKER = "https://github.com/gcovr/gcovr/issues"
SECTION = "devel"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=e59af597b3484fa3b52c0fbfd5d17611"

PYPI_PACKAGE = "gcovr"

DEPENDS += "\
    ${PYTHON_PN}-jinja2 \
    ${PYTHON_PN}-lxml \
    ${PYTHON_PN}-markupsafe \
    ${PYTHON_PN}-pygments \
"

SRC_URI[md5sum] = "d4bc4239231218193834538ce6335274"
SRC_URI[sha256sum] = "217195085ec94346291a87b7b1e6d9cfdeeee562b3e0f9a32b25c9530b3bce8f"

inherit pypi setuptools3

FILES:${PN}:append:class-nativesdk = " ${SDKPATHNATIVE}"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-jinja2 \
    ${PYTHON_PN}-lxml \
    ${PYTHON_PN}-markupsafe \
    ${PYTHON_PN}-pygments \
    ${PYTHON_PN}-setuptools \
"

do_install:append:class-nativesdk() {
    echo "export GCOV=""$""{TARGET_PREFIX}gcov" > ${WORKDIR}/gcovr.sh
    install -d ${D}${SDKPATHNATIVE}/environment-setup.d
    install -m 644 ${WORKDIR}/gcovr.sh ${D}${SDKPATHNATIVE}/environment-setup.d/gcovr.sh
}

BBCLASSEXTEND = "native nativesdk"
