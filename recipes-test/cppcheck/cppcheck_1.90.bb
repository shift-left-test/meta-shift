SUMMARY = "cppcheck - Static code analyzer for C/C++"
DESCRIPTION = "Cppcheck is a static analysis tool for C/C++ code"
HOMEPAGE = "http://cppcheck.sourceforge.net/"
SECTION = "devel"
BUGTRACKER = "https://trac.cppcheck.net/"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

SRC_URI = "git://github.com/danmar/cppcheck.git;protocol=https;tag=${PV} \
           file://0001-Makefile-fixes.patch"

S = "${WORKDIR}/git"

inherit pkgconfig

DEPENDS = "libpcre"

## no debug packages
INHIBIT_PACKAGE_DEBUG_SPLIT = "1"

EXTRA_OEMAKE = "HAVE_RULES=yes"
EXTRA_OEMAKE_class-native += "FILESDIR=${bindir}"

do_compile() {
	oe_runmake
}

FILES_${PN} = "${bindir}/** ${datadir}"

do_install() {
    install -d ${D}${bindir}
    install -d ${D}${datadir}
    install ${B}/cppcheck ${D}${bindir}
    cp -R ${B}/addons ${D}${bindir}
    cp -R ${B}/cfg ${D}${bindir}
    install -D ${B}/htmlreport/cppcheck-htmlreport ${D}${bindir}
}

BBCLASSEXTEND = "native nativesdk"
