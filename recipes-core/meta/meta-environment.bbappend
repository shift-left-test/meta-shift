toolchain_create_sdk_env_script_append() {
    echo 'export OECORE_TARGET_ARCH="${TARGET_ARCH}"' >> $script
    echo 'export QEMU_EXTRAOPTIONS="${QEMU_EXTRAOPTIONS_${TUNE_PKGARCH}}"' >> $script
}
