SUMMARY = "gcovr"
DESCRIPTION = "generate code coverage reports with gcc/gcov"
AUTHOR = "gcovr authors"
HOMEPAGE = "https://github.com/gcovr/gcovr"
BUGTRACKER = "https://github.com/gcovr/gcovr/issues"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=221e634a1ceafe02ef74462cbff2fb16"

inherit pypi setuptools

PYPI_PACKAGE = "gcovr"

SRC_URI[md5sum] = "83f75d78d59cbd8a34275a372a47f557"
SRC_URI[sha256sum] = "5aae34dc81e51600cfecbbbce3c3a80ce3f7548bc0aa1faa4b74ecd18f6fca3f"

DEPENDS += "\
    ${PYTHON_PN}-jinja2 \
    ${PYTHON_PN}-lxml \
    ${PYTHON_PN}-markupsafe \
"

RDEPENDS_${PN} += "\
    ${PYTHON_PN}-setuptools \
    ${PYTHON_PN}-jinja2 \
    ${PYTHON_PN}-lxml \
    ${PYTHON_PN}-markupsafe \
"

do_install_append_class-nativesdk() {
    # To fix the nativesdk recipe shebang path bug of distutils for Yocto morty
    for i in ${D}${bindir}/* ; do
        sed -i -e s:${bindir}/env:${USRBINPATH}/env:g $i
    done

    echo "export GCOV=""$""{TARGET_PREFIX}gcov" > ${WORKDIR}/gcovr.sh
    mkdir -p ${D}${SDKPATHNATIVE}/environment-setup.d/
    install -m 644 ${WORKDIR}/gcovr.sh ${D}${SDKPATHNATIVE}/environment-setup.d/gcovr.sh
}

FILES_${PN}_append_class-nativesdk = " ${SDKPATHNATIVE}"

BBCLASSEXTEND = "native nativesdk"
