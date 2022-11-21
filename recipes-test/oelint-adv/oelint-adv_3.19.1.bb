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
            file://0004-changes-for-custom-rule.patch \
            file://0005-Patch-for-overridden-syntax-change-in-honister.patch \
            file://0006-remove-requirements.txt.patch"

SRC_URI[md5sum] = "f8fa7bbdfa33c9faf275670374317290"
SRC_URI[sha256sum] = "2220f0ffefc2cecbeee2d0fe4659654a6f729fd38394c2aee51820055a50b197"

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

