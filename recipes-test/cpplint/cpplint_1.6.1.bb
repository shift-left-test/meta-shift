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

SRC_URI[md5sum] = "a3e842f20d6cf6f512e7885f71937bdb"
SRC_URI[sha256sum] = "d430ce8f67afc1839340e60daa89e90de08b874bc27149833077bba726dfc13a"

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
