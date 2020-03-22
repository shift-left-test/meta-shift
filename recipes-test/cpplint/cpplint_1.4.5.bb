SUMMARY = "CPPLint - a static code analyzer for C/C++"
DESCRIPTION = "A Static code analyzer for C/C++ written in python"
AUTHOR = "Google Inc."
HOMEPAGE = "https://github.com/cpplint/cpplint"
BUGTRACKER = "https://github.com/cpplint/cpplint/issues"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a58572e3501e262ddd5da01be644887d"

inherit pypi setuptools

PYPI_PACKAGE = "cpplint"

SRC_URI += "file://0001-remove-pytest-runner-dependency.patch"

SRC_URI[md5sum] = "1762216775e1666bbba3e5a3a92e82f9"
SRC_URI[sha256sum] = "08b384606136146ac1d32a2ffb60623a5dc1b20434588eaa0fa12a6e24eb3bf5"

RDEPENDS_${PN} += "${PYTHON_PN}-setuptools"

# To fix the nativesdk recipe shebang path bug of distutils for Yocto morty
do_install_append_class-nativesdk() {
    for i in ${D}${bindir}/* ; do
        sed -i -e s:${bindir}/env:${USRBINPATH}/env:g $i
    done
}

BBCLASSEXTEND = "native nativesdk"
