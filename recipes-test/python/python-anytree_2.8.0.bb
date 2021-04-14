SUMMARY = "anytree"
DESCRIPTION = "Simple, lightweight and extensible Tree data structure."
AUTHOR = "c0fec0de"
HOMEPAGE = "https://github.com/c0fec0de/anytree"
BUGTRACKER = "https://github.com/c0fec0de/anytree/issues"
SECTION = "devel"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=e3fc50a88d0a364313df4b21ef20c29e"

PYPI_PACKAGE = "anytree"

SRC_URI[md5sum] = "25ef3e656ad16a2a6b6c187807da7e5f"
SRC_URI[sha256sum] = "3f0f93f355a91bc3e6245319bf4c1d50e3416cc7a35cc1133c1ff38306bbccab"

inherit pypi setuptools

do_install_prepend() {
    # Remove LICCENSE from setup, as
    # it isn't really needed
    sed -i "s!include LICENSE!!g" ${S}/MANIFEST.in
    sed -i "s/('',\ \['LICENSE'\])//g" ${S}/setup.py
}

DEPENDS += "\
    ${PYTHON_PN}-six \
"

RDEPENDS_${PN} += "\
    ${PYTHON_PN}-six \
"

BBCLASSEXTEND = "native nativesdk"
