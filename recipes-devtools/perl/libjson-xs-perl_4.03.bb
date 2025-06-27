SUMMARY = "JSON serialising/deserialising, done correctly and fast"
DESCRIPTION = "This module converts Perl data structures to JSON and vice versa. \
Its primary goal is to be correct and its secondary goal is to be fast. \
To reach the latter goal it was written in C."

HOMEPAGE = "https://metacpan.org/pod/JSON::XS"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPL-1.0-or-later"
LIC_FILES_CHKSUM = "file://COPYING;md5=043dba8b278e1db1b0ef93f30140b02b"

DEPENDS += "perl libcanary-stability-perl-native libcommon-sense-perl-native libtypes-serialiser-perl-native"

SRC_URI = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-${PV}.tar.gz"

SRC_URI[md5sum] = "5358225ebc9f5b74516d7585ac236086"
SRC_URI[sha256sum] = "515536f45f2fa1a7e88c8824533758d0121d267ab9cb453a1b5887c8a56b9068"

S = "${UNPACKDIR}/JSON-XS-${PV}"

inherit cpan

RDEPENDS:${PN} += "perl libcanary-stability-perl libcommon-sense-perl libtypes-serialiser-perl"

do_install:append:class-native() {
  sed -i -e '1s,#!.*perl,#!${USRBINPATH}/env nativeperl,' ${D}${bindir}/json_xs
}

BBCLASSEXTEND = "native"
