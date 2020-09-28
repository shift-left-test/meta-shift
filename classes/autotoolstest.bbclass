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

autotoolstest_do_checkcode() {
    shifttest_do_checkcode
}

# $1 : print stdout if "PRINT"
# $2 : report save path
autotoolstest_run_test() {
    PRINT_LINES=$1
    OUTPUT_DIR=$2

    if [ ! -z "${OUTPUT_DIR}" ]; then
        shifttest_prepare_output_dir ${OUTPUT_DIR}
    fi
    shifttest_prepare_env

    export LOG_COMPILER='${WORKDIR}/test-runner.sh'

    cd ${B}

    # Do not use '-e' option of 'make'.
    make check || true
    if [ "${PRINT_LINES}" = "PRINT" ]; then
        find . -name "test-suite.log" -exec cat {} \; | shifttest_print_lines
    fi
}

autotoolstest_do_test() {
    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        autotoolstest_run_test "PRINT" ${TEST_REPORT_OUTPUT}/${PF}/test
        shifttest_gtest_update_xmls
        shifttest_check_output_dir
    else
        autotoolstest_run_test "PRINT"
    fi
}

autotoolstest_do_coverage() {
    shifttest_do_coverage
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
        shifttest_checktest_mutate $line
        shifttest_checktest_build
        rm -rf ${CHECKTEST_WORKDIR_ACTUAL}/*
        autotoolstest_run_test "NOPRINT" ${CHECKTEST_WORKDIR_ACTUAL}
        shifttest_checktest_evaluate $line
        shifttest_checktest_restore_from_backup
    done

    shifttest_checktest_report

    # restore original build
    shifttest_checktest_build
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest
