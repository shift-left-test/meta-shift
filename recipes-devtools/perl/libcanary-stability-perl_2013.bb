SUMMARY = "Canary::Stability - canary to check perl compatibility for schmorp's modules"
DESCRIPTION = "This module is used by Schmorp's modules during configuration stage to test the installed perl for compatibility with his modules. \
It's not, at this stage, meant as a tool for other module authors, although in principle nothing prevents them from subscribing to the same ideas."

HOMEPAGE = "https://metacpan.org/pod/Canary::Stability"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPL-1.0+"
LIC_FILES_CHKSUM = "file://COPYING;md5=043dba8b278e1db1b0ef93f30140b02b"

DEPENDS += "perl"

SRC_URI = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Canary-Stability-${PV}.tar.gz"

SRC_URI[md5sum] = "5368520547521b254317ea0e9b3d23ab"
SRC_URI[sha256sum] = "a5c91c62cf95fcb868f60eab5c832908f6905221013fea2bce3ff57046d7b6ea"

S = "${WORKDIR}/Canary-Stability-${PV}"

inherit cpan

RDEPENDS_${PN} += "perl"

BBCLASSEXTEND = "native"
