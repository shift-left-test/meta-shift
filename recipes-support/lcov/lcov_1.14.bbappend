FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "\
    file://0001-add-demangle-tool-option.patch \
"

DEPENDS += "\
    perl \
    libjson-perl \
    libperlio-gzip-perl \
"

RDEPENDS_${PN} += "\
    gcov-symlinks \
    perl-module-digest-md5 \
    perl-module-file-copy \
"

RDEPENDS_${PN}_class-native += "\
"

BBCLASSEXTEND = "native nativesdk"

do_install_append_class-native() {
    sed -i -e '1s,#!.*perl,#!${USRBINPATH}/env nativeperl,' ${D}${bindir}/*
}

do_install_append_class-nativesdk() {
    sed -i -e '1s,#!.*perl,#!${USRBINPATH}/env perl,' ${D}${bindir}/*
}
