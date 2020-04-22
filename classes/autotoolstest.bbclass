inherit autotools
inherit shifttest

DEPENDS_prepend = "\
    gtest \
    gmock \
    "

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
        unset CFLAGS_ORI
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
qemu-${TUNE_ARCH} -L ${STAGING_DIR_TARGET} ""$""TARGET" > ${WORKDIR}/test-runner.sh
    chmod 755 ${WORKDIR}/test-runner.sh
}

autotoolstest_do_test() {
    export LOG_COMPILER='${WORKDIR}/test-runner.sh'

    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        local OUTPUT_DIR="${TEST_RESULT_OUTPUT}/${PF}"
        export GTEST_OUTPUT="xml:${OUTPUT_DIR}/"
        rm -rf "${OUTPUT_DIR}"
    fi

    cd ${B}

    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
    
    # Do not use '-e' option of 'make'.
    make check || true
    find . -name "test-suite.log" -exec cat {} \; | shifttest_print_lines

    if [ -z "${TEST_RESULT_OUTPUT}" ]; then
        return
    fi

    local OUTPUT_DIR="${TEST_RESULT_OUTPUT}/${PF}"

    if [ ! -d "${OUTPUT_DIR}" ]; then
        bbwarn "No test report files generated at ${OUTPUT_DIR}"
        return
    fi

    for i in "${OUTPUT_DIR}/*.xml"; do
        sed -i "s|classname=\"|classname=\"${PN}.|g" $i
    done
}

autotoolstest_do_coverage() {
    shifttest_do_coverage
}

autotoolstest_do_doc() {
    shifttest_do_doc
}

EXPORT_FUNCTIONS do_test do_coverage do_doc
