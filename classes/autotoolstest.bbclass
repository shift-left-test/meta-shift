inherit autotools
inherit shifttest
inherit shiftutils

do_configure_prepend() {
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

do_configure_append() {
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
    bb.build.exec_func("shifttest_do_checkcode", d)
}

python autotoolstest_do_test() {
    dd = d.createCopy()
    env = os.environ.copy()

    # Set up the test runner
    env["LOG_COMPILER"] = dd.expand("${WORKDIR}/test-runner.sh")

    configured = dd.getVar("SHIFT_REPORT_DIR", True)

    if configured:
        report_dir = dd.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        mkdirhier(report_dir, True)

        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir

    # Prepare for the coverage reports
    check_call(["lcov", "-c", "-i",
                "-d", dd.getVar("B", True),
                "-o", dd.expand("${B}/coverage_base.info"),
                "--ignore-errors", "gcov",
                "--gcov-tool", dd.expand("${TARGET_PREFIX}gcov"),
                "--rc", "lcov_branch_coverage=1"], dd)

    try:
        timeout(check_call ,"make check", dd, env=env, cwd=dd.getVar("B", True))
    except bb.process.ExecutionError as e:
        if e.exitcode == 124:
            raise e
        pass

    # Print test logs
    for f in find_files(dd.getVar("B", True), "test-suite.log"):
        for line in readlines(f):
            plain(line, dd)

    if configured:
        if os.path.exists(report_dir):
            # Prepend the package name to each of the classname tags for GTest reports
            xml_files = find_files(report_dir, "*.xml")
            replace_files(xml_files, 'classname="', dd.expand('classname="${PN}.'))
        else:
            warn("No test report files found at %s" % report_dir, dd)
}

python autotoolstest_do_coverage() {
    bb.build.exec_func("shifttest_do_coverage", d)
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage
