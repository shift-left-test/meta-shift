inherit cpptest


OECMAKE_C_FLAGS:append:class-target = " -O0 -fprofile-arcs -ftest-coverage"
OECMAKE_CXX_FLAGS:append:class-target = " -O0 -fprofile-arcs -ftest-coverage"

EXTRA_OECMAKE:append:class-target = " -DCMAKE_CROSSCOMPILING_EMULATOR='${@shiftutils_qemu_cmake_emulator(d)}'"
EXTRA_OECMAKE:append:class-target = " -DCMAKE_EXPORT_COMPILE_COMMANDS=ON"


cmake_do_compile:prepend:class-target() {
    export TARGET_SYS="${TARGET_SYS}"
}

cmaketest_do_test() {
    local REPORT_DIR=""

    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        REPORT_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
        rm -rf "${REPORT_DIR}"
        mkdir -p "${REPORT_DIR}"
        shifttest_write_metadata "${REPORT_DIR}"

        export GTEST_OUTPUT="xml:${REPORT_DIR}/"
    fi

    cpptest_reset_coverage_counters

    # Forward env into the qemu guest test process via QEMU_SET_ENV so an
    # LD_PRELOAD interposer reaches the guest, not the host loader.
    local QEMU_SET_ENV_VAL="${@shiftutils_qemu_set_env(d)}"
    [ -n "${QEMU_SET_ENV_VAL}" ] && export QEMU_SET_ENV="${QEMU_SET_ENV_VAL}"

    bbplain "${PF} do_${BB_CURRENTTASK}: Running tests..."

    local CTEST_CMD="ctest --output-on-failure"
    if ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_SHUFFLE')) else 'false'}; then
        CTEST_CMD="${CTEST_CMD} --schedule-random"
    fi

    if [ -n "${SHIFT_TEST_FILTER}" ]; then
        # Translate gtest-style filter to ctest -R/-E
        local FILTER="${SHIFT_TEST_FILTER}"
        FILTER="${FILTER//./\\.}"
        FILTER="${FILTER//\*/.*}"
        FILTER="${FILTER//:/|}"
        FILTER="${FILTER//\?/.?}"
        local INCLUDE="${FILTER%%-*}"
        local EXCLUDE=""
        [[ "${FILTER}" == *-* ]] && EXCLUDE="${FILTER#*-}"
        [ -n "${INCLUDE}" ] && CTEST_CMD="${CTEST_CMD} -R ${INCLUDE}"
        [ -n "${EXCLUDE}" ] && CTEST_CMD="${CTEST_CMD} -E ${EXCLUDE}"
    fi

    if ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_STOP_ON_FAILURE')) else 'false'}; then
        CTEST_CMD="${CTEST_CMD} --stop-on-failure"
    fi

    if [ -n "${SHIFT_TEST_PARALLEL_JOBS}" ]; then
        CTEST_CMD="${CTEST_CMD} --parallel ${SHIFT_TEST_PARALLEL_JOBS}"
    fi

    local TEST_RC=0
    ( cd "${B}" && ${CTEST_CMD} ) 2>&1 | shiftutils_stream_plain
    TEST_RC=${PIPESTATUS[0]}

    shifttest_handle_test_rc ${TEST_RC} "ctest"

    if [ -n "${REPORT_DIR}" ] && [ -d "${REPORT_DIR}" ]; then
        cpptest_prefix_xml_classnames "${REPORT_DIR}"
    fi
}

cmaketest_do_coverage() {
    cpptest_do_coverage
}

cmaketest_do_checktest() {
    cpptest_do_checktest
}

EXPORT_FUNCTIONS do_test do_coverage do_checktest
