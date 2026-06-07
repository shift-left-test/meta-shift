inherit shifttest


DEPENDS:prepend:class-target = "\
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', 'sentinel-native' if bb.utils.to_boolean(d.getVar('SHIFT_CHECKTEST_ENABLED')) else '', '', d)} \
    compiledb-native \
    coreutils-native \
    gmock \
    gtest \
    python3-gcovr-native \
    qemu-native \
    "

# Coverage needs the real on-disk paths in .gcno. The default DEBUG_PREFIX_MAP
# remaps them (-ffile-prefix-map, and even -fdebug-prefix-map rewrites the
# paths gcov reads), making sysroot headers unresolvable, so disable it here.
DEBUG_PREFIX_MAP:class-target = ""

# The coverage flag bakes absolute .gcda paths into the binary, tripping the
# 'buildpaths' QA check.
python do_package_qa:prepend() {
    for package in set((d.getVar('PACKAGES', True) or '').split()):
        d.appendVar("INSANE_SKIP:%s" % package, " buildpaths")
}

do_coverage[recrdeptask] += "do_test"

# do_checktest reuses bitbake's compiled ${T}/run.do_test script for sentinel's
# --test-command, so do_test must have run at least once first.
do_checktest[depends] += "${PN}:do_test"

# Reset coverage counters before a test run so re-runs (nostamp) do not
# accumulate execution counts. gcovr derives zero-coverage for never-executed
# files directly from .gcno, so no lcov baseline capture is needed.
cpptest_reset_coverage_counters() {
    find "${B}" -name '*.gcda' -delete
}

# Prepend ${PN}. to gtest XML classname attributes (idempotent).
cpptest_prefix_xml_classnames() {
    find "$1" -name '*.xml' -exec sed -E -i \
        "s|classname=\"(${PN}\.)?|classname=\"${PN}.|g" {} +
}

cpptest_do_coverage() {
    local REPORT_DIR="${SHIFT_REPORT_DIR}/${PF}/coverage"
    local XML_FILE="${REPORT_DIR}/coverage.xml"

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

    # autoconf leaves conftest.gc{no,da} artifacts whose sources are removed
    # after configure. gcovr >= 6 treats the missing source as a fatal error
    # (gcovr <= 5 only warns), so drop them before scanning ${B}.
    find "${B}" -name '*conftest*.gcno' -delete
    find "${B}" -name '*conftest*.gcda' -delete

    # Code under test may call umask(), leaving .gcda the owner cannot read.
    find "${B}" -name '*.gcda' -exec chmod u+rw {} +

    # SHIFT_COVERAGE_EXCLUDES are regexes (gcovr --exclude), space-separated.
    local EXCLUDE_OPTS=""
    for exc in ${SHIFT_COVERAGE_EXCLUDES}; do
        EXCLUDE_OPTS="${EXCLUDE_OPTS} --exclude ${exc}"
    done

    bbplain "${PF} do_${BB_CURRENTTASK}: GCC Code Coverage Report"

    # Report files only when SHIFT_REPORT_DIR is set; gcovr emits all formats
    # (stdout text + HTML + Cobertura) in a single invocation (gcovr >= 5.0).
    local REPORT_OPTS=""
    if [ -n "${SHIFT_REPORT_DIR}" ]; then
        mkdir -p "${REPORT_DIR}"
        ${@save_metadata(d) or ''}
        REPORT_OPTS="--html-details ${REPORT_DIR}/index.html --html-self-contained --cobertura ${XML_FILE}"
    fi

    # SHIFT_COVERAGE_BRANCH switches the text report from line to branch coverage
    # (HTML and Cobertura always carry both). gcovr >= 7.0 renamed --branches to
    # --txt-metric, so feature-detect which flag the installed gcovr accepts.
    local BRANCH_OPT=""
    if ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_COVERAGE_BRANCH')) else 'false'}; then
        if gcovr --help 2>&1 | grep -q -- '--txt-metric'; then
            BRANCH_OPT="--txt-metric branch"
        else
            BRANCH_OPT="--branches"
        fi
    fi

    local GCOV_TOOL="${TARGET_PREFIX}gcov"
    case "${CC}" in
        *clang*) GCOV_TOOL="llvm-cov gcov" ;;
    esac

    gcovr \
        --root "${S}" \
        --gcov-executable "${GCOV_TOOL}" \
        ${EXCLUDE_OPTS} \
        --txt - \
        ${BRANCH_OPT} \
        ${REPORT_OPTS} \
        "${B}" 2>&1 | shiftutils_stream_plain

    # Prefix the Cobertura package name with ${PN}. (idempotent) to keep
    # per-recipe attribution.
    if [ -n "${SHIFT_REPORT_DIR}" ] && [ -f "${XML_FILE}" ]; then
        sed -E -i "s|(<package[[:space:]]+name=\")(${PN}\.)?|\1${PN}.|g" "${XML_FILE}"
    fi
}

cpptest_do_checktest() {
    if ! ${@'true' if bb.utils.to_boolean(d.getVar('SHIFT_CHECKTEST_ENABLED')) else 'false'}; then
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

    # Normalize compile_commands.json so sentinel/clang can match mutation
    # candidates: compiledb leaves source paths relative to "directory", but
    # clang echoes them verbatim and relative entries produce 0 mutants. Also
    # (re-)inject the target triple idempotently, since this nostamp task may
    # reuse a JSON left from a previous run.
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

    # Stream sentinel's output through bbplain so it reaches the console, and
    # recover its real exit code via PIPESTATUS. Option toggles resolve at parse
    # time via ${@...}; shell ${VAR:+...} would drop them since BitBake vars are
    # not exported into the task shell.
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
