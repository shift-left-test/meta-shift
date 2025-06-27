SUMMARY = "Duplo"
DESCRIPTION = "C/C++/Java Duplicate Source Code Block Finder"
HOMEPAGE = "https://github.com/dlidstrom/Duplo"
BUGTRACKER = "https://github.com/dlidstrom/Duplo/issues"
SECTION = "devel"
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=ffa10f40b98be2c2bc9608f56827ed23"

SRC_URI = "git://github.com/dlidstrom/Duplo.git;protocol=https;nobranch=1 \
           file://stdc++17_revert.patch \
           file://0002-add-hpp-file-extension.patch \
"

SRCREV = "0bf5dee6d08e7aee15e7d587f6287c036fa248fb"

inherit cmake

BBCLASSEXTEND = "native nativesdk"
