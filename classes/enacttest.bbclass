inherit shifttest


DEPENDS:prepend:class-target = "\
    coreutils-native \
    nodejs-native \
"

def enacttest_get_nodejs_arch(d):
    target_arch = d.getVar('TRANSLATED_TARGET_ARCH', True)
    arch_map = {
        "x86-64": "x64",
        "aarch64": "arm64",
        "powerpc": "ppc",
        "powerpc64": "ppc64",
        "i486": "ia32",
        "i586": "ia32",
        "i686": "ia32",
    }
    return arch_map.get(target_arch, target_arch)


enacttest_npm_install() {
    local ATTEMPTS=0
    local STATUS=-1
    local NPM_INSTALL_ARCH="${@enacttest_get_nodejs_arch(d)}"
    local NPM_INSTALL_OPTIONS="--arch=${NPM_INSTALL_ARCH} --target_arch=${NPM_INSTALL_ARCH} --without-ssl --insecure --no-optional --force"

    while [ ${STATUS} -ne 0 ]; do
        ATTEMPTS=$(expr ${ATTEMPTS} + 1)
        if [ ${ATTEMPTS} -gt 5 ]; then
            bberror "NPM installation failed. Abort!"
            exit ${STATUS}
        fi

        bbnote "NPM module installation: #${ATTEMPTS} (of 5)..." && echo
        STATUS=0
        timeout --kill-after=5m 15m ${STAGING_BINDIR_NATIVE}/npm install ${NPM_INSTALL_OPTIONS} "$@" || eval "STATUS=\$?"
        if [ ${STATUS} -ne 0 ]; then
            bbwarn "...NPM installation failed with status ${STATUS}"
        else
            bbnote "...NPM installation succeeded" && echo
        fi
    done
}

do_compile:append:class-target() {
    local STATUS=0

    bbnote "Installing node modules including devDependencies..."
    enacttest_npm_install

    bbnote "Checking if @enact/cli is installed..."
    STATUS=0
    ${STAGING_BINDIR_NATIVE}/npm list @enact/cli || eval "STATUS=\$?"
    if [ ${STATUS} -ne 0 ]; then
        bbnote "Unable to locate @enact/cli. Installing the latest version of the module..."
        enacttest_npm_install @enact/cli --save-dev
    fi

    bbnote "Checking if jest-junit is installed..."
    STATUS=0
    ${STAGING_BINDIR_NATIVE}/npm list jest-junit || eval "STATUS=\$?"
    if [ ${STATUS} -ne 0 ]; then
        bbnote "Unable to locate jest-junit. Installing the latest version of the module..."
        enacttest_npm_install jest-junit --save-dev
    fi
}

enacttest_do_test() {
    export HOME="${WORKDIR}"

    local NPM_ARGS=""
    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        local REPORT_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
        rm -rf "${REPORT_DIR}"
        mkdir -p "${REPORT_DIR}"
        shifttest_write_metadata "${REPORT_DIR}"
        export JEST_JUNIT_OUTPUT_DIR="${REPORT_DIR}"
        NPM_ARGS="--reporters=default --reporters=jest-junit"
    fi

    if ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_STOP_ON_FAILURE')) else 'false'}; then
        NPM_ARGS="${NPM_ARGS} --bail"
    fi

    bbplain "${PF} do_${BB_CURRENTTASK}: Running tests..."

    local TEST_RC=0
    ( cd "${S}" && npm test -- ${NPM_ARGS} 2>&1 ) | shiftutils_stream_plain
    TEST_RC=${PIPESTATUS[0]}

    shifttest_handle_test_rc ${TEST_RC} "npm test"
}

enacttest_do_coverage() {
    export HOME="${WORKDIR}"

    local NPM_ARGS="--coverage"
    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        local TEST_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
        local COV_DIR="${SHIFT_REPORT_DIR}/${PF}/coverage"
        mkdir -p "${TEST_DIR}" "${COV_DIR}"
        # do_verify runs only do_coverage, which also emits the test report.
        shifttest_write_metadata "${TEST_DIR}"
        shifttest_write_metadata "${COV_DIR}"
        export JEST_JUNIT_OUTPUT_DIR="${TEST_DIR}"
        NPM_ARGS="${NPM_ARGS} --reporters=default --reporters=jest-junit"
        NPM_ARGS="${NPM_ARGS} --coverageDirectory=${COV_DIR}"
        NPM_ARGS="${NPM_ARGS} --coverageReporters=text --coverageReporters=html --coverageReporters=cobertura"
    fi

    if ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_TEST_STOP_ON_FAILURE')) else 'false'}; then
        NPM_ARGS="${NPM_ARGS} --bail"
    fi

    bbplain "${PF} do_${BB_CURRENTTASK}: Running tests with coverage..."

    local TEST_RC=0
    ( cd "${S}" && npm test -- ${NPM_ARGS} 2>&1 ) | shiftutils_stream_plain
    TEST_RC=${PIPESTATUS[0]}

    shifttest_handle_test_rc ${TEST_RC} "npm test"
}

enacttest_do_checktest() {
    :
}

python enacttest_do_verify() {
    shifttest_verify(d, tasks=["coverage", "checktest"])
}

EXPORT_FUNCTIONS do_test do_coverage do_checktest do_verify
