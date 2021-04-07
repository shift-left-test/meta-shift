SUMMARY = "Advanced oelint"
DESCRIPTION = "Advanced oelint"
AUTHOR = "Sangmo.kang"
HOMEPAGE = "http://mod.lge.com/hub/yocto/addons/oelint-adv"
BUGTRACKER = "http://mod.lge.com/hub/yocto/addons/oelint-adv/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=5445ee55866227a2eaf17ebe47250e09 \
                    file://oelint_adv/LICENSE;md5=e926c89aceef6c1a4247d5df08f94533"

SRC_URI = "git://mod.lge.com/hub/yocto/addons/oelint-adv.git;protocol=http;nobranch=1"
SRCREV = "31dd843dab251333d9278413fd51aaeff65435bb"

S = "${WORKDIR}/git"

inherit setuptools3

BBCLASSEXTEND = "native nativesdk"

