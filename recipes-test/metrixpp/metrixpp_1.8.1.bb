SUMMARY = "metrix++"
DESCRIPTION = "Metrix++ is an extendable tool for code metrics collection and analysis."
AUTHOR = "Stefan Strobel"
HOMEPAGE = "https://metrixplusplus.github.io/home.html"
BUGTRACKER = "https://github.com/metrixplusplus/metrixplusplus/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2eb11559d123a93fbde4d5567e366e2d"

SRC_URI = "git://github.com/metrixplusplus/metrixplusplus.git;protocol=https;nobranch=1"

SRCREV = "ac9a697381d2740165d47526b82bb4e6aa8def48"

inherit setuptools3

DEPENDS += "\
    ${PYTHON_PN}-pytablewriter \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-pytablewriter \
"

BBCLASSEXTEND = "native nativesdk"
