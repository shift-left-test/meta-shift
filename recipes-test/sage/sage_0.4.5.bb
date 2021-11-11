SUMMARY = "Static Analyzer Group Executor"
DESCRIPTION = "Execute the set of static analysis tools against the given source code"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "http://mod.lge.com/hub/yocto/addons/sage"
BUGTRACKER = "http://mod.lge.com/hub/yocto/addons/sage/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=df949e8c96ecf1483905048fb77276b5"

SRC_URI = "git://mod.lge.com/hub/yocto/addons/sage.git;protocol=http;nobranch=1"

SRCREV = "93ebb7a2878cd0c3e73638b5d9d7040721db49ac"

S = "${WORKDIR}/git"

inherit setuptools


DEPENDS += "\
    ${PYTHON_PN}-texttable \
    duplo \
    metrixpp \
"

RDEPENDS_${PN} += "\
    ${PYTHON_PN}-texttable \
"

do_install_append_class-native() {
    if test -e ${D}${bindir} ; then
        for i in ${D}${bindir}/* ; do \
            sed -i -e s:${bindir}/python-native/python:${USRBINPATH}/env\ nativepython:g $i
        done
    fi
}

BBCLASSEXTEND = "native nativesdk"

