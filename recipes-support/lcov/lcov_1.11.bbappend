FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://0001-add-demangle-tool-option.patch \
            file://0002-fix-remove-space-loop-warning.patch \
"

DEPENDS += "perl"

RDEPENDS_${PN} += "\
    perl-module-digest-md5 \
    perl-module-file-spec-functions \
    perl-module-file-temp \
    perl-module-file-find \
    perl-module-getopt-long \
"

RDEPENDS_${PN}_class-native = "\
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
