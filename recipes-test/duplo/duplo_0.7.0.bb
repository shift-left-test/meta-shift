SUMMARY = "Duplo"
DESCRIPTION = "C/C++/Java Duplicate Source Code Block Finder"
HOMEPAGE = "https://github.com/dlidstrom/Duplo"
BUGTRACKER = "https://github.com/dlidstrom/Duplo/issues"
SECTION = "devel"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=ffa10f40b98be2c2bc9608f56827ed23"

SRC_URI = "git://github.com/dlidstrom/Duplo.git;protocol=https;nobranch=1 \
           file://stdc++17_revert.patch \
           file://0002-add-hpp-file-extension.patch \
"

SRCREV = "370e9bf76ac58e3f66779be8f3b0302f71d0cbe0"

S = "${WORKDIR}/git"

inherit cmake

BBCLASSEXTEND = "native nativesdk"
