SUMMARY = "gcovr"
DESCRIPTION = "generate code coverage reports with gcc/gcov"
AUTHOR = "gcovr authors"
HOMEPAGE = "https://github.com/gcovr/gcovr"
BUGTRACKER = "https://github.com/gcovr/gcovr/issues"
SECTION = "devel"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=221e634a1ceafe02ef74462cbff2fb16"

PYPI_PACKAGE = "gcovr"

DEPENDS += "\
    ${PYTHON_PN}-jinja2 \
    ${PYTHON_PN}-lxml \
    ${PYTHON_PN}-markupsafe \
"

SRC_URI[md5sum] = "83f75d78d59cbd8a34275a372a47f557"
SRC_URI[sha256sum] = "5aae34dc81e51600cfecbbbce3c3a80ce3f7548bc0aa1faa4b74ecd18f6fca3f"

inherit pypi setuptools

FILES_${PN}_append_class-nativesdk = " ${SDKPATHNATIVE}"

RDEPENDS_${PN} += "\
    ${PYTHON_PN}-jinja2 \
    ${PYTHON_PN}-lxml \
    ${PYTHON_PN}-markupsafe \
    ${PYTHON_PN}-setuptools \
"

do_install_append_class-native() {
    if test -e ${D}${bindir} ; then
        for i in ${D}${bindir}/* ; do \
            sed -i -e s:${bindir}/python-native/python:${USRBINPATH}/env\ nativepython:g $i
        done
    fi
}

do_install_append_class-nativesdk() {
    echo "export GCOV=""$""{TARGET_PREFIX}gcov" > ${WORKDIR}/gcovr.sh
    install -d ${D}${SDKPATHNATIVE}/environment-setup.d
    install -m 644 ${WORKDIR}/gcovr.sh ${D}${SDKPATHNATIVE}/environment-setup.d/gcovr.sh
}

BBCLASSEXTEND = "native nativesdk"
