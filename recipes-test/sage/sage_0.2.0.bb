SUMMARY = "Static Analyzer Group Executor"
DESCRIPTION = "Execute the set of static analysis tools against the given source code"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "http://mod.lge.com/hub/yocto/addons/sage"
BUGTRACKER = "http://mod.lge.com/hub/yocto/addons/sage/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d41d8cd98f00b204e9800998ecf8427e"

DEPENDS_prepend = "\
    compiledb \
    cppcheck \
    cpplint \
"

SRC_URI = "git://mod.lge.com/hub/yocto/addons/sage.git;protocol=http;nobranch=1"

SRCREV = "e6fd38fe858439013a6dcf6bfb4a038f4069a2e7"

S = "${WORKDIR}/git"

inherit setuptools

RDEPENDS_${PN} = "\
    compiledb \
    cppcheck \
    cpplint \
"

BBCLASSEXTEND = "native nativesdk"
