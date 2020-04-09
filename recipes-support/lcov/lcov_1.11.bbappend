DEPENDS += "\
    perl \
"

RDEPENDS_${PN}_class-native = " \
    perl-native \
    perl-module-filehandle-native \
    perl-module-getopt-std-native \
    perl-module-digest-sha-native \
"

RDEPENDS_${PN}_class-nativesdk = " \
    nativesdk-perl \
    nativesdk-perl-module-filehandle \
    nativesdk-perl-module-getopt-std \
    nativesdk-perl-module-digest-sha \
    nativesdk-perl-module-digest-md5 \
    nativesdk-perl-module-file-temp \
    nativesdk-perl-module-file-spec-functions \
"

BBCLASSEXTEND = "native nativesdk"

do_install_class-native() {
    oe_runmake install PREFIX=${D}${STAGING_DIR_NATIVE}
    sed -i -e '1s,#!.*perl -w,#!${USRBINPATH}/env nativeperl,' ${D}${bindir}/*
}

do_install_class-nativesdk() {
    oe_runmake install PREFIX=${D}${base_prefix}
    sed -i -e '1s,#!.*perl -w,#!${USRBINPATH}/env perl,' ${D}${bindir}/*
}