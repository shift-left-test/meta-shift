inherit shifttest


DEPENDS:prepend:class-target = "\
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', bb.utils.contains('SHIFT_CHECKTEST_ENABLED', '1', 'sentinel-native', '', d), '', d)} \
    compiledb-native \
    coreutils-native \
    gmock \
    gtest \
    lcov-native \
    python3-lcov-cobertura-native \
    qemu-native \
    "

# Coverage flag causes the binary to store the absolute path to the gcda file, resulting in a 'buildpaths' QA Issue.
python do_package_qa:prepend() {
    for package in set((d.getVar('PACKAGES', True) or '').split()):
        d.appendVar("INSANE_SKIP:%s" % package, " buildpaths")
}

# Execute the do_coverage task after the do_test task completes
do_coverage[recrdeptask] += "do_test"

# do_checktest reuses bitbake's compiled ${T}/run.do_test script for sentinel's
# --test-command, so do_test must have run at least once first.
do_checktest[depends] += "${PN}:do_test"

# Capture a zero-coverage baseline from .gcno alone. Shared by all
# build-system-specific do_test functions to keep their bodies identical.
cpptest_capture_coverage_baseline() {
    local LCOV_BRANCH_OPT="${@shiftutils_get_branch_coverage_option(d, 'lcov')}"
    find "${B}" -name '*.gcda' -delete
    lcov -c -i \
        -d "${B}" \
        -o "${B}/coverage_base.info" \
        --ignore-errors gcov \
        --gcov-tool "${TARGET_PREFIX}gcov" \
        ${LCOV_BRANCH_OPT}
}

# Prepend ${PN}. to gtest XML classname attributes (idempotent).
cpptest_prefix_xml_classnames() {
    find "$1" -name '*.xml' -exec sed -E -i \
        "s|classname=\"(${PN}\.)?|classname=\"${PN}.|g" {} +
}

cpptest_do_coverage() {
    local LCOV_BRANCH_OPT="${@shiftutils_get_branch_coverage_option(d, 'lcov')}"
    local GENHTML_BRANCH_OPT="${@shiftutils_get_branch_coverage_option(d, 'genhtml')}"
    local DATAFILE_BASE="${B}/coverage_base.info"
    local DATAFILE_TEST="${B}/coverage_test.info"
    local DATAFILE_TOTAL="${B}/coverage_total.info"
    local DATAFILE="${B}/coverage.info"

    rm -f "${DATAFILE_TOTAL}" "${DATAFILE}"

    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        local TEST_RESULT_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
        if ! find "${TEST_RESULT_DIR}" -maxdepth 1 -iname '*.xml' -print -quit 2>/dev/null | grep -q .; then
            bbwarn "No test result files generated at ${TEST_RESULT_DIR}"
            return 0
        fi
    fi

    if ! find "${B}" -name '*.gcda' -print -quit 2>/dev/null | grep -q .; then
        bbwarn "No .gcda files found at ${B}"
        return 0
    fi

    lcov -c \
        -d "${B}" \
        -o "${DATAFILE_TEST}" \
        --gcov-tool "${TARGET_PREFIX}gcov" \
        ${LCOV_BRANCH_OPT}

    lcov \
        -a "${DATAFILE_BASE}" \
        -a "${DATAFILE_TEST}" \
        -o "${DATAFILE_TOTAL}" \
        ${LCOV_BRANCH_OPT}

    lcov \
        --extract "${DATAFILE_TOTAL}" \
        ${LCOV_BRANCH_OPT} \
        "${S}/*" \
        -o "${DATAFILE}"

    if [ -n "${SHIFT_COVERAGE_EXCLUDES}" ]; then
        # Build a newline-delimited file of paths and pass via xargs so paths
        # with spaces survive. bash arrays / process-substitution would be
        # cleaner but BitBake's shell parser only accepts POSIX constructs.
        local EXC_FILE=$(mktemp)
        for exc in ${SHIFT_COVERAGE_EXCLUDES}; do
            local matched=0
            for path in ${S}/${exc}; do
                if [ -e "${path}" ]; then
                    if [ -d "${path}" ]; then
                        # lcov --remove takes file paths, not directories.
                        find "${path}" -type f >> "${EXC_FILE}"
                    else
                        echo "${path}" >> "${EXC_FILE}"
                    fi
                    matched=1
                fi
            done
            if [ ${matched} -eq 0 ]; then
                bbwarn "SHIFT_COVERAGE_EXCLUDES: no file matches ${exc}"
            fi
        done
        if [ -s "${EXC_FILE}" ]; then
            xargs -d '\n' -a "${EXC_FILE}" lcov --remove "${DATAFILE}" -o "${DATAFILE}" ${LCOV_BRANCH_OPT}
        fi
        rm -f "${EXC_FILE}"
    fi

    bbplain "${PF} do_${BB_CURRENTTASK}: GCC Code Coverage Report"
    lcov --list "${DATAFILE}" ${LCOV_BRANCH_OPT} | shiftutils_stream_plain

    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        local REPORT_DIR="${SHIFT_REPORT_DIR}/${PF}/coverage"
        local XML_FILE="${REPORT_DIR}/coverage.xml"

        mkdir -p "${REPORT_DIR}"

        ${@save_metadata(d) or ''}

        genhtml "${DATAFILE}" \
            --demangle-cpp \
            --rc "genhtml_demangle_cpp_tool=${TARGET_PREFIX}c++filt" \
            --output-directory "${REPORT_DIR}" \
            --ignore-errors source \
            ${GENHTML_BRANCH_OPT}

        ( cd "${S}" && lcov_cobertura "${DATAFILE}" \
            --demangle-tool "${TARGET_PREFIX}c++filt" \
            --demangle \
            --output "${XML_FILE}" )

        if [ -f "${XML_FILE}" ]; then
            sed -E -i "s|(<package[[:space:]]+name=\")(${PN}\.)?|\1${PN}.|g" "${XML_FILE}"
        else
            bbwarn "No coverage report files generated at ${REPORT_DIR}"
        fi
    fi
}

cpptest_do_checktest() {
    if [ "${SHIFT_CHECKTEST_ENABLED}" != "1" ]; then
        return 0
    fi

    if [ -z "${SHIFT_REPORT_DIR}" ]; then
        bbwarn "SHIFT_REPORT_DIR is empty; skipping do_checktest (mutation report has nowhere to go)"
        return 0
    fi

    if ! echo "${BBFILE_COLLECTIONS}" | grep -qw clang-layer; then
        bbfatal "The task requires meta-clang to be present"
    fi

    if [ ! -d "${S}/.git" ]; then
        bbwarn "No .git directory in source directory"
        return 0
    fi

    # cmake exports compile_commands.json natively; autotools/qmake do not.
    if [ ! -f "${B}/compile_commands.json" ]; then
        ( cd "${B}" && compiledb --command-style make ) || {
            bbwarn "Failed to create compile_commands.json using compiledb"
            return 0
        }
    fi

    # Normalize compile_commands.json so Sentinel/Clang can match mutation
    # candidates. cmake emits "file" and the source argument inside "command"
    # as absolute paths, but compiledb leaves them relative to "directory".
    # Sentinel matches candidates by the path Clang reports through
    # SourceManager, which echoes the source argument from the compile
    # command verbatim — relative entries therefore produce 0 mutants. The
    # target triple is also (re-)injected idempotently since this task is
    # nostamp and the JSON may persist across runs.
    python3 -c '
import json, os, re, sys
p, target_sys = sys.argv[1], sys.argv[2]
with open(p) as f:
    db = json.load(f)
target_opt = "--target=" + target_sys
for e in db:
    if not os.path.isabs(e["file"]):
        e["file"] = os.path.normpath(os.path.join(e["directory"], e["file"]))
    abs_file = e["file"]
    base = os.path.basename(abs_file)
    pattern = re.compile(r"(?<![\w/])(?:\S*/)?" + re.escape(base) + r"(?=\s|$)")
    cmd = pattern.sub(abs_file, e["command"])
    cmd = re.sub(r"\s*--target=\S+", "", cmd)
    e["command"] = cmd + " " + target_opt
with open(p, "w") as f:
    json.dump(db, f, indent=1)
' "${B}/compile_commands.json" "${TARGET_SYS}"

    # Sentinel's iterations overwrite ${SHIFT_REPORT_DIR}/${PF}/test on every
    # invocation, so back up any pre-existing baseline and restore it on exit.
    local TEST_RESULT_DIR="${SHIFT_REPORT_DIR}/${PF}/test"
    local BACKUP_DIR="${WORKDIR}/checktest-baseline-backup"
    # Recover from a prior interrupted run that left baseline only in BACKUP_DIR.
    if [ -d "${BACKUP_DIR}" ] && [ ! -d "${TEST_RESULT_DIR}" ]; then
        mv "${BACKUP_DIR}" "${TEST_RESULT_DIR}"
    fi
    rm -rf "${BACKUP_DIR}"
    if [ -d "${TEST_RESULT_DIR}" ]; then
        mv "${TEST_RESULT_DIR}" "${BACKUP_DIR}"
    fi

    mkdir -p "${SHIFT_REPORT_DIR}/${PF}/checktest"

    # Stream sentinel's output via bbplain so it surfaces to the console; the
    # raw exit code is recovered via PIPESTATUS since the while-loop always
    # succeeds. Option toggles are resolved at BitBake parse time via
    # ${@...} — shell ${VAR:+...} would silently drop them because BitBake
    # vars are not exported into the task shell environment.
    local SENTINEL_RC=0
    sentinel \
        --clean \
        --workspace="${WORKDIR}/sentinel-workspace" \
        --source-dir="${S}" \
        --build-command="bash ${T}/run.do_compile" \
        --test-command="bash ${T}/run.do_test" \
        --test-result-dir="${TEST_RESULT_DIR}" \
        --output-dir="${SHIFT_REPORT_DIR}/${PF}/checktest" \
        --compiledb-dir="${B}" \
        ${@shiftutils_cli_opt(d, 'SHIFT_CHECKTEST_LIMIT', '--limit')} \
        ${@shiftutils_cli_opt(d, 'SHIFT_CHECKTEST_TIMEOUT', '--timeout')} \
        ${@shiftutils_cli_opt(d, 'SHIFT_CHECKTEST_GENERATOR', '--generator')} \
        ${@shiftutils_cli_opt(d, 'SHIFT_CHECKTEST_SEED', '--seed')} \
        ${@shiftutils_cli_opt(d, 'SHIFT_CHECKTEST_FROM', '--from')} \
        ${@shiftutils_cli_bool(d, 'SHIFT_CHECKTEST_UNCOMMITTED', '--uncommitted')} \
        ${@shiftutils_cli_bool(d, 'SHIFT_CHECKTEST_VERBOSE', '--verbose')} \
        ${@shiftutils_cli_multi(d, 'SHIFT_CHECKTEST_OPERATORS', '--operator')} \
        ${@shiftutils_cli_multi(d, 'SHIFT_CHECKTEST_PATTERNS', '--pattern')} \
        ${@shiftutils_cli_multi(d, 'SHIFT_CHECKTEST_EXTENSIONS', '--extension')} \
        2>&1 | shiftutils_stream_plain
    SENTINEL_RC=${PIPESTATUS[0]}

    rm -rf "${TEST_RESULT_DIR}"
    if [ -d "${BACKUP_DIR}" ]; then
        mv "${BACKUP_DIR}" "${TEST_RESULT_DIR}"
    fi

    ${@save_metadata(d) or ''}

    return ${SENTINEL_RC}
}
