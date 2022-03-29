SUMMARY = "metrix++"
DESCRIPTION = "Metrix++ is an extendable tool for code metrics collection and analysis."
AUTHOR = "Stefan Strobel"
HOMEPAGE = "https://metrixplusplus.github.io/home.html"
BUGTRACKER = "https://github.com/metrixplusplus/metrixplusplus/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=2eb11559d123a93fbde4d5567e366e2d"

SRC_URI = "git://github.com/metrixplusplus/metrixplusplus.git;protocol=https;nobranch=1 \
           file://remove-python-requires.patch \
           file://fix-to-ignore-errors-when-opening-file.patch"

SRCREV = "8b1a4b956507f0097d7761ddad02df897492fecc"

S = "${WORKDIR}/git"

inherit setuptools

BBCLASSEXTEND = "native nativesdk"

