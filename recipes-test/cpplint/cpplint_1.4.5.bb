SUMMARY = "CPPLint - a static code analyzer for C/C++"
DESCRIPTION = "A Static code analyzer for C/C++ written in python"
AUTHOR = "Google Inc."
HOMEPAGE = "https://github.com/cpplint/cpplint"
BUGTRACKER = "https://github.com/cpplint/cpplint/issues"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=a58572e3501e262ddd5da01be644887d"

SRC_URI = "git://github.com/cpplint/cpplint.git;protocol=https;tag=${PV};nobranch=1"

S = "${WORKDIR}/git"

DEPENDS = "python-native"

do_install() {
    install -d ${D}${bindir}
    install -m 755 ${B}/cpplint.py ${D}${bindir}/
}

FILES_${PN} ="${bindir}"

BBCLASSEXTEND = "native nativesdk"
