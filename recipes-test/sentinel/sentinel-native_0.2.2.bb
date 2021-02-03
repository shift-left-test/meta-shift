SUMMARY = "Mutation Testing Tool"
DESCRIPTION = "The mutation testing tool for the meta-shift project"
AUTHOR = "Sung Gon Kim"
HOMEPAGE = "http://mod.lge.com/hub/yocto/addons/sentinel"
BUGTRACKER = "http://mod.lge.com/hub/yocto/addons/sentinel/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=68afeac0415f7ffea472ec34ec9d20c7 \
                    file://external/args-6.2.3/LICENSE;md5=b5d002ff26328bc38158aff274711f1d \
                    file://external/tinyxml2/LICENSE.txt;md5=135624eef03e1f1101b9ba9ac9b5fffd \
                    file://external/fmt/LICENSE.rst;md5=af88d758f75f3c5c48a967501f24384b"

DEPENDS_class-native += "\
    clang-cross-${TUNE_ARCH} \
    libgit2-native \
"

SRC_URI = "git://mod.lge.com/hub/yocto/addons/sentinel.git;protocol=http;nobranch=1"
SRCREV = "268ac2761f7b1f02ac94fcf960053d039dee476c"

S = "${WORKDIR}/git"

inherit cmake native
