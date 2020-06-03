# Since the loading priority of'$HOME/.local python package' is higher than 'usr/lib/python in sysroot', 
# an error may occur in the python script operation deployed in sysroots usr/bin.
# This issue is resolved at 'sumo' branch.

do_install_append_class-nativesdk () {
    sed -i -E "s|(export .*)|\1 PYTHONNOUSERSITE=1|g" ${D}${bindir}/python2.7
}
