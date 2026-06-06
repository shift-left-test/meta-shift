inherit shiftutils


DEBUG_BUILD:class-target = "1"

addtask test after do_compile
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

shifttest_do_test() {
    :
}

addtask coverage after do_compile
do_coverage[nostamp] = "1"
do_coverage[doc] = "Measures code coverage for the target"

shifttest_do_coverage() {
    :
}

addtask checktest after do_compile
do_checktest[nostamp] = "1"
do_checktest[doc] = "Runs mutation tests for the target"

shifttest_do_checktest() {
    :
}

addtask verify after do_compile
do_verify[nostamp] = "1"
do_verify[doc] = "Runs test, coverage, and mutation tasks for the target"

def shifttest_verify(d, tasks=None):
    if tasks is None:
        tasks = ["test", "coverage", "checktest"]

    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        bb.warn(d.expand("${PF}: Unsupported class type of the recipe"))
        return

    if not d.getVar("SHIFT_REPORT_DIR", True):
        bb.warn(d.expand("${PF}: SHIFT_REPORT_DIR is not set. No reports will be generated."))

    for task in tasks:
        if task == "checktest" and "clang-layer" not in (d.getVar("BBFILE_COLLECTIONS", True) or "").split():
            bb.plain(d.expand("${PF} do_checktest: Skipping do_checktest because there is no clang-layer"))
            continue
        dd = d.createCopy()
        dd.setVar("BB_CURRENTTASK", task)
        # exec_func only writes the ${T}/run.do_<task> symlink (which sentinel
        # uses as --test-command) when BB_RUNTASK matches the function name.
        dd.setVar("BB_RUNTASK", "do_" + task)
        # externalsrc adds ${S}/singletask.lock to every task; do_verify already
        # holds it, so give the nested task its own lock to avoid self-deadlock.
        func = "do_" + task
        lockfiles = dd.getVarFlag(func, "lockfiles", True) or ""
        src_lock = dd.expand("${S}/singletask.lock")
        if src_lock in lockfiles:
            dd.setVarFlag(func, "lockfiles", lockfiles.replace(src_lock, dd.expand("${S}/%s_singletask.lock" % func)))
        bb.build.exec_func(func, dd)

python shifttest_do_verify() {
    shifttest_verify(d)
}

EXPORT_FUNCTIONS do_verify


shiftutils_stream_plain() {
    while IFS= read -r line; do
        bbplain "${PF} do_${BB_CURRENTTASK}: ${line}"
    done
}

# Raise a build error when a test runner exits non-zero, unless the recipe set
# SHIFT_TEST_SUPPRESS_FAILURES.
shifttest_handle_test_rc() {
    if [ "$1" -ne 0 ] && ! ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_SUPPRESS_FAILURES')) else 'false'}; then
        bberror "$2 failed with exit code $1"
    fi
}

python() {
    # Native/cross/SDK recipes have no unit-test surface, so mark their shift
    # tasks no-op.
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        for task in ("do_test", "do_coverage", "do_checktest", "do_verify"):
            d.setVarFlag(task, "noexec", "1")

    if not bb.utils.to_boolean(d.getVar("SHIFT_PARALLEL_TASKS", True)):
        for task in ("do_test", "do_coverage", "do_checktest", "do_verify"):
            d.appendVarFlag(task, "lockfiles", "${TMPDIR}/%s.lock" % task)
}
