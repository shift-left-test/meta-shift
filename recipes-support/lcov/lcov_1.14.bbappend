FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI += "\
    file://0001-add-demangle-tool-option.patch \
"

DEPENDS += "\
    perl \
    libjson-perl \
    libperlio-gzip-perl \
"

RDEPENDS:${PN} += "\
    gcov-symlinks \
    perl-module-digest-md5 \
    perl-module-file-copy \
"

RDEPENDS:${PN}:class-native += "\
"

BBCLASSEXTEND = "native nativesdk"

do_install:append:class-native() {
    sed -i -e '1s,#!.*perl,#!${USRBINPATH}/env nativeperl,' ${D}${bindir}/*
}

do_install:append:class-nativesdk() {
    sed -i -e '1s,#!.*perl,#!${USRBINPATH}/env perl,' ${D}${bindir}/*
}
