SUMMARY = "Tool for generating Clang's JSON Compilation Database files"
DESCRIPTION = "Tool for generating Clang's JSON Compilation Database files for make-based build systems."
AUTHOR = "Nick Yamane"
HOMEPAGE = "https://github.com/nickdiego/compiledb"
BUGTRACKER = "https://github.com/nickdiego/compiledb/issues"
SECTION = "devel"
LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://PKG-INFO;md5=1edc0f0ce6c3b1c976f0c74187d93b15"

PYPI_PACKAGE = "compiledb"

DEPENDS += "\
    ${PYTHON_PN}-bashlex \
    ${PYTHON_PN}-click \
    ${PYTHON_PN}-shutilwhich \
"

SRC_URI[md5sum] = "957ea6c6b66017f7ecefe9edf8ee7a80"
SRC_URI[sha256sum] = "06bb47dd1fa04de3a12720379ff382d40441074476db7c16a27e2ad79b7e966e"

inherit pypi setuptools3

RDEPENDS_${PN} += "\
    ${PYTHON_PN}-bashlex \
    ${PYTHON_PN}-click \
    ${PYTHON_PN}-shutilwhich \
"

BBCLASSEXTEND = "native nativesdk"
