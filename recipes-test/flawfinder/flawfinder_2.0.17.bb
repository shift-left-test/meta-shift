SUMMARY = "Flawfinder"
DESCRIPTION = "a static analysis tool for finding vulnerabilities in C/C++ source code"
AUTHOR = "David A. Wheeler"
HOMEPAGE = "https://github.com/david-a-wheeler/flawfinder"
BUGTRACKER = "https://github.com/david-a-wheeler/flawfinder/issues"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=0636e73ff0215e8d672dc4c32c317bb3"

DEPENDS += "python-native"

SRC_URI = "git://github.com/david-a-wheeler/flawfinder.git;protocol=https"

SRCREV = "53ad19bb3b864b36369a60c08bce12820c06a3a0"

S = "${WORKDIR}/git"

inherit setuptools

do_install_prepend() {
    # Remove the data_files section from setup, as
    # it isn't really needed
    sed -i "/data_files/d" ${S}/setup.py
}

do_install_append() {
    install -d ${D}${datadir}
}

FILES_${PN} += "${prefix}"

BBCLASSEXTEND = "native nativesdk"
