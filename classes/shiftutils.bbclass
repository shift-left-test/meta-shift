inherit qemu


def isNativeCrossSDK(pn):
    return pn.startswith("nativesdk-") or "-cross-" in pn or "-crosssdk" in pn or pn.endswith("-native")


def shiftutils_cli_opt(d, var, flag):
    v = d.getVar(var)
    return "{}={}".format(flag, v) if v else ""


def shiftutils_cli_bool(d, var, flag):
    return flag if bb.utils.to_boolean(d.getVar(var)) else ""


def shiftutils_cli_multi(d, var, flag):
    return " ".join("{}={}".format(flag, x) for x in (d.getVar(var) or "").split())


def shiftutils_qemu_set_env(d):
    # QEMU_SET_ENV wants comma-separated VAR=VALUE; the variable is space-separated.
    return ",".join((d.getVar("SHIFT_TEST_QEMU_SET_ENV") or "").split())


def _get_qemu_options(data, arch):
    bb.debug(1, "TUNE_CCARGS: " + data.getVar("TUNE_CCARGS", True))
    options = data.getVar("QEMU_EXTRAOPTIONS_%s" % arch, True)

    if not options:
        options = bb.utils.contains("TUNE_CCARGS", "-march=core2", " -cpu core2duo", "", data)

    bb.debug(1, "QEMU EXTRA OPTIONS: " + options)
    return options


def shiftutils_qemu_run_cmd(data):
    sysroot_dir = data.getVar('STAGING_DIR_TARGET', True)
    if sysroot_dir:
        libdir = data.getVar('libdir', True)
        base_libdir = data.getVar('base_libdir', True)
        library_paths = [
            sysroot_dir + libdir,
            sysroot_dir + base_libdir
        ]

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
