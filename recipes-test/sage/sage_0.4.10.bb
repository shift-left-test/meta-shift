SUMMARY = "Static Analyzer Group Executor"
DESCRIPTION = "Execute the set of static analysis tools against the given source code"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "https://github.com/shift-left-test/sage"
BUGTRACKER = "https://github.com/shift-left-test/sage/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=df949e8c96ecf1483905048fb77276b5 \
                    file://oss-pkg-info.yaml;md5=f72b54b66db40d89f1246b04ba924707"

SRC_URI = "git://github.com/shift-left-test/sage.git;protocol=https;nobranch=1"

SRCREV = "68213cb738688e9f1f0a91370e341bc68f7195bb"

inherit setuptools3

DEPENDS += "\
    ${PYTHON_PN}-texttable \
    ${PYTHON_PN}-defusedxml \
    duplo \
    metrixpp \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-texttable \
    ${PYTHON_PN}-defusedxml \
"

BBCLASSEXTEND = "native nativesdk"
