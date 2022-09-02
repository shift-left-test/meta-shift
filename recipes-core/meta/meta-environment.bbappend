toolchain_create_sdk_env_script:append() {
    echo 'export QEMU_EXTRAOPTIONS="${@d.getVar("QEMU_EXTRAOPTIONS_%s" % d.getVar("TUNE_PKGARCH", True), True) or ""}"' >> $script
}
