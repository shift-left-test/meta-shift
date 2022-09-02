SUMMARY = "common::sense - save a tree AND a kitten, use common::sense!"
DESCRIPTION = "This module implements some sane defaults for Perl programs, \
as defined by two typical (or not so typical - use your common sense) specimens of Perl coders. \
In fact, after working out details on which warnings and strict modes to enable and make fatal, \
we found that we (and our code written so far, and others) fully agree on every option, \
even though we never used warnings before, \
so it seems this module indeed reflects a "common" sense among some long-time Perl coders."

HOMEPAGE = "https://metacpan.org/pod/common::sense"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPL-1.0+"
LIC_FILES_CHKSUM = "file://LICENSE;md5=043dba8b278e1db1b0ef93f30140b02b"

DEPENDS += "perl"

SRC_URI = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/common-sense-${PV}.tar.gz"

SRC_URI[md5sum] = "0929c6b03455ca988a9b4219aca15292"
SRC_URI[sha256sum] = "a86a1c4ca4f3006d7479064425a09fa5b6689e57261fcb994fe67d061cba0e7e"

S = "${WORKDIR}/common-sense-${PV}"

inherit cpan

RDEPENDS:${PN} += "perl"

BBCLASSEXTEND = "native"
