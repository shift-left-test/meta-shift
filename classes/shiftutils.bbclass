inherit qemu

def _get_qemu_options(data, arch):
    bb.debug(1, "TUNE_CCARGS: " + data.getVar("TUNE_CCARGS", True))
    options = data.getVar("QEMU_EXTRAOPTIONS_%s" % arch, True)

    if not options:
        options = bb.utils.contains("TUNE_CCARGS", "-march=core2", " -cpu core2duo", "", data)

    bb.debug(1, "QEMU EXTRA OPTIONS: " + options)
    return options

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

        import string
        qemu_binary = qemu_target_binary(data)
        if qemu_binary == "qemu-allarch":
            qemu_binary = "qemuwrapper"

        qemu_options = _get_qemu_options(data, data.getVar('PACKAGE_ARCH', True))

        return qemu_binary + " " + qemu_options + " -L " + sysroot_dir \
            + " -E LD_LIBRARY_PATH=" + ":".join(library_paths) + " "
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
    
    qemu_options = _get_qemu_options(data, data.getVar('TUNE_PKGARCH', True))

    return qemu_binary + ";" + qemu_options.replace(' ', ';') + ";-L;\$ENV{SDKTARGETSYSROOT}" \
        + ";-E;LD_LIBRARY_PATH=" + ":".join(library_paths)

