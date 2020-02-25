SUMMARY = "Invoke py.test as distutils command with dependency resolution"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a33f38bbf47d48c70fe0d40e5f77498e"

SRC_URI[md5sum] = "e5f66b8e8e87f62c59631c35c919d321"
SRC_URI[sha256sum] = "96c7e73ead7b93e388c5d614770d2bae6526efd997757d3543fe17b557a0942b"

DEPENDS += "\
            ${PYTHON_PN}-setuptools-scm-native \
            ${PYTHON_PN}-setuptools-native \
            ${PYTHON_PN}-py-native \
           "
	   
inherit pypi
inherit native
inherit setuptools3
