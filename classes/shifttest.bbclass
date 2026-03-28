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

addtask checkcache after do_build
do_checkcache[nostamp] = "1"
do_checkcache[doc] = "Check cache availability of the recipe"

shifttest_do_checkcache() {
    :
}

def shifttest_checkcache(d):
    def make_plain_report(print_list):
        def newline(new_str=""):
            return "%s\n" % new_str

        ret = ""
        for title, found, missed in print_list:
            wanted = len(found) + len(missed)
            ret += newline(title)
            ret += newline("-" * len(title))
            if wanted != 0:
                ret += newline("Wanted : %d (%d%%)" % (wanted, 100 * wanted / wanted))
                ret += newline("Found  : %d (%d%%)" % (len(found), 100 * len(found) / wanted))
                ret += newline("Missed : %d (%d%%)" % (len(missed), 100 * len(missed) / wanted))
            else:
                ret += newline("Wanted : %d (-%%)" % (wanted))
                ret += newline("Found  : %d (-%%)" % (len(found)))
                ret += newline("Missed : %d (-%%)" % (len(missed)))
            ret += newline()

        return ret

    def make_json_report(print_list):
        import json
        json_dict = dict()

        for title, found, missed in print_list:
            json_dict[title] = dict()
            json_dict[title]["Summary"] = dict()
            json_dict[title]["Summary"]["Wanted"] = len(found) + len(missed)
            json_dict[title]["Summary"]["Found"] = len(found)
            json_dict[title]["Summary"]["Missed"] = len(missed)
            json_dict[title]["Found"] = [str(x) for x in found]
            json_dict[title]["Missed"] = [str(x) for x in missed]

        return json.dumps(json_dict, indent=2) + "\n"

    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    if "checkcache" not in str(d.getVar("INHERIT", True)):
        fatal("The task needs to inherit checkcache", d)

    found_sstate, missed_sstate = shiftutils_get_sstate_availability(d)
    found_source, missed_source = shiftutils_get_source_availability(d)

    plain_report_str = str(make_plain_report([("Shared State Availability", found_sstate, missed_sstate), ("Source Availability", found_source, missed_source)]))

    for splited in plain_report_str.splitlines():
        plain(splited, d)

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcache")
        mkdirhier(report_dir, True)

        save_metadata(d)

        with open(os.path.join(report_dir, "caches.json"), "w") as f:
            f.write(make_json_report([("Shared State", found_sstate, missed_sstate), ("Premirror", found_source, missed_source)]))


addtask report after do_compile
do_report[nostamp] = "1"
do_report[doc] = "Generates reports for the target"

shifttest_do_report() {
    :
}

def shifttest_report(d, tasks=["test", "coverage", "checkcache", "checktest"]):
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

    if "checkcache" in tasks:
        if "checkcache" in str(dd.getVar("INHERIT", True)):
            dd.setVar("BB_CURRENTTASK", "checkcache")
            exec_func("do_checkcache", dd)
        else:
            plain("Skipping do_checkcache because checkcache is not inherited", dd)

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
        d.appendVarFlag("do_checkcache", "lockfiles", "${TMPDIR}/do_checkcache.lock")
        d.appendVarFlag("do_report", "lockfiles", "${TMPDIR}/do_report.lock")
}
