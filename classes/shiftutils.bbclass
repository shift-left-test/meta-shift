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


def save_metadata(d):
    import json, os
    if not d.getVar("SHIFT_REPORT_DIR", True):
        return ""
    path = d.expand("${SHIFT_REPORT_DIR}/${PF}/metadata.json")
    bb.utils.mkdirhier(os.path.dirname(path))
    with open(path, "w") as f:
        f.write(json.dumps({
            "S": d.getVar("S", True) or "",
            "PWD": os.getcwd(),
        }, indent=2) + "\n")
    return ""


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


def shiftutils_get_branch_coverage_option(data, tool) :
    flag = 1 if bb.utils.to_boolean(data.getVar("SHIFT_COVERAGE_BRANCH", True)) else 0
    return "--rc {}_branch_coverage={}".format(tool, flag)
