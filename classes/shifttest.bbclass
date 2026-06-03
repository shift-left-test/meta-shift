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

def shifttest_report(d, tasks=None):
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
        # Make bb.build.exec_func treat this call as if do_<task> were the
        # top-level task: it writes ${T}/run.do_<task>.<PID> AND creates the
        # ${T}/run.do_<task> symlink (only when BB_RUNTASK == func). Without
        # this, sentinel cannot find ${T}/run.do_test as its --test-command.
        dd.setVar("BB_RUNTASK", "do_" + task)
        # In devtool/externalsrc env, externalsrc.bbclass adds
        # ${S}/singletask.lock to every task. do_verify already holds that
        # lock, so the nested exec_func call would self-deadlock. Rewrite to
        # a task-specific path so the sub-task takes a different lock.
        func = "do_" + task
        lockfiles = dd.getVarFlag(func, "lockfiles", True) or ""
        src_lock = dd.expand("${S}/singletask.lock")
        if src_lock in lockfiles:
            dd.setVarFlag(func, "lockfiles",
                          lockfiles.replace(src_lock, dd.expand("${S}/%s_singletask.lock" % func)))
        bb.build.exec_func(func, dd)

python shifttest_do_verify() {
    shifttest_report(d)
}

EXPORT_FUNCTIONS do_verify


shiftutils_stream_plain() {
    while IFS= read -r line; do
        bbplain "${PF} do_${BB_CURRENTTASK}: ${line}"
    done
}

python() {
    # Native/cross/SDK recipes have no meaningful unit-test surface; mark all
    # shift tasks no-op to avoid the boilerplate `case "${PN}" in nativesdk-*|...`
    # guard previously duplicated in every shell function.
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        for task in ("do_test", "do_coverage", "do_checktest", "do_verify"):
            d.setVarFlag(task, "noexec", "1")

    if not bb.utils.to_boolean(d.getVar("SHIFT_PARALLEL_TASKS", True)):
        d.appendVarFlag("do_test", "lockfiles", "${TMPDIR}/do_test.lock")
        d.appendVarFlag("do_coverage", "lockfiles", "${TMPDIR}/do_coverage.lock")
        d.appendVarFlag("do_checktest", "lockfiles", "${TMPDIR}/do_checktest.lock")
        d.appendVarFlag("do_verify", "lockfiles", "${TMPDIR}/do_verify.lock")
}
