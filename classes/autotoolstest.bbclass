inherit cpptest


do_configure:prepend:class-target() {
    # add coverage flags to cxxflags & cflags
    if [ ! -z ${CXXFLAGS+x} ]; then
        export CXXFLAGS_ORI="$CXXFLAGS"
    fi
    export CXXFLAGS="$CXXFLAGS -O0 -fprofile-arcs -ftest-coverage"

    if [ ! -z ${CFLAGS+x} ]; then
        export CFLAGS_ORI="$CFLAGS"
    fi
    export CFLAGS="$CFLAGS -O0 -fprofile-arcs -ftest-coverage"
}

do_configure:append:class-target() {
    # restore environment variables
    if [ ! -z ${CXXFLAGS_ORI+x} ]; then
        export CXXFLAGS="$CXXFLAGS_ORI"
        unset CXXFLAGS_ORI
    else
        unset CXXFLAGS
    fi

    if [ ! -z ${CFLAGS_ORI+x} ]; then
        export CFLAGS="$CFLAGS_ORI"
        unset CFLAGS_ORI
    else
        unset CFLAGS
    fi

    # revert 'automake' new_rt_path_for_test-driver.patch'
    cd ${B}
    find . -name Makefile \
        -exec sed -r -i 's|(top_builddir)(.*test-driver)|top_srcdir\2|g' {} \;

    # create custom log_compiler for qemu usermode return
    {
        echo "if [ -f .libs/""$""1 ]; then"
        echo "    TARGET=.libs/""$""1"
        echo "else"
        echo "    TARGET=""$""1"
        echo "fi"
        echo "${@shiftutils_qemu_run_cmd(d)} ""$""TARGET"
    } > ${WORKDIR}/test-runner.sh

    chmod 755 ${WORKDIR}/test-runner.sh
}

python autotoolstest_do_checkcode() {
    cpptest_checkcode(d)
}

python autotoolstest_do_test() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    env = os.environ.copy()

    # Set up the test runner
    env["LOG_COMPILER"] = d.expand("${WORKDIR}/test-runner.sh")

    # Let tests run in random order
    if bb.utils.to_boolean(d.getVar("SHIFT_TEST_SHUFFLE", True)):
        env["GTEST_SHUFFLE"] = "1"

    configured = d.getVar("SHIFT_REPORT_DIR", True)

    if configured:
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        mkdirhier(report_dir, True)

        save_metadata(d)

        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir

    for gcdaFile in find_files(d.getVar("B", True), "*.gcda"):
        bb.utils.remove(gcdaFile)

    # Prepare for the coverage reports
    check_call(["lcov", "-c", "-i",
                "-d", d.getVar("B", True),
                "-o", d.expand("${B}/coverage_base.info"),
                "--ignore-errors", "gcov",
                "--gcov-tool", d.expand("${TARGET_PREFIX}gcov"),
                shiftutils_get_branch_coverage_option(d, "lcov")], d)

    # Run tests matching regular expression
    if d.getVar("SHIFT_TEST_FILTER", True):
        env["GTEST_FILTER"] = d.getVar("SHIFT_TEST_FILTER", True)

    try:
        timeout(check_call ,"make check", d, env=env, cwd=d.getVar("B", True))
    except bb.process.ExecutionError as e:
        if not bb.utils.to_boolean(d.getVar("SHIFT_TEST_SUPPRESS_FAILURES", True)):
            error(str(e), d)
        if d.getVar("SHIFT_TIMEOUT", True) and e.exitcode == 124:
            err = bb.BBHandledException(e)
            err.exitcode = e.exitcode
            raise err

    # Print test logs
    for f in find_files(d.getVar("B", True), "test-suite.log"):
        for line in readlines(f):
            plain(line, d)

    if configured:
        if os.path.exists(report_dir):
            # Prepend the package name to each of the classname tags for GTest reports
            xml_files = find_files(report_dir, "*.xml")
            replace_files(xml_files, 'classname="', d.expand('classname="${PN}.'))
        else:
            warn("No test report files found at %s" % report_dir, d)
}

python autotoolstest_do_coverage() {
    cpptest_coverage(d)
}

python autotoolstest_do_checktest() {
    cpptest_checktest(d)
}

python autotoolstest_do_checkrecipe() {
    shifttest_checkrecipe(d)
}

python autotoolstest_do_checkcache() {
    shifttest_checkcache(d)
}

python autotoolstest_do_report() {
    shifttest_report(d)
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest do_checkrecipe do_checkcache do_report
