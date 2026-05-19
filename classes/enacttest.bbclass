inherit shifttest


DEPENDS:prepend:class-target = "\
    coreutils-native \
    nodejs-native \
"

def enacttest_get_nodejs_arch(d):
    target_arch = d.getVar('TRANSLATED_TARGET_ARCH', True)

    if target_arch == "x86-64":
        target_arch = "x64"
    elif target_arch == "aarch64":
        target_arch = "arm64"
    elif target_arch == "powerpc":
        target_arch = "ppc"
    elif target_arch == "powerpc64":
        target_arch = "ppc64"
    elif (target_arch == "i486" or target_arch == "i586" or target_arch == "i686"):
        target_arch = "ia32"

    return target_arch


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
    ${STAGING_BINDIR_NATIVE}/npm list @enact/cli || eval "STATUS=\$?"
    if [ ${STATUS} -ne 0 ]; then
        bbnote "Unable to locate @enact/cli. Installing the latest version of the module..."
        enacttest_npm_install @enact/cli --save-dev
    fi

    bbnote "Checking if jest-junit is installed..."
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
        export JEST_JUNIT_OUTPUT_DIR="${REPORT_DIR}"
        NPM_ARGS="--reporters=default --reporters=jest-junit"

        ${@save_metadata(d) or ''}
    fi

    bbplain "${PF} do_${BB_CURRENTTASK}: Running tests..."

    local TEST_RC=0
    ( cd "${S}" && npm test -- ${NPM_ARGS} 2>&1 ) | shiftutils_stream_plain
    TEST_RC=${PIPESTATUS[0]}

    if [ ${TEST_RC} -ne 0 ] && [ "${SHIFT_TEST_SUPPRESS_FAILURES}" != "1" ]; then
        bberror "npm test failed with exit code ${TEST_RC}"
    fi
}

enacttest_do_coverage() {
    export HOME="${WORKDIR}"

    local NPM_ARGS="--coverage"
    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        local TEST_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
        local COV_DIR="${SHIFT_REPORT_DIR}/${PF}/coverage"
        mkdir -p "${TEST_DIR}" "${COV_DIR}"
        export JEST_JUNIT_OUTPUT_DIR="${TEST_DIR}"
        NPM_ARGS="${NPM_ARGS} --reporters=default --reporters=jest-junit"
        NPM_ARGS="${NPM_ARGS} --coverageDirectory=${COV_DIR}"
        NPM_ARGS="${NPM_ARGS} --coverageReporters=text --coverageReporters=html --coverageReporters=cobertura"

        ${@save_metadata(d) or ''}
    fi

    bbplain "${PF} do_${BB_CURRENTTASK}: Running tests with coverage..."

    local TEST_RC=0
    ( cd "${S}" && npm test -- ${NPM_ARGS} 2>&1 ) | shiftutils_stream_plain
    TEST_RC=${PIPESTATUS[0]}

    if [ ${TEST_RC} -ne 0 ] && [ "${SHIFT_TEST_SUPPRESS_FAILURES}" != "1" ]; then
        bberror "npm test failed with exit code ${TEST_RC}"
    fi
}

enacttest_do_checktest() {
    :
}

python enacttest_do_report() {
    shifttest_report(d, tasks=["coverage", "checktest"])
}

EXPORT_FUNCTIONS do_test do_coverage do_checktest do_report
