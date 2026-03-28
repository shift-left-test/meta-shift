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
    import io
    import re
    for filename in files:
        debug("Replacing contents: %s" % filename)
        with io.open(filename, "r+", encoding="utf-8", errors="replace") as f:
            data = f.read()
            f.seek(0)
            f.write(re.sub(pattern, repl, data))
            f.truncate()


def readlines(path):
    import io
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
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
    import select

    class Popen(bb.process.Popen):
        defaults = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
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
        stdout_eof = not bool(proc.stdout)
        stderr_eof = not bool(proc.stderr)

        if stderr_eof:
            stderr_str = None
        else:
            stderr_str = ""

        select_target = []

        if not stdout_eof:
            select_target.append(proc.stdout)

        if not stderr_eof:
            select_target.append(proc.stderr)

        while not stdout_eof or not stderr_eof:
            proc.poll()
            ready = select.select(select_target, [], [], 1.0)
            if not stdout_eof and proc.stdout in ready[0]:
                buf = proc.stdout.readline()
                stdout_eof = len(buf) == 0
                if not stdout_eof:
                    plain(buf.decode("utf-8", errors="replace").rstrip(), d)

            if not stderr_eof and proc.stderr in ready[0]:
                buf = proc.stderr.readline()
                stderr_eof = len(buf) == 0
                if not stderr_eof:
                    stderr_str += buf.decode("utf-8", errors="replace")

        proc.wait()
        if proc.returncode != 0:
            raise bb.process.ExecutionError(cmd, proc.returncode, None, stderr_str)


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


def save_as_json(dictionary, path):
    import json
    with open(path, "w") as f:
        f.write(json.dumps(dictionary, indent=2) + "\n")


def save_metadata(d):
    metadata = {
        "S": d.getVar("S", True) or "",
        "PWD": os.getcwd(),
    }
    save_as_json(metadata, d.expand("${SHIFT_REPORT_DIR}/${PF}/metadata.json"))


def shiftutils_qemu_cmake_emulator(data):
    return shiftutils_qemu_run_cmd(data).replace(' ', ';')


def shiftutils_get_coverage_info(data, coverage_file) :
    coverage_info = dict()
    if os.path.exists(coverage_file):
        current_file = ""
        with open(coverage_file, "r") as f:
            for line in f.read().splitlines():
                if line.startswith("SF"):
                    current_file = line.split(":")[1]
                    coverage_info[current_file] = list()

                if line.startswith("DA"):
                    v = line.split(":")[1].split(",")
                    if v[1] != "0":
                        coverage_info[current_file].append(v[0])
    else:
        warn("No coverage info file generated at %s" % coverage_file, data)

    return coverage_info

def shiftutils_get_branch_coverage_option(data, tool) :
    flag = 1 if bb.utils.to_boolean(data.getVar("SHIFT_COVERAGE_BRANCH", True)) else 0
    return "--rc {}_branch_coverage={}".format(tool, flag)

def del_stamp(taskname, d):
    stamp = d.getVar('STAMP')
    if not stamp:
        return

    taskflagname = taskname
    if taskname.endswith("_setscene"):
        taskflagname = taskname.replace("_setscene", "")

    file_name = d.getVar('BB_FILENAME')
    extrainfo = d.getVarFlag(taskflagname, 'stamp-extra-info')  or ""

    stamp = bb.parse.siggen.stampfile(stamp, file_name, taskname, extrainfo)

    stampdir = os.path.dirname(stamp)
    if bb.parse.cached_mtime_noerror(stampdir) == 0:
        bb.utils.mkdirhier(stampdir)

    bb.utils.remove(stamp)
