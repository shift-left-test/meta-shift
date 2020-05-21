LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://PKG-INFO;md5=1edc0f0ce6c3b1c976f0c74187d93b15"

inherit pypi setuptools

PYPI_PACKAGE = "compiledb"

SRC_URI[md5sum] = "957ea6c6b66017f7ecefe9edf8ee7a80"
SRC_URI[sha256sum] = "06bb47dd1fa04de3a12720379ff382d40441074476db7c16a27e2ad79b7e966e"

DEPENDS += " \
    ${PYTHON_PN}-bashlex \
    ${PYTHON_PN}-click \
    ${PYTHON_PN}-enum34 \
    ${PYTHON_PN}-shutilwhich \
"

RDEPENDS_${PN} += " \
    ${PYTHON_PN}-bashlex \
    ${PYTHON_PN}-click \
    ${PYTHON_PN}-enum34 \
    ${PYTHON_PN}-shutilwhich \
"

BBCLASSEXTEND = "native nativesdk"