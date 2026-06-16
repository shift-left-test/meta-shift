SUMMARY = "Generate a self-contained HTML report from JUnit/XUnit XML results"
DESCRIPTION = "junit2html turns a JUnit or XUnit XML results file into a single \
self-contained HTML report."
AUTHOR = "Ian Norton"
HOMEPAGE = "https://gitlab.com/inorton/junit2html"
BUGTRACKER = "https://gitlab.com/inorton/junit2html/-/issues"
SECTION = "devel"
LICENSE = "MIT"

# The sdist ships no LICENSE file, so checksum the license line in setup.py.
LIC_FILES_CHKSUM = "file://setup.py;beginline=21;endline=21;md5=055db07cc04cc29742c6605dee235451"

PYPI_PACKAGE = "junit2html"

SRC_URI[sha256sum] = "d6ae8aa4a76b66fa7c5efc460a4a28ae56430e0bc683f8a64d7f3e3443816d6b"

inherit pypi python_setuptools_build_meta

RDEPENDS:${PN} += "${PYTHON_PN}-jinja2"

# Used as a build-host tool by the shift tasks; native is enough.
BBCLASSEXTEND = "native"
