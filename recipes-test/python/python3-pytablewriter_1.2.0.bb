SUMMARY = "pytablewriter"
DESCRIPTION = "pytablewriter is a Python library to write a table in various formats: AsciiDoc / CSV / Elasticsearch / HTML / JavaScript / JSON / LaTeX / LDJSON / LTSV / Markdown / MediaWiki / NumPy / Excel / Pandas / Python / reStructuredText / SQLite / TOML / TSV / YAML."
AUTHOR = "Tsuyoshi Hombashi"
HOMEPAGE = "https://github.com/thombashi/pytablewriter"
BUGTRACKER = "https://github.com/thombashi/pytablewriter/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c83e45046b59fcd90b15acc1c54e1c00"

PYPI_PACKAGE = "pytablewriter"

SRC_URI[md5sum] = "4e3d421d026f30fadec4ac1670e524ee"
SRC_URI[sha256sum] = "0204a4bb684a22140d640f2599f09e137bcdc18b3dd49426f4a555016e246b46"

inherit pypi python_setuptools_build_meta

DEPENDS += "\
    ${PYTHON_PN}-dataproperty \
    ${PYTHON_PN}-mbstrdecoder \
    ${PYTHON_PN}-pathvalidate \
    ${PYTHON_PN}-tabledata \
    ${PYTHON_PN}-tcolorpy \
    ${PYTHON_PN}-typepy \
"

RDEPENDS:${PN} += "\
    ${PYTHON_PN}-dataproperty \
    ${PYTHON_PN}-mbstrdecoder \
    ${PYTHON_PN}-pathvalidate \
    ${PYTHON_PN}-tabledata \
    ${PYTHON_PN}-tcolorpy \
    ${PYTHON_PN}-typepy \
"

BBCLASSEXTEND = "native nativesdk"
