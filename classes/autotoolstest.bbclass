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

autotoolstest_do_test() {
    local REPORT_DIR=""

    export LOG_COMPILER="${WORKDIR}/test-runner.sh"

    if ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_SHUFFLE')) else 'false'}; then
        export GTEST_SHUFFLE=1
    fi

    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        REPORT_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
        rm -rf "${REPORT_DIR}"
        mkdir -p "${REPORT_DIR}"

        ${@save_metadata(d) or ''}

        export GTEST_OUTPUT="xml:${REPORT_DIR}/"
    fi

    cpptest_reset_coverage_counters

    if [ -n "${SHIFT_TEST_FILTER}" ]; then
        export GTEST_FILTER="${SHIFT_TEST_FILTER}"
    fi

    local TEST_RC=0
    ( cd "${B}" && make check ) || TEST_RC=$?

    shifttest_handle_test_rc ${TEST_RC} "make check"

    find "${B}" -name 'test-suite.log' -exec cat {} \; | shiftutils_stream_plain

    if [ -n "${REPORT_DIR}" ] && [ -d "${REPORT_DIR}" ]; then
        cpptest_prefix_xml_classnames "${REPORT_DIR}"
    fi
}

autotoolstest_do_coverage() {
    cpptest_do_coverage
}

autotoolstest_do_checktest() {
    cpptest_do_checktest
}

EXPORT_FUNCTIONS do_test do_coverage do_checktest
