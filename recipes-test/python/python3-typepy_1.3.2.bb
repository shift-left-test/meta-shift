SUMMARY = "typepy"
DESCRIPTION = "typepy is a Python library for variable type checker/validator/converter at a run time."
AUTHOR = "Tsuyoshi Hombashi"
HOMEPAGE = "https://github.com/thombashi/typepy"
BUGTRACKER = "https://github.com/thombashi/typepy/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=59fdfaa81e55e0ce5e45508e49e41f18"

PYPI_PACKAGE = "typepy"

SRC_URI[md5sum] = "2637fdf609b8a7b9b8ec722852efc706"
SRC_URI[sha256sum] = "b69fd48b9f50cdb3809906eef36b855b3134ff66c8893a4f8580abddb0b39517"

inherit pypi python_setuptools_build_meta

DEPENDS += "\
    ${PYTHON_PN}-dateutil \
    ${PYTHON_PN}-mbstrdecoder \
    ${PYTHON_PN}-packaging \
    ${PYTHON_PN}-pytz \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-dateutil \
    ${PYTHON_PN}-mbstrdecoder \
    ${PYTHON_PN}-packaging \
    ${PYTHON_PN}-pytz \
"

BBCLASSEXTEND = "native nativesdk"
