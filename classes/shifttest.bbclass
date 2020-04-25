DEPENDS_prepend = "\
    gtest \
    gmock \
    lcov-native \
    lcov-cobertura-native \
    qemu-native \
    doxygen-native \
    "

shifttest_print_lines() {
    while IFS= read line; do
        bbplain "$line"
    done
}


addtask test after do_compile do_populate_sysroot
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

shifttest_do_test() {
    bbfatal "'inherit shifttest' is not allowed. You should inherit an appropriate bbclass instead."
}

shifttest_prepare_output_dir() {
    [ -z "${TEST_RESULT_OUTPUT}" ] && return
    rm -rf "${TEST_RESULT_OUTPUT}/${PF}"
    mkdir -p "${TEST_RESULT_OUTPUT}"
}

shifttest_prepare_env() {
    [ ! -z "${TEST_RESULT_OUTPUT}" ] && export GTEST_OUTPUT="xml:${TEST_RESULT_OUTPUT}/${PF}/"
    [ ! -z "${GTEST_FILTER}" ] && export GTEST_FILTER="${GTEST_FILTER}"
    [ ! -z "${GTEST_FAIL_FAST}" ] && export GTEST_FAIL_FAST="${GTEST_FAIL_FAST}"
    [ ! -z "${GTEST_ALSO_RUN_DISABLED_TESTS}" ] && export GTEST_ALSO_RUN_DISABLED_TESTS="${GTEST_ALSO_RUN_DISABLED_TESTS}"
    [ ! -z "${GTEST_REPEAT}" ] && export GTEST_REPEAT="${GTEST_REPEAT}"
    [ ! -z "${GTEST_SHUFFLE}" ] && export GTEST_SHUFFLE="${GTEST_SHUFFLE}"
    [ ! -z "${GTEST_RANDOM_SEED}" ] && export GTEST_RANDOM_SEED="${GTEST_RANDOM_SEED}"
    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
}

shifttest_gtest_update_xmls() {
    [ -z "${TEST_RESULT_OUTPUT}" ] && return
    [ ! -d "${TEST_RESULT_OUTPUT}/${PF}" ] && return
    find "${TEST_RESULT_OUTPUT}/${PF}" -name "*.xml" \
        -exec sed -i "s|classname=\"|classname=\"${PN}.|g" {} \;
}

shifttest_check_output_dir() {
    [ -z "${TEST_RESULT_OUTPUT}" ] && return
    [ -d "${TEST_RESULT_OUTPUT}/${PF}" ] && return
    bbwarn "No test report files found at ${TEST_RESULT_OUTPUT}/${PF}"
}


addtask coverage after do_test
do_coverage[nostamp] = "1"
do_coverage[doc] = "Measures code coverage metrics for the target"

shifttest_do_coverage() {
    local LCOV_DATAFILE_TOTAL="${B}/coverage_total.info"
    local LCOV_DATAFILE="${B}/coverage.info"

    rm -f ${LCOV_DATAFILE_TOTAL}
    rm -f ${LCOV_DATAFILE}

    if [ -z "$(find ${B} -name *.gcda -type f)" ]; then
        bbwarn "No .gcda files found at ${B}"
        return
    fi

    lcov -c -d ${B} -o ${LCOV_DATAFILE_TOTAL} \
        --ignore-errors gcov \
        --gcov-tool ${TARGET_PREFIX}gcov \
        --rc lcov_branch_coverage=1

    lcov --extract ${LCOV_DATAFILE_TOTAL} \
        --rc lcov_branch_coverage=1 \
        "${S}/*" -o ${LCOV_DATAFILE}

    bbplain "GCC Code Coverage Report"

    lcov --list ${LCOV_DATAFILE} --rc lcov_branch_coverage=1 | shifttest_print_lines

    if [ -z "${TEST_COVERAGE_OUTPUT}" ]; then
        return
    fi

    local OUTPUT_DIR="${TEST_COVERAGE_OUTPUT}/${PF}"
    local COBERTURA_FILE="${OUTPUT_DIR}/coverage.xml"

    rm -rf ${OUTPUT_DIR}

    genhtml ${LCOV_DATAFILE} \
        --output-directory ${OUTPUT_DIR} \
        --ignore-errors source \
        --rc genhtml_branch_coverage=1

    cd ${S}

    nativepython -m lcov_cobertura ${LCOV_DATAFILE} \
        --demangle \
        --output ${COBERTURA_FILE}

    if [ ! -f "${COBERTURA_FILE}" ]; then
        bbwarn "No coverage report files generated at ${OUTPUT_DIR}"
        return
    fi

    sed -r -i 's|(<package.*name=\")(.*")|\1${PN}\.\2|g' "${OUTPUT_DIR}/coverage.xml"
}


addtask doc after do_configure
do_doc[nostamp] = "1"
do_doc[doc] = "Generates documents for the target"

shifttest_do_doc() {
    if [ ! -f "${S}/Doxyfile" ]; then
        bbplain "No Doxyfile found. Skip generating the doxygen documents"
        return
    fi

    if [ -z "${DOXYGEN_OUTPUT}" ]; then
        bbwarn "No DOXYGEN_OUTPUT variable found. Use the default path (${TOPDIR}/report/doxygen)"
        DOXYGEN_OUTPUT="${TOPDIR}/report/doxygen"
    fi

    cd ${S}

    local OUTPUT_DIR="${DOXYGEN_OUTPUT}/${PF}"
    rm -rf ${OUTPUT_DIR}
    mkdir -p ${OUTPUT_DIR}
    bbplain "Generating API documentation with Doxygen"
    (cat "${S}/Doxyfile" ; echo "OUTPUT_DIRECTORY = ${OUTPUT_DIR}") | doxygen - | shifttest_print_lines
}
