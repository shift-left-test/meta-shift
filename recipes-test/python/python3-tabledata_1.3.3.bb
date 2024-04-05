SUMMARY = "tabledata"
DESCRIPTION = "tabledata is a Python library to represent tabular data. Used for pytablewriter/pytablereader/SimpleSQLite/etc."
AUTHOR = "Tsuyoshi Hombashi"
HOMEPAGE = "https://github.com/thombashi/tabledata"
BUGTRACKER = "https://github.com/thombashi/tabledata/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=59fdfaa81e55e0ce5e45508e49e41f18"

PYPI_PACKAGE = "tabledata"

SRC_URI[md5sum] = "579c4e7454a837d252d4977b73556aae"
SRC_URI[sha256sum] = "c90daaba9a408e4397934b3ff2f6c06797d5289676420bf520c741ad43e6ff91"

inherit pypi setuptools3

DEPENDS += "\
    ${PYTHON_PN}-dataproperty \
    ${PYTHON_PN}-typepy \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-dataproperty \
    ${PYTHON_PN}-typepy \
"

BBCLASSEXTEND = "native nativesdk"
