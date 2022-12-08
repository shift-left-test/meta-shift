SUMMARY = "alternative parser for bitbake recipes"
DESCRIPTION = "alternative parser for bitbake recipes"
AUTHOR = "Konrad Weihmann"
HOMEPAGE = "https://github.com/priv-kweihmann/oelint-parser"
BUGTRACKER = "https://github.com/priv-kweihmann/oelint-parser/issues"
SECTION = "devel"
LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=297280a76099d6470990f30683c459d4"

PYPI_PACKAGE = "oelint_parser"

SRC_URI += "file://0001-do-not-add-inherited-files.patch \
            file://0002-prevent-false-alarm-in-external-src-context.patch"


SRC_URI[md5sum] = "c8312e149f6b45f021fc3b297633e937"
SRC_URI[sha256sum] = "f0c0dbc17a11dbf5f9627770c9b754634e3a71f69dffbee8147f33110f8ceaf4"

inherit pypi setuptools3

DEPENDS += "\
    ${PYTHON_PN}-regex \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-regex \
"

BBCLASSEXTEND = "native nativesdk"
