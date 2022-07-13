SUMMARY = "CPPLint - a static code analyzer for C/C++"
DESCRIPTION = "A Static code analyzer for C/C++ written in python"
AUTHOR = "Google Inc."
HOMEPAGE = "https://github.com/cpplint/cpplint"
BUGTRACKER = "https://github.com/cpplint/cpplint/issues"
SECTION = "devel"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a58572e3501e262ddd5da01be644887d"

PYPI_PACKAGE = "cpplint"

SRC_URI += "file://0001-remove-pytest-runner-dependency.patch \
            file://0002-compatibility-with-python2.patch"

SRC_URI[md5sum] = "6c28ca4d4bae38310ca9a48629e91076"
SRC_URI[sha256sum] = "8af99f95ed1af2d18e60467cdc13ee0441c2a14d693b7d2dbb71ad427074e491"

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
