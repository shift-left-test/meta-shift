inherit qemu


def debug(s, level=1):
    bb.debug(level, s)


def plain(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.plain(d.expand("${PF} do_${BB_CURRENTTASK}: ") + s)


def warn(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.warn(s)


def error(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.error(s)


def fatal(s, d):
    if d.getVar("SHIFT_SUPPRESS_OUTPUT", True):
        return
    bb.fatal(s)


def isNativeCrossSDK(pn):
    return pn.startswith("nativesdk-") or "-cross-" in pn or "-crosssdk" in pn or pn.endswith("-native")


def shlex_split(s):
    import shlex
    return shlex.split(s)


def mkdirhier(path, clean=False):
    if clean and os.path.exists(path):
        debug("Removing the existing directory: %s" % path)
        bb.utils.remove(path, True)
    bb.utils.mkdirhier(path)


def find_files(directory, pattern):
    import fnmatch
    found = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                found.append(os.path.join(root, filename))
    return found


def replace_files(files, pattern, repl):
    import fileinput
    import re
    for filename in files:
        debug("Replacing contents: %s" % filename)
        for line in fileinput.input(filename, inplace=True):
            print(re.sub(pattern, repl, line).rstrip())


def readlines(path):
    import io
    with io.open(path, "r", encoding="utf-8") as f:
        for line in f.read().splitlines():
            yield line


def exec_func(func, d, verbose=True, timeout=0):
    try:
        cwd = os.getcwd()
        dd = d.createCopy()
        if not verbose:
            dd.setVar("SHIFT_SUPPRESS_OUTPUT", True)
        if timeout > 0:
            dd.setVar("SHIFT_TIMEOUT", timeout)
        lockfiles = dd.getVarFlag(func, "lockfiles", True) or ""
        lockfile = dd.expand("${S}/singletask.lock")
        if lockfile in lockfiles:
            lockfiles = lockfiles.replace(lockfile, dd.expand("${S}/%s_singletask.lock" % func))
            dd.setVarFlag(func, "lockfiles", lockfiles)
        bb.build.exec_func(func, dd)
    finally:
        os.chdir(cwd)


def timeout(func, cmd, d, **options):
    if not isinstance(cmd, str):
        cmd = " ".join(map(str, cmd))

    period = d.getVar("SHIFT_TIMEOUT", True) or None
    if period and not cmd.startswith("timeout"):
        cmd = "timeout %s %s" % (period, cmd)

    return func(cmd, d, **options)


def check_call(cmd, d, **options):
    if not "shell" in options:
        options["shell"] = True

    if not isinstance(cmd, str):
        cmd = " ".join(map(str, cmd))

    debug('Executing: "%s"' % cmd)
    import subprocess
    try:
        subprocess.check_call(cmd, **options)
    except subprocess.CalledProcessError as e:
        raise bb.process.ExecutionError(cmd, e.returncode, None, None)


def exec_proc(cmd, d, **options):
    import subprocess

    class Popen(bb.process.Popen):
        defaults = {
            "stdout": subprocess.PIPE,
            "stderr": None,
            "stdin": None,
            "shell": True,
        }

        def __init__(self, *args, **kwargs):
            options = dict(self.defaults)
            options.update(kwargs)
            bb.process.Popen.__init__(self, *args, **options)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, value, traceback):
            if self.stdout:
                self.stdout.close()
            if self.stderr:
                self.stderr.close()

    if not isinstance(cmd, str):
        cmd = " ".join(map(str, cmd))

    debug('Executing: "%s"' % cmd)
    with Popen(cmd, **options) as proc:
        for line in proc.stdout:
            plain(line.decode("utf-8").rstrip(), d)

        proc.wait()
        if proc.returncode != 0:
            raise bb.process.ExecutionError(cmd, proc.returncode, None, None)


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
        sysroot_destdir = data.getVar('SYSROOT_DESTDIR', True)

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


def save_as_json(dictionary, path):
    import json
    with open(path, "w") as f:
        f.write(json.dumps(dictionary, indent=2) + "\n")


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
        '\$ENV{SDKTARGETSYSROOT}' + data.getVar('libdir_nativesdk', True),
        '\$ENV{SDKTARGETSYSROOT}' + data.getVar('base_libdir_nativesdk', True),
        '\$LD_LIBRARY_PATH'
    ]

    qemu_options = _get_qemu_options(data, data.getVar('TUNE_PKGARCH', True))

    return qemu_binary + ";" + qemu_options.replace(' ', ';') + ";-L;\$ENV{SDKTARGETSYSROOT}" \
        + ";-E;LD_LIBRARY_PATH=" + ":".join(library_paths)
