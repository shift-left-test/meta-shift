SUMMARY = "the new Python stdlib enum module"
DESCRIPTION = "enum34 is the new Python stdlib enum module available in Python 3.4 backported for previous versions of Python from 2.4 to 3.3. tested on 2.6, 2.7, and 3.3+"
AUTHOR = "Ethan Furman"
HOMEPAGE = "https://bitbucket.org/stoneleaf/enum34/src/default/"
BUGTRACKER = "https://bitbucket.org/stoneleaf/enum34/issues"
SECTION = "devel"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://PKG-INFO;md5=1df814b19189c5fcd18ab57d938f6fd0"

PYPI_PACKAGE = "enum34"

SRC_URI[md5sum] = "b5ac0bb5ea9e830029599e410d09d3b5"
SRC_URI[sha256sum] = "cce6a7477ed816bd2542d03d53db9f0db935dd013b70f336a95c73979289f248"

inherit pypi setuptools

BBCLASSEXTEND = "native nativesdk"
