SUMMARY = "Static Analyzer Group Executor"
DESCRIPTION = "Execute the set of static analysis tools against the given source code"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "http://mod.lge.com/hub/yocto/addons/sage"
BUGTRACKER = "http://mod.lge.com/hub/yocto/addons/sage/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d41d8cd98f00b204e9800998ecf8427e"

SRC_URI = "git://mod.lge.com/hub/yocto/addons/sage.git;protocol=http;nobranch=1"

SRCREV = "1d7119ca99e180bdfd38c4c95907dbf69bf3b7d4"

S = "${WORKDIR}/git"

inherit setuptools

do_install_append_class-native() {
    if test -e ${D}${bindir} ; then
        for i in ${D}${bindir}/* ; do \
            sed -i -e s:${bindir}/python-native/python:${USRBINPATH}/env\ nativepython:g $i
        done
    fi
}

BBCLASSEXTEND = "native nativesdk"
