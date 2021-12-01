SUMMARY = "texttable"
DESCRIPTION = "Python module for creating simple ASCII tables."
AUTHOR = "Gerome Fournier"
HOMEPAGE = "https://github.com/foutaise/texttable/"
BUGTRACKER = "https://github.com/foutaise/texttable/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=7a97cdac2d9679ffdcfef3dc036d24f6"

PYPI_PACKAGE = "texttable"

SRC_URI[md5sum] = "15faadc07ba44d337cc1675ea6092a02"
SRC_URI[sha256sum] = "42ee7b9e15f7b225747c3fa08f43c5d6c83bc899f80ff9bae9319334824076e9"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
