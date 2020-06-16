DEPENDS_prepend = "\
    gtest \
    gmock \
    lcov-native \
    python-lcov-cobertura-native \
    qemu-native \
    cppcheck-native \
    cpplint-native \
    sage-native \
    "

shifttest_print_lines() {
    while IFS= read line; do
        bbplain "${PF} do_${BB_CURRENTTASK}: $line"
    done
}

addtask checkcode after do_compile
do_checkcode[nostamp] = "1"
do_checkcode[doc] = "Runs static analysis for the target"

shifttest_do_checkcode() {
    if [ ! -z "${CHECK_CODE_OUTPUT}" ]; then
        rm -rf "${CHECK_CODE_OUTPUT}/${PF}"
        mkdir -p "${CHECK_CODE_OUTPUT}/${PF}"
        local OUTPUT_PATH_OPTION="--output-path=${CHECK_CODE_OUTPUT}/${PF}"
    fi

    sage --source ${S} --build ${B} ${OUTPUT_PATH_OPTION} ${CHECK_CODE_TOOLS} | shifttest_print_lines
}

# In order to overwrite the sstate cache libraries
do_install[nostamp] = "1"

addtask test after do_compile do_populate_sysroot
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

shifttest_do_test() {
    bbfatal "'inherit shifttest' is not allowed. You should inherit an appropriate bbclass instead."
}

shifttest_prepare_output_dir() {
    [ -z "${TEST_RESULT_OUTPUT}" ] && return
    mkdir -p "${TEST_RESULT_OUTPUT}"
    rm -rf "${TEST_RESULT_OUTPUT}/${PF}"
}

shifttest_prepare_env() {
    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        export GTEST_OUTPUT="xml:${TEST_RESULT_OUTPUT}/${PF}/"
    fi
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

    bbplain "${PF} do_${BB_CURRENTTASK}: GCC Code Coverage Report"

    lcov --list ${LCOV_DATAFILE} --rc lcov_branch_coverage=1 | shifttest_print_lines

    if [ -z "${TEST_COVERAGE_OUTPUT}" ]; then
        return
    fi

    local OUTPUT_DIR="${TEST_COVERAGE_OUTPUT}/${PF}"
    local COBERTURA_FILE="${OUTPUT_DIR}/coverage.xml"

    rm -rf ${OUTPUT_DIR}

    genhtml ${LCOV_DATAFILE} \
        --demangle-tool ${TARGET_PREFIX}c++filt \
        --demangle-cpp \
        --output-directory ${OUTPUT_DIR} \
        --ignore-errors source \
        --rc genhtml_branch_coverage=1

    cd ${S}

    nativepython -m lcov_cobertura ${LCOV_DATAFILE} \
        --demangle-tool=${TARGET_PREFIX}c++filt \
        --demangle \
        --output ${COBERTURA_FILE}

    if [ ! -f "${COBERTURA_FILE}" ]; then
        bbwarn "No coverage report files generated at ${OUTPUT_DIR}"
        return
    fi

    sed -r -i 's|(<package.*name=\")(.*")|\1${PN}\.\2|g' "${OUTPUT_DIR}/coverage.xml"
}
