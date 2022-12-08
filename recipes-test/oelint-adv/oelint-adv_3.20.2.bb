SUMMARY = "Advanced oelint"
DESCRIPTION = "Advanced oelint"
AUTHOR = "Konrad Weihmann"
HOMEPAGE = "https://github.com/priv-kweihmann/oelint-adv"
BUGTRACKER = "https://github.com/priv-kweihmann/oelint-adv/issues"
SECTION = "devel"
LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e926c89aceef6c1a4247d5df08f94533"

PYPI_PACKAGE = "oelint_adv"

SRC_URI += "file://0001-change-output-option-to-make-json-format-report.patch \
            file://0002-add-logger.patch \
            file://0003-disable-SSL-CERTIFICATE_VERIFY_FAILED.patch \
            file://0004-remove-requirements.txt.patch"

SRC_URI[md5sum] = "b103834dea2da1f47856d1922b2a498c"
SRC_URI[sha256sum] = "0335a3aa878592f58328b9a4593ad15e67586955251f64d73c8c3cac28456ab0"

inherit pypi setuptools3

DEPENDS += "\
    oelint-parser \
    ${PYTHON_PN}-colorama \
    ${PYTHON_PN}-anytree \
"

RDEPENDS:${PN} += "\
    oelint-parser \
    ${PYTHON_PN}-colorama \
    ${PYTHON_PN}-anytree \
"

BBCLASSEXTEND = "native nativesdk"
