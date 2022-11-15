SUMMARY = "cppcheck - Static code analyzer for C/C++"
DESCRIPTION = "Cppcheck is a static analysis tool for C/C++ code"
AUTHOR = "The cppcheck team"
HOMEPAGE = "http://cppcheck.sourceforge.net/"
BUGTRACKER = "https://trac.cppcheck.net/"
SECTION = "devel"
LICENSE = "GPL-3.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

SRC_URI = "git://github.com/danmar/cppcheck.git;protocol=https;nobranch=1 \
           file://0001-Makefile-fixes.patch"

SRCREV = "aca3f6fefa6d6b8c5915f15035c7e5908961f6f1"

S = "${WORKDIR}/git"

inherit pkgconfig

PACKAGECONFIG ??= "rules"
PACKAGECONFIG[rules] = "HAVE_RULES=yes,,libpcre"
PACKAGECONFIG[z3] = "USE_Z3=yes,,z3"

do_compile() {
    oe_runmake ${PACKAGECONFIG_CONFARGS}
}

do_install() {
    oe_runmake install DESTDIR=${D} FILESDIR=${bindir} PREFIX=${prefix}
}

FILES:${PN} = "${bindir} ${datadir}"

BBCLASSEXTEND = "native nativesdk"
