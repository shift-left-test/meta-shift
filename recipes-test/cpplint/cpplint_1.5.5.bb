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

SRC_URI[md5sum] = "88e9cf6a216c4281dab488d398589236"
SRC_URI[sha256sum] = "18e768d8a4e0c329d88f1272b0283bbc3beafce76f48ee0caeb44ddbf505bba5"

inherit pypi setuptools

RDEPENDS_${PN} += "${PYTHON_PN}-setuptools"

do_install_append_class-native() {
    if test -e ${D}${bindir} ; then
        for i in ${D}${bindir}/* ; do \
            sed -i -e s:${bindir}/python-native/python:${USRBINPATH}/env\ nativepython:g $i
        done
    fi
}

BBCLASSEXTEND = "native nativesdk"
