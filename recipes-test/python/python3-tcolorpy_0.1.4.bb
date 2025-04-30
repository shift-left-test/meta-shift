SUMMARY = "tcolorpy"
DESCRIPTION = "tcolopy is a Python library to apply true color for terminal text."
AUTHOR = "Tsuyoshi Hombashi"
HOMEPAGE = "https://github.com/thombashi/tcolorpy"
BUGTRACKER = "https://github.com/thombashi/tcolorpy/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=9600ae80fdc807c76a33c361519a0dd6"

PYPI_PACKAGE = "tcolorpy"

SRC_URI[md5sum] = "ca571cccff812ecdc0c73968c9d24ebf"
SRC_URI[sha256sum] = "f0dceb1cb95e554cee63024b3cd2fd8d4628c568773de2d1e6b4f0478461901c"

inherit pypi python_setuptools_build_meta

BBCLASSEXTEND = "native nativesdk"
