SUMMARY = "Tool for generating Clang's JSON Compilation Database files"
DESCRIPTION = "Tool for generating Clang's JSON Compilation Database files for make-based build systems."
AUTHOR = "Nick Yamane"
HOMEPAGE = "https://github.com/nickdiego/compiledb"
BUGTRACKER = "https://github.com/nickdiego/compiledb/issues"
SECTION = "devel"
LICENSE = "GPL-3.0-or-later"
LIC_FILES_CHKSUM = "file://LICENSE;md5=784d7dc7357bd924e8d5642892bf1b6b"

PYPI_PACKAGE = "compiledb"

DEPENDS += "\
    ${PYTHON_PN}-bashlex \
    ${PYTHON_PN}-click \
    ${PYTHON_PN}-setuptools-scm-native \
"

SRC_URI[sha256sum] = "97752d8810b6977654a11a22cdc41bf6b71473bcdb5da312bc135f36d6af8271"

# compiledb >= 0.10.5 builds via PEP 517 (pyproject.toml + setuptools-scm).
# It is fetched as a PyPI sdist with no SCM metadata, so pin the version
# explicitly instead of letting setuptools-scm probe for a git tree.
export SETUPTOOLS_SCM_PRETEND_VERSION = "${PV}"

inherit pypi python_setuptools_build_meta

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-bashlex \
    ${PYTHON_PN}-click \
"

BBCLASSEXTEND = "native nativesdk"
