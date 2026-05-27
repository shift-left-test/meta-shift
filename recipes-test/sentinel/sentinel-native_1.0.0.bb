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
                    file://external/fmt/LICENSE.rst;md5=af88d758f75f3c5c48a967501f24384b \
                    file://external/ftxui/LICENSE;md5=602507f167b627b30ce2cd7a24d50ea3 \
                    file://external/yaml-cpp/LICENSE;md5=6a8aaf0595c2efc1a9c2e0913e9c1a2c \
                    file://external/libgit2/COPYING;md5=8eacfdc17c8f4d219e131a073973b97d \
                    file://oss-pkg-info.yaml;md5=a86c5c89b251c54ccfe2d9683f63bda8"

TUNE_FEATURES:class-native += "${TUNE_FEATURES:tune-${DEFAULTTUNE}}"

DEPENDS:class-native += "\
    clang-cross-${TUNE_ARCH} \
    ncurses-native \
    zstd-native \
"

SRC_URI = "git://github.com/shift-left-test/sentinel.git;protocol=https;nobranch=1"
SRCREV = "9e281ee2c3564123f5db7c93c5795309bb24cd5b"

inherit cmake native
