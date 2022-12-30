SUMMARY = "XML bomb protection for Python stdlib modules"
DESCRIPTION = "Python package with modified subclasses of all stdlib XML \
parsers that prevent any potentially malicious operation."
AUTHOR = "Christian Heimes"
HOMEPAGE = "https://github.com/tiran/defusedxml"
BUGTRACKER = "https://github.com/tiran/defusedxml/issues"
SECTION = "devel"
LICENSE = "PSFv2"
LIC_FILES_CHKSUM = "file://LICENSE;md5=056fea6a4b395a24d0d278bf5c80249e"

PYPI_PACKAGE = "defusedxml"

SRC_URI[md5sum] = "7ff1501366c6d1dcd2de8514dc2b755e"
SRC_URI[sha256sum] = "24d7f2f94f7f3cb6061acb215685e5125fbcdc40a857eff9de22518820b0a4f4"

inherit pypi setuptools

BBCLASSEXTEND = "native nativesdk"

