SUMMARY = "LCOV to Cobertura XML converter"
HOMEPAGE = "https://eriwen.github.com/lcov-to-cobertura-xml/"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=a09cec46daff2efa2376aaa93df30e16"

inherit pypi setuptools

PYPI_PACKAGE = "lcov_cobertura"

SRC_URI[md5sum] = "181d336280230414f045e5c26aacd4ce"
SRC_URI[sha256sum] = "0f4993d8a296f2a4b29287849be5af53ed85c0532f7d46cc25b8d3afa4375909"

RPROVIDES_${PN} = "lcov_cobertura"

BBCLASSEXTEND = "native nativesdk"
