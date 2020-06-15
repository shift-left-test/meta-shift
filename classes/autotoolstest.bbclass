inherit autotools
inherit shifttest

do_configure_prepend() {
    # add coverage flags to cxxflags & cflags
    if [[ -v CXXFLAGS ]]; then
        export CXXFLAGS_ORI="$CXXFLAGS"
    fi
    export CXXFLAGS="$CXXFLAGS -O0 -fprofile-arcs -ftest-coverage"

    if [[ -v CFLAGS ]]; then
        export CFLAGS_ORI="$CFLAGS"
    fi
    export CFLAGS="$CFLAGS -O0 -fprofile-arcs -ftest-coverage"
}

do_configure_append() {
    # restore environment variables
    if [[ -v CXXFLAGS_ORI ]]; then
        export CXXFLAGS="$CXXFLAGS_ORI"
        unset CXXFLAGS_ORI
    else
        unset CXXFLAGS
    fi

    if [[ -v CFLAGS_ORI ]]; then
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
    echo "
if [ -f .libs/""$""1 ]; then
    TARGET=.libs/""$""1
else
    TARGET=""$""1
fi
${QEMU_BIN_NAME} -L ${STAGING_DIR_TARGET}  -E LD_LIBRARY_PATH=""$""{LD_LIBRARY_PATH}:${STAGING_DIR_TARGET}/${baselib} ""$""TARGET" > ${WORKDIR}/test-runner.sh
    chmod 755 ${WORKDIR}/test-runner.sh
}

autotoolstest_do_checkcode() {
    shifttest_do_checkcode
}

autotoolstest_do_test() {
    shifttest_prepare_output_dir

    shifttest_prepare_env
    export LOG_COMPILER='${WORKDIR}/test-runner.sh'
    cd ${B}

    # Do not use '-e' option of 'make'.
    make check || true
    find . -name "test-suite.log" -exec cat {} \; | shifttest_print_lines

    shifttest_gtest_update_xmls
    shifttest_check_output_dir
}

autotoolstest_do_coverage() {
    shifttest_do_coverage
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage
