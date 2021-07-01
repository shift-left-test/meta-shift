SUMMARY = "Python parser for bash"
DESCRIPTION = "bashlex is a Python port of the parser used internally by GNU bash."
AUTHOR = "Idan Kamara"
HOMEPAGE = "https://github.com/idank/bashlex"
BUGTRACKER = "https://github.com/idank/bashlex/issues"
SECTION = "devel"
LICENSE = "GPL-3.0+"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d32239bcb673463ab874e80d47fae504"

PYPI_PACKAGE = "bashlex"

SRC_URI[md5sum] = "964e165b427837b5c3940e871ccb4678"
SRC_URI[sha256sum] = "fe539cf9eba046f60a8d32eda2a28e9dccdd06cb4b9f5089ec658348ea53a6dd"

inherit pypi setuptools

BBCLASSEXTEND = "native nativesdk"
