SUMMARY = "Fake Function Framework (fff) for C"
DESCRIPTION = "A testing micro framework for creating function test doubles"
AUTHOR = "Michael Long"
HOMEPAGE = "https://github.com/meekrosoft/fff"
BUGTRACKER = "https://github.com/meekrosoft/fff/issues"
SECTION = "devel"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=ae0c5f671972941881237cb85e1c74b2"

SRC_URI = "git://github.com/meekrosoft/fff.git;protocol=https;nobranch=1"

SRCREV = "995f26b93955601e9a0570faf8f171316edfe055"

S = "${WORKDIR}/git"

ALLOW_EMPTY_${PN} = "1"

FILES_${PN} = "${includedir}"

do_configure() {
    :
}

do_compile() {
    :
}

do_install() {
    install -d ${D}/${includedir}/fff
    install -m 644 ${S}/fff.h ${D}/${includedir}/fff/fff.h
}

BBCLASSEXTEND = "native nativesdk"
