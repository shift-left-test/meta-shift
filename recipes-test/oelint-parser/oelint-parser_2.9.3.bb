SUMMARY = "alternative parser for bitbake recipes"
DESCRIPTION = "alternative parser for bitbake recipes"
AUTHOR = "Konrad Weihmann"
HOMEPAGE = "https://github.com/priv-kweihmann/oelint-parser"
BUGTRACKER = "https://github.com/priv-kweihmann/oelint-parser/issues"
SECTION = "devel"
LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=297280a76099d6470990f30683c459d4"

PYPI_PACKAGE = "oelint_parser"

SRC_URI += "file://0001-changes-for-custom-rule.patch \
            file://0002-do-not-add-inherited-files.patch \
            file://0003-prevent-false-alarm-in-external-src-context.patch"


SRC_URI[md5sum] = "035c2e30b855c878a7a0c3dce96502a6"
SRC_URI[sha256sum] = "e6f4d189761ce8e34078c94bf56a06be9dd3669e6145f1c34a0c9e36b35970e5"

inherit pypi setuptools3

DEPENDS += "\
    ${PYTHON_PN}-regex \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-regex \
"

BBCLASSEXTEND = "native nativesdk"
