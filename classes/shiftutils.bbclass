inherit qemu

def shiftutils_qemu_run_cmd(data):
    sysroot_dir = data.getVar('STAGING_DIR_TARGET', False)
    if sysroot_dir:
        libdir = data.getVar('libdir', False)
        base_libdir = data.getVar('base_libdir', False)
        library_paths = [
            sysroot_dir + libdir,
            sysroot_dir + base_libdir
        ]
        sysroot_destdir = data.getVar('SYSROOT_DESTDIR', False)
        
        if sysroot_destdir:
            library_paths.append(sysroot_destdir + libdir)
            library_paths.append(sysroot_destdir + base_libdir)
        library_paths.append('\$LD_LIBRARY_PATH')

        return qemu_wrapper_cmdline(data, sysroot_dir, library_paths).replace('PSEUDO_UNLOAD=1 ', '')
    else:
        return ""

def shiftutils_qemu_cmake_emulator(data):
    return shiftutils_qemu_run_cmd(data).replace(' ', ';')

def shiftutils_qemu_cmake_emulator_sdktarget(data):
    target_arch = data.getVar("TUNE_ARCH", True)
    if target_arch in ("i486", "i586", "i686"):
        target_arch = "i386"
    elif target_arch == "powerpc":
        target_arch = "ppc"
    elif target_arch == "powerpc64":
        target_arch = "ppc64"

    import string

    qemu_binary = "qemu-" + target_arch
    if qemu_binary == "qemu-allarch":
        qemu_binary = "qemuwrapper"

    library_paths = [
        '\$ENV{SDKTARGETSYSROOT}' + data.getVar('libdir_nativesdk', False),
        '\$ENV{SDKTARGETSYSROOT}' + data.getVar('base_libdir_nativesdk', False), 
        '\$LD_LIBRARY_PATH'
    ]
    
    qemu_options = (data.getVar("QEMU_EXTRAOPTIONS_%s" % data.getVar('TUNE_PKGARCH', True), True) or "").replace(' ', ';')

    return qemu_binary + ";" + qemu_options + ";-L;\$ENV{SDKTARGETSYSROOT}" \
        + ";-E;LD_LIBRARY_PATH=" + ":".join(library_paths)

