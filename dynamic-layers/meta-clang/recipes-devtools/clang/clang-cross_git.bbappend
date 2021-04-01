python() {
    # Fixes the "Manifest file not found in x86_64_x86_64 (variant '')?" error message
    # by creating a manifest file which seems to be never used by the bitbake process.
    manifest = d.expand("${SSTATE_MANIFESTS}/manifest-${BUILD_ARCH}_${BUILD_ARCH}-${PN}.%s" % "populate_sysroot")
    if not os.path.exists(manifest):
        bb.utils.mkdirhier(os.path.dirname(manifest))
        os.mknod(manifest)
}
