# To fix the nativesdk recipe shebang path bug of distutils for Yocto morty
do_install_append_class-nativesdk() {
    for i in ${D}${bindir}/* ; do \
        sed -i -e s:${bindir}/env:${USRBINPATH}/env:g $i
    done
}
