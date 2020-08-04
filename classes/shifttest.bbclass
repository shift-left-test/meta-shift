DEPENDS_prepend = "\
    gtest \
    gmock \
    lcov-native \
    python3-lcov-cobertura-native \
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
    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        mkdir -p "${TEST_REPORT_OUTPUT}/${PF}/checkcode"
        rm -rf "${TEST_REPORT_OUTPUT}/${PF}/checkcode/*"
        local OUTPUT_PATH_OPTION="--output-path=${TEST_REPORT_OUTPUT}/${PF}/checkcode"
    fi

    sage --source ${S} --build ${B} ${OUTPUT_PATH_OPTION} ${CHECK_CODE_TOOLS} 2>&1 | shifttest_print_lines
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
    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        mkdir -p "${TEST_REPORT_OUTPUT}/${PF}/test"
        rm -rf "${TEST_REPORT_OUTPUT}/${PF}/test/*"
    fi
}

shifttest_prepare_env() {
    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        export GTEST_OUTPUT="xml:${TEST_REPORT_OUTPUT}/${PF}/test/"
    fi
    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
}

shifttest_gtest_update_xmls() {
    [ -z "${TEST_REPORT_OUTPUT}" ] && return
    [ ! -d "${TEST_REPORT_OUTPUT}/${PF}/test" ] && return
    find "${TEST_REPORT_OUTPUT}/${PF}/test" -name "*.xml" \
        -exec sed -i "s|classname=\"|classname=\"${PN}.|g" {} \;
}

shifttest_check_output_dir() {
    [ -z "${TEST_REPORT_OUTPUT}" ] && return
    [ -d "${TEST_REPORT_OUTPUT}/${PF}/test" ] && return
    bbwarn "No test report files found at ${TEST_REPORT_OUTPUT}/${PF}/test"
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

    if [ -z "${TEST_REPORT_OUTPUT}" ]; then
        return
    fi

    local OUTPUT_DIR="${TEST_REPORT_OUTPUT}/${PF}/coverage"
    local COBERTURA_FILE="${OUTPUT_DIR}/coverage.xml"

    rm -rf ${OUTPUT_DIR}

    genhtml ${LCOV_DATAFILE} \
        --demangle-tool ${TARGET_PREFIX}c++filt \
        --demangle-cpp \
        --output-directory ${OUTPUT_DIR} \
        --ignore-errors source \
        --rc genhtml_branch_coverage=1

    cd ${S}

    nativepython3 -m lcov_cobertura ${LCOV_DATAFILE} \
        --demangle-tool=${TARGET_PREFIX}c++filt \
        --demangle \
        --output ${COBERTURA_FILE}

    if [ ! -f "${COBERTURA_FILE}" ]; then
        bbwarn "No coverage report files generated at ${OUTPUT_DIR}"
        return
    fi

    sed -r -i 's|(<package.*name=\")(.*")|\1${PN}\.\2|g' "${OUTPUT_DIR}/coverage.xml"
}
