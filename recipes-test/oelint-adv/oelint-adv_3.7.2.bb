SUMMARY = "Advanced oelint"
DESCRIPTION = "Advanced oelint"
AUTHOR = "Konrad Weihmann"
HOMEPAGE = "https://github.com/priv-kweihmann/oelint-adv"
BUGTRACKER = "https://github.com/priv-kweihmann/oelint-adv/issues"
SECTION = "devel"
LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e926c89aceef6c1a4247d5df08f94533"

SRC_URI = "git://github.com/priv-kweihmann/oelint-adv.git;protocol=https;nobranch=1"
SRCREV = "8106cb9fdd71834b131487bcef41e95f68895b4e"

SRC_URI += "file://0001-compatibility-with-python2.patch \
            file://0002-change-output-option-to-make-json-format-report.patch \
            file://0003-add-logger.patch \
            file://0004-disable-SSL-CERTIFICATE_VERIFY_FAILED.patch \
            file://0005-changes-for-custom-rule.patch"

S = "${WORKDIR}/git"

inherit setuptools3

DEPENDS += "\
    oelint-parser \
    ${PYTHON_PN}-colorama \
    ${PYTHON_PN}-anytree \
"

RDEPENDS_${PN} += "\
    oelint-parser \
    ${PYTHON_PN}-colorama \
    ${PYTHON_PN}-anytree \
"

BBCLASSEXTEND = "native nativesdk"

