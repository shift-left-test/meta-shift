do_install_append_class-nativesdk () {
    sed -i -E "s|(export .*)|\1 PYTHONNOUSERSITE=1|g" ${D}${bindir}/python2.7
}
