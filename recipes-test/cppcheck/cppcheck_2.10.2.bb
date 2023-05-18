SUMMARY = "cppcheck - Static code analyzer for C/C++"
DESCRIPTION = "Cppcheck is a static analysis tool for C/C++ code"
AUTHOR = "The cppcheck team"
HOMEPAGE = "http://cppcheck.sourceforge.net/"
BUGTRACKER = "https://trac.cppcheck.net/"
SECTION = "devel"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

SRC_URI = "git://github.com/danmar/cppcheck.git;protocol=https;branch=2.10.x \
    file://0001-cleaned-up-includes-based-on-include-what-you-use-45.patch \
    file://0002-Add-missing-rebinding-trait-to-TaggedAllocator.patch \
"

SRCREV = "5c2d64ec4809fcba712b1114cf0462962924b903"

S = "${WORKDIR}/git"

inherit pkgconfig

PACKAGECONFIG ??= ""
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
