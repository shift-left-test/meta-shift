inherit qemu


def debug(s, level=1):
    bb.debug(level, s)


def plain(s, d):
    bb.plain(d.expand("${PF} do_${BB_CURRENTTASK}: ") + s)


def warn(s, d):
    bb.warn(d.expand("${PF} do_${BB_CURRENTTASK}: ") + s)


def error(s, d):
    bb.error(d.expand("${PF} do_${BB_CURRENTTASK}: ") + s)


def fatal(s, d):
    bb.fatal(d.expand("${PF} do_${BB_CURRENTTASK}: ") + s)


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


def exec_func(func, d):
    try:
        cwd = os.getcwd()
        dd = d.createCopy()
        lockfiles = dd.getVarFlag(func, "lockfiles", True) or ""
        lockfile = dd.expand("${S}/singletask.lock")
        if lockfile in lockfiles:
            lockfiles = lockfiles.replace(lockfile, dd.expand("${S}/%s_singletask.lock" % func))
            dd.setVarFlag(func, "lockfiles", lockfiles)
        bb.build.exec_func(func, dd)
    finally:
        os.chdir(cwd)


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
    debug("TUNE_CCARGS: " + data.getVar("TUNE_CCARGS", True))
    options = data.getVar("QEMU_EXTRAOPTIONS_%s" % arch, True)

    if not options:
        options = bb.utils.contains("TUNE_CCARGS", "-march=core2", " -cpu core2duo", "", data)

    debug("QEMU EXTRA OPTIONS: " + options)
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


def shiftutils_get_source_availability(d):
    taskdepdata = d.getVar("BB_TASKDEPDATA", False)

    total_depends = set()
    if taskdepdata:
        for td in taskdepdata:
            dep = taskdepdata[td][0]
            if dep:
                total_depends.add(dep)

    found_source = list()
    missed_source = list()

    for dep in total_depends:
        try:
            path = d.expand("${TOPDIR}/checkcache/%s" % dep)

            with open(os.path.join(path,"source_availability"), "r") as f:
                source_availability = f.read()
                if source_availability == "True":
                    found_source.append(dep)
                elif source_availability == "False":
                    missed_source.append(dep)
                else:
                    raise Exception("Unknown Value(%s)" % source_availability)

        except Exception as e:
            debug("Failed to read source_availability of %s:%s" % (dep, str(e)))

    found_source.sort()
    missed_source.sort()

    return found_source, missed_source

shiftutils_get_source_availability[vardepsexclude] += "BB_TASKDEPDATA"

def shiftutils_get_sstate_availability(d, siginfo=False):
    # migration from poky/meta/classes/sstate.bbclass::sstate_checkhashes

    mirrors = d.getVar("SSTATE_MIRRORS", True)
    if not mirrors:
        bb.warn("Skipping check Shared State Availability because SSTATE_MIRRORS is not set.")
        return list(), list()

    if bb.utils.to_boolean(d.getVar('BB_NO_NETWORK', True)):
        bb.warn("Skipping check Shared State Availability because BB_NO_NETWORK is set.")
        return list(), list()

    sq_data = {"hash": dict(), "unihash": dict(), "hashfn": dict(), "fn_task": dict()}

    sstatetasks = str(d.getVar("SSTATETASKS", True)).split()

    taskdepdata = d.getVar("BB_TASKDEPDATA", False)
    if taskdepdata:
        for td in taskdepdata:
            if taskdepdata[td][1] in sstatetasks:
                dep = taskdepdata[td][0]
                try:
                    path = d.expand("${TOPDIR}/checkcache/%s" % dep)

                    with open(os.path.join(path,"hashfilename"), "r") as f:
                        hashfilename = str(f.read())
                except Exception as e:
                    debug("Failed to read hashfilename of %s:%s" % (dep, str(e)))
                else:
                    sq_data["hashfn"][td] = hashfilename
                    sq_data["hash"][td] = taskdepdata[td][5]
                    try:
                        sq_data["unihash"][td] = taskdepdata[td][6]
                    except:
                        sq_data["unihash"][td] = None
                    sq_data["fn_task"][td] = "%s:%s" % (taskdepdata[td][0], taskdepdata[td][1])


    currentcount = 0

    found = set()
    missed = set()
    extension = ".tgz"
    if siginfo:
        extension = extension + ".siginfo"

    def gethash(task):
        if sq_data['unihash'][task]:
            return sq_data['unihash'][task]
        return sq_data['hash'][task]

    def getpathcomponents(task, d):
        # Magic data from BB_HASHFILENAME
        splithashfn = sq_data['hashfn'][task].split(" ")
        spec = splithashfn[1]
        if splithashfn[0] == "True":
            extrapath = d.getVar("NATIVELSBSTRING", True) + "/"
        else:
            extrapath = ""

        tname = bb.runqueue.taskname_from_tid(task)[3:]

        if tname in ["fetch", "unpack", "patch", "populate_lic", "preconfigure"] and splithashfn[2]:
            spec = splithashfn[2]
            extrapath = ""

        return spec, extrapath, tname

    if mirrors:
        # Copy the data object and override DL_DIR and SRC_URI
        localdata = bb.data.createCopy(d)

        import tempfile
        tmp_dldir = tempfile.mkdtemp(prefix="checkcache-tempdir-")

        localdata.delVar('MIRRORS')
        localdata.setVar('FILESPATH', tmp_dldir)
        localdata.setVar('DL_DIR', tmp_dldir)
        localdata.setVar('PREMIRRORS', mirrors)

        bb.debug(2, "SState using premirror of: %s" % mirrors)

        # if BB_NO_NETWORK is set but we also have SSTATE_MIRROR_ALLOW_NETWORK,
        # we'll want to allow network access for the current set of fetches.
        if bb.utils.to_boolean(localdata.getVar('BB_NO_NETWORK', True)) and \
                bb.utils.to_boolean(localdata.getVar('SSTATE_MIRROR_ALLOW_NETWORK', True)):
            localdata.delVar('BB_NO_NETWORK')

        from bb.fetch2 import FetchConnectionCache
        def checkstatus_init(thread_worker):
            thread_worker.connection_cache = FetchConnectionCache()

        def checkstatus_end(thread_worker):
            thread_worker.connection_cache.close_connections()

        def checkstatus(thread_worker, arg):
            (tid, sstatefile) = arg

            localdata2 = bb.data.createCopy(localdata)
            srcuri = "file://" + sstatefile
            localdata.setVar('SRC_URI', srcuri)
            bb.debug(2, "SState: Attempting to fetch %s" % srcuri)

            try:
                fetcher = bb.fetch2.Fetch(srcuri.split(), localdata2,
                            connection_cache=thread_worker.connection_cache)
                fetcher.checkstatus()
                bb.debug(2, "SState: Successful fetch test for %s" % srcuri)
                found.add(tid)
                if tid in missed:
                    missed.remove(tid)
            except:
                missed.add(tid)
                bb.debug(2, "SState: Unsuccessful fetch test for %s" % srcuri)
                pass

        tasklist = []
        for tid in sq_data['hash']:
            if tid in found:
                continue
            spec, extrapath, tname = getpathcomponents(tid, d)
            sstatefile = d.expand(extrapath + generate_sstatefn(spec, gethash(tid), d) + "_" + tname + extension)
            tasklist.append((tid, sstatefile))

        if tasklist:
            import multiprocessing
            nproc = min(multiprocessing.cpu_count(), len(tasklist))

            bb.event.enable_threadlock()
            pool = oe.utils.ThreadedPool(nproc, len(tasklist),
                    worker_init=checkstatus_init, worker_end=checkstatus_end)
            for t in tasklist:
                pool.add_task(checkstatus, t)
            pool.start()
            pool.wait_completion()
            bb.event.disable_threadlock()
        try:
            bb.utils.remove(tmp_dldir, True)
        except:
            pass

    found = list(found)
    found = [sq_data['fn_task'][x] for x in found]
    found.sort()
    missed = list(missed)
    missed = [sq_data['fn_task'][x] for x in missed]
    missed.sort()

    return found, missed

shiftutils_get_sstate_availability[vardepsexclude] += "BB_TASKDEPDATA NATIVELSBSTRING"

def shiftutils_get_branch_coverage_option(data, tool) :
    flag = 1 if bb.utils.to_boolean(data.getVar("SHIFT_COVERAGE_BRANCH", True)) else 0
    return "--rc {}_branch_coverage={}".format(tool, flag)
