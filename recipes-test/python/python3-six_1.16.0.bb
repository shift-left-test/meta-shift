SUMMARY = "six"
DESCRIPTION = "Six is a Python 2 and 3 compatibility library."
AUTHOR = "Benjamin Peterson"
HOMEPAGE = "https://github.com/benjaminp/six"
BUGTRACKER = "https://github.com/benjaminp/six/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=43cfc9e4ac0e377acfb9b76f56b8415d"

PYPI_PACKAGE = "six"

SRC_URI[md5sum] = "a7c927740e4964dd29b72cebfc1429bb"
SRC_URI[sha256sum] = "1e61c37477a1626458e36f7b1d82aa5c9b094fa4802892072e49de9c60c4c926"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
