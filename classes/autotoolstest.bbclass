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

# $1 : print stdout if "PRINT"
# $2 : report save path
autotoolstest_run_test() {
    PRINT_LINES=$1
    OUTPUT_DIR=$2
    TIMEOUT_STATUS=0

    if [ ! -z "${OUTPUT_DIR}" ]; then
        shifttest_prepare_output_dir ${OUTPUT_DIR}
    fi
    shifttest_prepare_env

    export LOG_COMPILER='${WORKDIR}/test-runner.sh'

    cd ${B}

    # Do not use '-e' option of 'make'.
    local TEST_EXIT_CODE=0
    timeout ${TEST_TIMEOUT} make check || TEST_EXIT_CODE=$?
    if [ "${PRINT_LINES}" = "PRINT" ]; then
        find . -name "test-suite.log" -exec cat {} \; | shifttest_print_lines
    fi

    if [ "$TEST_EXIT_CODE" = "124" ]; then
        TIMEOUT_STATUS=1
        if [ "${PRINT_LINES}" = "PRINT" ]; then
            echo "Test timeout after ${TEST_TIMEOUT} ..." | shifttest_print_lines
        fi
    fi
}

python autotoolstest_do_test() {
    dd = d.createCopy()
    env = os.environ.copy()

    # Set up the test runner
    env["LOG_COMPILER"] = dd.expand("${WORKDIR}/test-runner.sh")

    configured = dd.getVar("TEST_REPORT_OUTPUT", True)

    if configured:
        report_dir = dd.expand("${TEST_REPORT_OUTPUT}/${PF}/test")
        if os.path.exists(report_dir):
            bb.debug(2, "Removing the existing test report directory: %s" % report_dir)
            bb.utils.remove(report_dir, True)
        bb.utils.mkdirhier(report_dir)

        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir

    # Prepare for the coverage reports
    check_call("lcov -c -i " \
               "-d %s " \
               "-o %s " \
               "--ignore-errors %s " \
               "--gcov-tool %s " \
               "--rc %s" % (
                   dd.getVar("B", True),
                   dd.expand("${B}/coverage_base.info"),
                   "gcov",
                   dd.expand("${TARGET_PREFIX}gcov"),
                   "lcov_branch_coverage=1"), dd)

    try:
        check_call("make check", dd, env=env, cwd=dd.getVar("B", True))
    except bb.process.ExecutionError:
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

autotoolstest_do_checktest() {
    if [ ! -z "${CHECKTEST_DISABLED}" ]; then
        bbfatal ${CHECKTEST_DISABLED}
    fi

    shifttest_checktest_prepare
    autotoolstest_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ORIGINAL}

    shifttest_checktest_populate
    cat ${CHECKTEST_WORKDIR}/mutables.db | while read line
    do
        shifttest_checktest_mutate "${line}"
        TEST_STATE="success"
        cd ${B} && do_compile && do_install || TEST_STATE="build_failure"
        if [ "${TEST_STATE}" = "success" ]; then
            rm -rf ${CHECKTEST_WORKDIR_ACTUAL}/*
            autotoolstest_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ACTUAL}
            if [ "$TIMEOUT_STATUS" = "1" ]; then
                TEST_STATE="timeout"
            fi
        else
            bbdebug 1 "build failed"
        fi
        shifttest_checktest_evaluate "${line}" "${TEST_STATE}"
        shifttest_checktest_restore_from_backup
        unset TEST_STATE
    done

    shifttest_checktest_report

    # restore original build
    shifttest_checktest_build
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest
