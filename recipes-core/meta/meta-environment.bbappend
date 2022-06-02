toolchain_create_sdk_env_script:append() {
    echo 'export QEMU_EXTRAOPTIONS="${QEMU_EXTRAOPTIONS_${TUNE_PKGARCH}}"' >> $script
}

