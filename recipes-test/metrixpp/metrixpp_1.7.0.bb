SUMMARY = "metrix++"
DESCRIPTION = "Metrix++ is an extendable tool for code metrics collection and analysis."
AUTHOR = "Stefan Strobel"
HOMEPAGE = "https://metrixplusplus.github.io/home.html"
BUGTRACKER = "https://github.com/metrixplusplus/metrixplusplus/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fa326b4a8b6570216bf32b2a9b38d919"

SRC_URI = "git://github.com/metrixplusplus/metrixplusplus.git;protocol=https;nobranch=1"
SRCREV = "cb87f5650f12dee6025dc81cdaa99806ff6a4f86"

SRC_URI += "file://remove-python-requires.patch"

S = "${WORKDIR}/git"

inherit setuptools3

BBCLASSEXTEND = "native nativesdk"
