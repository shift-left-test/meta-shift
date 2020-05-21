SUMMARY = "shutil.which for those not using Python 3.3 yet."
HOMEPAGE = "http://github.com/mbr/shutilwhich"

LICENSE = "PSF"
LIC_FILES_CHKSUM = "file://PKG-INFO;md5=29a00402e8ebb60f3711b66fe4db4b44"

inherit pypi setuptools

PYPI_PACKAGE = "shutilwhich"

SRC_URI[md5sum] = "915947c5cdae7afd748ac715ee547adb"
SRC_URI[sha256sum] = "db1f39c6461e42f630fa617bb8c79090f7711c9ca493e615e43d0610ecb64dc6"

BBCLASSEXTEND = "native nativesdk"
