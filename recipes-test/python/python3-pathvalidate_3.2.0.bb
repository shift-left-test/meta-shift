SUMMARY = "pathvalidate"
DESCRIPTION = "pathvalidate is a Python library to sanitize/validate a string such as filenames/file-paths/etc."
AUTHOR = "Tsuyoshi Hombashi"
HOMEPAGE = "https://github.com/thombashi/pathvalidate"
BUGTRACKER = "https://github.com/thombashi/pathvalidate/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c83e45046b59fcd90b15acc1c54e1c00"

PYPI_PACKAGE = "pathvalidate"

SRC_URI[md5sum] = "2a76cbe4e08f58087f418d150a1461b5"
SRC_URI[sha256sum] = "5e8378cf6712bff67fbe7a8307d99fa8c1a0cb28aa477056f8fc374f0dff24ad"

inherit pypi python_setuptools_build_meta

BBCLASSEXTEND = "native nativesdk"
