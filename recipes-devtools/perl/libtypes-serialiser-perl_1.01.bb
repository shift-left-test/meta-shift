SUMMARY = "Types::Serialiser - simple data types for common serialisation formats"
DESCRIPTION = "This module provides some extra datatypes that are used by common serialisation formats such as JSON or CBOR. \
The idea is to have a repository of simple/small constants and containers that can be shared by different implementations \
so they become interoperable between each other."

HOMEPAGE = "https://metacpan.org/pod/Types::Serialiser"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPL-1.0-or-later"
LIC_FILES_CHKSUM = "file://COPYING;md5=043dba8b278e1db1b0ef93f30140b02b"

DEPENDS += "perl libcommon-sense-perl"

SRC_URI = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Types-Serialiser-${PV}.tar.gz"

SRC_URI[md5sum] = "4839af5f3fcbacc3945b0e6f3dc9a018"
SRC_URI[sha256sum] = "f8c7173b0914d0e3d957282077b366f0c8c70256715eaef3298ff32b92388a80"

S = "${WORKDIR}/Types-Serialiser-${PV}"

inherit cpan

RDEPENDS:${PN} += "perl libcommon-sense-perl"

BBCLASSEXTEND = "native"
