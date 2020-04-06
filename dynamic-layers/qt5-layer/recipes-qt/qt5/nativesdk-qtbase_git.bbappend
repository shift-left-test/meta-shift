do_install_append() {
    mkdir -p ${D}${SDKPATHNATIVE}/environment-setup.d
    
    echo "export QT_PLUGIN_PATH=\"""$""{SDKTARGETSYSROOT}/usr/lib/plugins\"" > ${WORKDIR}/QMakeUtils.sh
    echo "export QML_IMPORT_PATH=\"""$""{SDKTARGETSYSROOT}/usr/lib/qml\"" >> ${WORKDIR}/QMakeUtils.sh
    echo "export QML2_IMPORT_PATH=\"""$""{SDKTARGETSYSROOT}/usr/lib/qml\"" >> ${WORKDIR}/QMakeUtils.sh
    echo "export TESTRUNNER=\"qemu-${TUNE_ARCH} -L ""$""{SDKTARGETSYSROOT}\"" >> ${WORKDIR}/QMakeUtils.sh
    echo "export TESTARGS=\"-platform offscreen\"" >> ${WORKDIR}/QMakeUtils.sh

    install -m 644 ${WORKDIR}/QMakeUtils.sh ${D}${SDKPATHNATIVE}/environment-setup.d/
}