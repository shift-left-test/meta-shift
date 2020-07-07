SUMMARY = "CPPLint - a static code analyzer for C/C++"
DESCRIPTION = "A Static code analyzer for C/C++ written in python"
AUTHOR = "Google Inc."
HOMEPAGE = "https://github.com/cpplint/cpplint"
BUGTRACKER = "https://github.com/cpplint/cpplint/issues"
SECTION = "devel"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a58572e3501e262ddd5da01be644887d"

PYPI_PACKAGE = "cpplint"

SRC_URI += "file://0001-remove-pytest-runner-dependency.patch"

SRC_URI[md5sum] = "1762216775e1666bbba3e5a3a92e82f9"
SRC_URI[sha256sum] = "08b384606136146ac1d32a2ffb60623a5dc1b20434588eaa0fa12a6e24eb3bf5"

inherit pypi setuptools3

RDEPENDS_${PN} += "${PYTHON_PN}-setuptools"

BBCLASSEXTEND = "native nativesdk"
