toolchain_create_sdk_env_script_append() {
    echo 'export OECORE_TARGET_ARCH="${TARGET_ARCH}"' >> $script
    echo 'export QEMU_EXTRAOPTIONS="${@d.getVar("QEMU_EXTRAOPTIONS_%s" % d.getVar("TUNE_PKGARCH", True), True) or ""}"' >> $script
}
