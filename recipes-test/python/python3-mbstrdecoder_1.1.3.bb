SUMMARY = "mbstrdecoder"
DESCRIPTION = "mbstrdecoder is a Python library for multi-byte character string decode"
AUTHOR = "Tsuyoshi Hombashi"
HOMEPAGE = "https://github.com/thombashi/mbstrdecoder"
BUGTRACKER = "https://github.com/thombashi/mbstrdecoder/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=0a668d244d562d7da35d6f9783af137d"

PYPI_PACKAGE = "mbstrdecoder"

SRC_URI[md5sum] = "33522a4bd9217dae46ebd0761e1a1e7c"
SRC_URI[sha256sum] = "dcfd2c759322eb44fe193a9e0b1b86c5b87f3ec5ea8e1bb43b3e9ae423f1e8fe"

inherit pypi setuptools3

DEPENDS += "\
    ${PYTHON_PN}-chardet \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-chardet \
"

BBCLASSEXTEND = "native nativesdk"
