SUMMARY = "LCOV to Cobertura XML converter"
HOMEPAGE = "https://eriwen.github.com/lcov-to-cobertura-xml/"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=136e4f49dbf29942c572a3a8f6e88a77"

# SRC_URI = "git://github.com/eriwen/lcov-to-${PV}-xml.git;protocol=https"

# Modify these as desired
# PV = "cobertura+git${SRCPV}"
# SRCREV = "59584761cb5da4687693faec05bf3e2b74e9dde9"

# S = "${WORKDIR}/git"

# inherit distutils

inherit pypi setuptools

PYPI_PACKAGE = "lcov_cobertura"

SRC_URI[md5sum] = "181d336280230414f045e5c26aacd4ce"
SRC_URI[sha256sum] = "0f4993d8a296f2a4b29287849be5af53ed85c0532f7d46cc25b8d3afa4375909"

# WARNING: the following rdepends are determined through basic analysis of the
# python sources, and might not be 100% accurate.
# RDEPENDS_${PN} += "python-core python-distutils python-re python-subprocess python-textutils python-xml"

RPROVIDES_${PN} = "lcov_cobertura"

BBCLASSEXTEND = "native nativesdk"