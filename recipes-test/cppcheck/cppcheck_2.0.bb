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

PACKAGECONFIG ??= "rules"
PACKAGECONFIG[rules] = "HAVE_RULES=yes,,libpcre"
PACKAGECONFIG[z3] = "USE_Z3=yes,,z3"

do_compile() {
    oe_runmake ${PACKAGECONFIG_CONFARGS} FILESDIR=${datadir}
}

do_install() {
    oe_runmake install DESTDIR=${D} FILESDIR=${datadir} PREFIX=${prefix}
}

FILES_${PN} = "${bindir} ${datadir}"

BBCLASSEXTEND = "native nativesdk"
