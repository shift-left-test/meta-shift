SUMMARY = "colorama"
DESCRIPTION = "Makes ANSI escape character sequences (for producing colored terminal text and cursor positioning) work under MS Windows."
AUTHOR = "Jonathan Hartley"
HOMEPAGE = "https://github.com/tartley/colorama"
BUGTRACKER = "https://github.com/tartley/colorama/issues"
SECTION = "devel"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=b4936429a56a652b84c5c01280dcaa26"

PYPI_PACKAGE = "colorama"

SRC_URI[md5sum] = "02daee502863d24112a8c05a5d69a612"
SRC_URI[sha256sum] = "e96da0d330793e2cb9485e9ddfd918d456036c7149416295932478192f4436a1"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
