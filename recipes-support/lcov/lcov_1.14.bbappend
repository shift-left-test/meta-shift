FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://0001-add-demangle-tool-option.patch"

DEPENDS += "perl"

RDEPENDS_${PN}_class-native = "\
    perl-module-digest-sha-native \
    perl-module-filehandle-native \
    perl-module-getopt-std-native \
    perl-native \
"

RDEPENDS_${PN}_class-nativesdk = "\
    nativesdk-perl \
    nativesdk-perl-module-digest-md5 \
    nativesdk-perl-module-digest-sha \
    nativesdk-perl-module-filehandle \
    nativesdk-perl-module-file-spec-functions \
    nativesdk-perl-module-file-temp \
    nativesdk-perl-module-file-find \
    nativesdk-perl-module-getopt-std \
    nativesdk-perl-module-getopt-long \
"

BBCLASSEXTEND = "native nativesdk"

do_install_class-native() {
    oe_runmake install PREFIX=${D}${prefix} CFG_DIR=${D}${sysconfdir}
    sed -i -e '1s,#!.*perl,#!${USRBINPATH}/env nativeperl,' ${D}${bindir}/*
}

do_install_class-nativesdk() {
    oe_runmake install PREFIX=${D}${prefix} CFG_DIR=${D}${sysconfdir}
    sed -i -e '1s,#!.*perl,#!${USRBINPATH}/env perl,' ${D}${bindir}/*
}
