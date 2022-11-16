SUMMARY = "LCOV to Cobertura XML converter"
DESCRIPTION = "lcov-cobertura: LCOV to Cobertura XML converter"
AUTHOR = "Eric Wendelin"
HOMEPAGE = "https://github.com/eriwen/lcov-to-cobertura-xml"
BUGTRACKER = "https://github.com/eriwen/lcov-to-cobertura-xml/issues"
SECTION = "devel"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=136e4f49dbf29942c572a3a8f6e88a77"

PYPI_PACKAGE = "lcov_cobertura"

SRC_URI += "file://0001-add-demangle-tool-option.patch \
            file://0002-add-condition-information.patch"

SRC_URI[md5sum] = "ca3833facd11177275a2176d58dce7c2"
SRC_URI[sha256sum] = "c6ce347bf3ee67f8d5d020cd662626a3594cf2be727cc634aa0d11fa3f7f1374"

inherit pypi setuptools3

RPROVIDES:${PN} = "lcov_cobertura"

BBCLASSEXTEND = "native nativesdk"
