inherit cmake

DEPENDS_prepend = "\
    cmake-native \
    gtest \
    gmock \
    cppcheck-native \
    cpplint-native \
    lcov-native \
    lcov-cobertura-native \
    qemu-native \
    doxygen-native \
    "

OECMAKE_C_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"
OECMAKE_CXX_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"

EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=ON"
EXTRA_OECMAKE += "-DCMAKE_CROSSCOMPILING_EMULATOR='qemu-${TUNE_ARCH};-L;${STAGING_DIR_TARGET}'"

addtask test after do_compile do_populate_sysroot
cmaketest_do_test() {
    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        local OUTPUT_DIR="${TEST_RESULT_OUTPUT}/${PF}"
        export GTEST_OUTPUT="xml:${OUTPUT_DIR}/"
        if [ -d "${OUTPUT_DIR}" ]; then
            bbplain "Removing: ${OUTPUT_DIR}"
            rm -rf "${OUTPUT_DIR}"
        fi
    fi

    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"
    cmake --build ${B} --target test -- ARGS="--output-on-failure" |
    while IFS= read line; do
        bbplain "$line"
    done

    if [ ! -z "${TEST_RESULT_OUTPUT}" ]; then
        local OUTPUT_DIR="${TEST_RESULT_OUTPUT}/${PF}"
        if [ ! -d "${OUTPUT_DIR}" ]; then
          bbwarn "No test report files generated at ${OUTPUT_DIR}"
          return
        fi
        for i in "${OUTPUT_DIR}/*.xml"; do
            sed -i "s|classname=\"|classname=\"${PN}.|g" $i
        done
    fi
}
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

addtask coverage after do_test
cmaketest_do_coverage() {
    local LCOV_DATAFILE_TOTAL="${B}/coverage_total.info"
    local LCOV_DATAFILE="${B}/coverage.info"

    lcov -c -d ${B} -o ${LCOV_DATAFILE_TOTAL} \
        --ignore-errors gcov \
        --gcov-tool ${TARGET_PREFIX}gcov \
        --rc lcov_branch_coverage=1

    lcov --extract ${LCOV_DATAFILE_TOTAL} \
        --rc lcov_branch_coverage=1 \
        "${S}/*" -o ${LCOV_DATAFILE}

    bbplain "GCC Code Coverage Report"

    lcov --list ${LCOV_DATAFILE} --rc lcov_branch_coverage=1 |
    while IFS= read line; do
        bbplain "$line"
    done

    if [ ! -z "${TEST_COVERAGE_OUTPUT}" ]; then
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
    fi
}
do_coverage[nostamp] = "1"
do_coverage[doc] = "Measures code coverage metrics for the target"

addtask doc after do_configure
cmaketest_do_doc() {
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
    mkdir -p "${OUTPUT_DIR}"
    bbplain "Generating API documentation with Doxygen"
    (cat "${S}/Doxyfile" ; echo "OUTPUT_DIRECTORY = ${OUTPUT_DIR}") | doxygen - |
    while read line; do
        bbplain "$line"
    done
}
do_doc[nostamp] = "1"
do_doc[doc] = "Generates documents for the target"


EXPORT_FUNCTIONS do_test do_coverage do_doc
