SUMMARY = "Python composable command line interface toolkit"
DESCRIPTION = "Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary."
AUTHOR = "Pallets"
HOMEPAGE = "https://github.com/pallets/click"
BUGTRACKER = "https://github.com/pallets/click/issues"
SECTION = "devel"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE.rst;md5=1fa98232fd645608937a0fdc82e999b8"

PYPI_PACKAGE = "click"

SRC_URI[md5sum] = "53692f62cb99a1a10c59248f1776d9c0"
SRC_URI[sha256sum] = "d2b5255c7c6349bc1bd1e59e08cd12acbbd63ce649f2588755783aa94dfb6b1a"

inherit pypi setuptools

BBCLASSEXTEND = "native nativesdk"
