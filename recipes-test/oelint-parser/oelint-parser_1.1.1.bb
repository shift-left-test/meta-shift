SUMMARY = "alternative parser for bitbake recipes"
DESCRIPTION = "alternative parser for bitbake recipes"
AUTHOR = "Konrad Weihmann"
HOMEPAGE = "https://github.com/priv-kweihmann/oelint-parser"
BUGTRACKER = "https://github.com/priv-kweihmann/oelint-parser/issues"
SECTION = "devel"
LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=297280a76099d6470990f30683c459d4"

SRC_URI = "git://github.com/priv-kweihmann/oelint-parser.git;protocol=https;nobranch=1"
SRCREV = "3811959428f5b8881ad968cd0c197f62ce1b5839"

SRC_URI += "file://0001-compatibility-with-python2.patch \
            file://0002-changes-for-custom-rule.patch"

S = "${WORKDIR}/git"

inherit setuptools3

BBCLASSEXTEND = "native nativesdk"
