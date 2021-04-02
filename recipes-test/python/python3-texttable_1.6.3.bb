SUMMARY = "texttable"
DESCRIPTION = "Python module for creating simple ASCII tables."
AUTHOR = "Gerome Fournier"
HOMEPAGE = "https://github.com/foutaise/texttable/"
BUGTRACKER = "https://github.com/foutaise/texttable/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=7a97cdac2d9679ffdcfef3dc036d24f6"

PYPI_PACKAGE = "texttable"

SRC_URI[md5sum] = "68e6b31d36f5c20221da7d5db3eca772"
SRC_URI[sha256sum] = "ce0faf21aa77d806bbff22b107cc22cce68dc9438f97a2df32c93e9afa4ce436"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
