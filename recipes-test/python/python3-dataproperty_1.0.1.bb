SUMMARY = "DataProperty"
DESCRIPTION = "Python library for extract property from data."
AUTHOR = "Tsuyoshi Hombashi"
HOMEPAGE = "https://github.com/thombashi/DataProperty"
BUGTRACKER = "https://github.com/thombashi/DataProperty/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c83e45046b59fcd90b15acc1c54e1c00"

PYPI_PACKAGE = "DataProperty"

SRC_URI[md5sum] = "aca50cd5f543b7831d8a48ab1c02a152"
SRC_URI[sha256sum] = "723e5729fa6e885e127a771a983ee1e0e34bb141aca4ffe1f0bfa7cde34650a4"

inherit pypi python_setuptools_build_meta

DEPENDS += "\
    ${PYTHON_PN}-mbstrdecoder \
    ${PYTHON_PN}-typepy \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-mbstrdecoder \
    ${PYTHON_PN}-typepy \
"

BBCLASSEXTEND = "native nativesdk"
