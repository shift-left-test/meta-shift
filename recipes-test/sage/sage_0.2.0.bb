LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d41d8cd98f00b204e9800998ecf8427e"

SRC_URI = "git://mod.lge.com/hub/yocto/sage.git;protocol=http;tag=${PV}"

S = "${WORKDIR}/git"

inherit setuptools

# WARNING: the following rdepends are determined through basic analysis of the
# python sources, and might not be 100% accurate.
# RDEPENDS_${PN} += "python-argparse python-core python-json python-subprocess"
DEPENDS_prepend = " \
    compiledb \
    cppcheck \
    cpplint \
"

RDEPENDS_${PN} = " \
    compiledb \
    cppcheck \
    cpplint \
"

BBCLASSEXTEND = "native nativesdk"