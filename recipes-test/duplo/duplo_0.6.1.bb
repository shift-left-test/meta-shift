# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=ffa10f40b98be2c2bc9608f56827ed23"

SRC_URI = "git://github.com/dlidstrom/Duplo.git;protocol=https"

SRCREV = "a49e772b00abbf8f6c6f34a7ec0a6c6ffcbf7bea"

SRC_URI += "file://stdc++17_revert.patch"

S = "${WORKDIR}/git"

inherit cmake

# Specify any options you want to pass to cmake using EXTRA_OECMAKE:
EXTRA_OECMAKE = ""

BBCLASSEXTEND = "native nativesdk"