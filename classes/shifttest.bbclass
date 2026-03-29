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

addtask report after do_compile
do_report[nostamp] = "1"
do_report[doc] = "Generates reports for the target"

shifttest_do_report() {
    :
}

def shifttest_report(d, tasks=["test", "coverage", "checktest"]):
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    if not d.getVar("SHIFT_REPORT_DIR", True):
        warn("SHIFT_REPORT_DIR is not set. No reports will be generated.", d)

    dd = d.createCopy()

    if "test" in tasks:
        dd.setVar("BB_CURRENTTASK", "test")
        exec_func("do_test", dd)

    if "coverage" in tasks:
        dd.setVar("BB_CURRENTTASK", "coverage")
        exec_func("do_coverage", dd)

    if "checktest" in tasks:
        if "clang-layer" in dd.getVar("BBFILE_COLLECTIONS", True).split():
            dd.setVar("BB_CURRENTTASK", "checktest")
            exec_func("do_checktest", dd)
        else:
            plain("Skipping do_checktest because there is no clang-layer", dd)


python() {
    if d.getVar("SHIFT_TIMEOUT", True):
        fatal("You cannot use SHIFT_TIMEOUT as it is internal to shifttest.bbclass.", d)

    # Synchronize the tasks
    if not bb.utils.to_boolean(d.getVar("SHIFT_PARALLEL_TASKS", True)):
        d.appendVarFlag("do_test", "lockfiles", "${TMPDIR}/do_test.lock")
        d.appendVarFlag("do_coverage", "lockfiles", "${TMPDIR}/do_coverage.lock")
        d.appendVarFlag("do_checktest", "lockfiles", "${TMPDIR}/do_checktest.lock")
        d.appendVarFlag("do_report", "lockfiles", "${TMPDIR}/do_report.lock")
}
