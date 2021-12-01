SUMMARY = "Python parser for bash"
DESCRIPTION = "bashlex is a Python port of the parser used internally by GNU bash."
AUTHOR = "Idan Kamara"
HOMEPAGE = "https://github.com/idank/bashlex"
BUGTRACKER = "https://github.com/idank/bashlex/issues"
SECTION = "devel"
LICENSE = "GPL-3.0+"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d32239bcb673463ab874e80d47fae504"

PYPI_PACKAGE = "bashlex"

SRC_URI += "file://0001-compatability-for-low-versions-of-setuptools.patch"

SRC_URI[md5sum] = "8b855bb4aa275a48235257a3b2d048b3"
SRC_URI[sha256sum] = "dc6f017e49ce2d0fe30ad9f5206da9cd13ded073d365688c9fda525354e8c373"

inherit pypi setuptools

BBCLASSEXTEND = "native nativesdk"
