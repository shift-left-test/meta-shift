SUMMARY = "Mutation Testing Tool"
DESCRIPTION = "The mutation testing tool for the meta-shift project"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "https://github.com/shift-left-test/sentinel"
BUGTRACKER = "https://github.com/shift-left-test/sentinel/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=df949e8c96ecf1483905048fb77276b5 \
                    file://external/args-6.2.3/LICENSE;md5=b5d002ff26328bc38158aff274711f1d \
                    file://external/tinyxml2/LICENSE.txt;md5=135624eef03e1f1101b9ba9ac9b5fffd \
                    file://external/fmt/LICENSE.rst;md5=af88d758f75f3c5c48a967501f24384b"

DEPENDS_class-native += "\
    clang-cross-${TUNE_ARCH} \
    libgit2-native \
    ncurses-native \
"

SRC_URI = "git://github.com/shift-left-test/sentinel.git;protocol=https;nobranch=1"
SRCREV = "093b795bfa65c07053d3f379e14cc9ae1b6f08ee"

S = "${WORKDIR}/git"

inherit cmake native
