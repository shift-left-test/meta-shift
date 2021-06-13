SUMMARY = "Duplo"
DESCRIPTION = "C/C++/Java Duplicate Source Code Block Finder"
HOMEPAGE = "https://github.com/dlidstrom/Duplo"
BUGTRACKER = "https://github.com/dlidstrom/Duplo/issues"
SECTION = "devel"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=ffa10f40b98be2c2bc9608f56827ed23"

SRC_URI = "git://github.com/dlidstrom/Duplo.git;protocol=https;nobranch=1 \
           file://stdc++17_revert.patch"

SRCREV = "a49e772b00abbf8f6c6f34a7ec0a6c6ffcbf7bea"

S = "${WORKDIR}/git"

inherit cmake

BBCLASSEXTEND = "native nativesdk"

