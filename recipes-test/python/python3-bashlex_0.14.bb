SUMMARY = "Python parser for bash"
DESCRIPTION = "bashlex is a Python port of the parser used internally by GNU bash."
AUTHOR = "Idan Kamara"
HOMEPAGE = "https://github.com/idank/bashlex"
BUGTRACKER = "https://github.com/idank/bashlex/issues"
SECTION = "devel"
LICENSE = "GPL-3.0+"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d32239bcb673463ab874e80d47fae504"

PYPI_PACKAGE = "bashlex"

SRC_URI[md5sum] = "25089ff596f0be42a430564e7f1dc5f6"
SRC_URI[sha256sum] = "5a92e0900b7a91de93a338b3fae651adc2b6a0e9656972b9e2ed3afd9c492ffd"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
