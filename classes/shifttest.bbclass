DEPENDS_prepend = "\
    gtest \
    gmock \
    lcov-native \
    python-lcov-cobertura-native \
    qemu-native \
    cppcheck-native \
    cpplint-native \
    compiledb-native \
    sage-native \
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', 'sentinel-native', '', d)} \
    ${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', 'clang-cross-' + d.getVar('TUNE_ARCH', True) + ' ', '', d)} \
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

    cd ${B}
    # if 'compile_commands.json is generated by shifttest", then delete that
    if [ -f ".shift_compiledb_mark" ]; then
        if [ -f "compile_commands.json" ]; then
            bbdebug 1 "check compile_commands.json SHA"
            SHA_OUTPUT=$(sha256sum -c .shift_compiledb_mark) || true
            bbdebug 1 "${SHA_OUTPUT}"
            case ${SHA_OUTPUT} in
                *"compile_commands.json: OK"*)
                    bbdebug 1 "compile_commands.json is temporary generated. so it should be deleted"
                    rm -f compile_commands.json
                    ;;
                *)
                    bbdebug 1 "compile_commands.json is generated by other tool. don't delete"
                    ;;
            esac
        fi
        rm -f .shift_compiledb_mark
    fi

    if [ ! -f "compile_commands.json" ]; then
        bbdebug 1 "generate compile_commands.json & .shift_compiledb_mark"
        compiledb --command-style --output shift_compile_commands.json -n make
        local DIGEST=$(sha256sum shift_compile_commands.json | cut -f1 -d ' ')
        bbdebug 1 "$DIGEST"
        echo "${DIGEST} compile_commands.json" > .shift_compiledb_mark
        mv shift_compile_commands.json compile_commands.json
    else
        bbdebug 1 "compile_commands.json exists"
    fi

    sage --source-path ${S} --build-path ${B} --tool-path ${STAGING_DIR_NATIVE}${bindir} \
        --target-triple ${TARGET_SYS} \
        --verbose \
        ${OUTPUT_PATH_OPTION} \
        ${@" ".join([tool + ":" + d.getVarFlag("CHECKCODE_TOOL_OPTIONS", tool, True).replace(' ', '\ ') if d.getVarFlag("CHECKCODE_TOOL_OPTIONS", tool, True) else tool for tool in (d.getVar("CHECKCODE_TOOLS", True) or "").split()])} \
        2>&1 | shifttest_print_lines
}

# In order to overwrite the sstate cache libraries
do_install[nostamp] = "1"

addtask test after do_compile do_populate_sysroot
do_test[nostamp] = "1"
do_test[doc] = "Runs tests for the target"

shifttest_do_test() {
    bbfatal "'inherit shifttest' is not allowed. You should inherit an appropriate bbclass instead."
}

# $1 : report save path
shifttest_prepare_output_dir() {
    OUTPUT_PATH=$1
    mkdir -p "${OUTPUT_PATH}"
    rm -rf "${OUTPUT_PATH}/*"
    export GTEST_OUTPUT="xml:${OUTPUT_PATH}/"
}

shifttest_prepare_env() {
    export LD_LIBRARY_PATH="${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}"

    local LCOV_DATAFILE_BASE="${B}/coverage_base.info"

    lcov -c -i -d ${B} -o ${LCOV_DATAFILE_BASE} \
    --ignore-errors gcov \
    --gcov-tool ${TARGET_PREFIX}gcov \
    --rc lcov_branch_coverage=1
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
    local LCOV_DATAFILE_BASE="${B}/coverage_base.info"
    local LCOV_DATAFILE_TEST="${B}/coverage_test.info"
    local LCOV_DATAFILE_TOTAL="${B}/coverage_total.info"
    local LCOV_DATAFILE="${B}/coverage.info"

    rm -f ${LCOV_DATAFILE_TOTAL}
    rm -f ${LCOV_DATAFILE}

    if [ -z "$(find ${B} -name *.gcda -type f)" ]; then
        bbwarn "No .gcda files found at ${B}"
        return
    fi

    lcov -c -d ${B} -o ${LCOV_DATAFILE_TEST} \
        --ignore-errors gcov \
        --gcov-tool ${TARGET_PREFIX}gcov \
        --rc lcov_branch_coverage=1

    lcov -a ${LCOV_DATAFILE_BASE} \
         -a ${LCOV_DATAFILE_TEST} \
         -o ${LCOV_DATAFILE_TOTAL}

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

addtask checktest after do_compile do_populate_sysroot
do_checktest[nostamp] = "1"
do_checktest[doc] = "Runs mutation tests for the target"

CHECKTEST_DISABLED="${@bb.utils.contains('BBFILE_COLLECTIONS', 'clang-layer', '', 'has no clang layer', d)}"
CHECKTEST_WORKDIR="${WORKDIR}/mutation_test_tmp"
CHECKTEST_WORKDIR_ORIGINAL="${CHECKTEST_WORKDIR}/original"
CHECKTEST_WORKDIR_ACTUAL="${CHECKTEST_WORKDIR}/actual"
CHECKTEST_WORKDIR_BACKUP="${CHECKTEST_WORKDIR}/backup"
CHECKTEST_WORKDIR_EVAL="${CHECKTEST_WORKDIR}/eval"
CHECKTEST_MUTATION_MAXCOUNT ?= "10"
CHECKTEST_SCOPE ?= "commit"
CHECKTEST_EXTENSIONS ?= ""
CHECKTEST_EXCLUDES ?= ""

shifttest_checktest_compile_db_patch() {
    sed -r -e 's|("command": ".*)(")|\1 --target=${TARGET_SYS}\2|g' \
        ${B}/compile_commands.json > ${CHECKTEST_WORKDIR}/compile_commands.json
}

shifttest_checktest_prepare() {
    if [ -d ${CHECKTEST_WORKDIR} ]; then
        # restore & build
        shifttest_checktest_restore_from_backup
        shifttest_checktest_build

        rm -rf ${CHECKTEST_WORKDIR}
    fi

    mkdir ${CHECKTEST_WORKDIR}

    # create compile_commands.json if not exists
    if [ ! -f "${B}/compile_commands.json" ]; then
        cd ${B}
        compiledb --command-style make
        shifttest_checktest_compile_db_patch
        rm ${B}/compile_commands.json
    else
        shifttest_checktest_compile_db_patch
    fi
}

shifttest_checktest_restore_from_backup() {
    BACKUP_PATH=${CHECKTEST_WORKDIR_BACKUP}
    SOURCE_PATH=${S}

    if [ -d ${BACKUP_PATH} ]; then
        bbdebug 1 "start retore: ${BACKUP_PATH}"
        pushd ${BACKUP_PATH}
        find * -type f \
            -exec cp --parents "{}" "${SOURCE_PATH}" \; || true
        popd
    fi

    rm -rf ${BACKUP_PATH}
}

shifttest_checktest_populate() {
    bbdebug 1 "start populate"
    sentinel populate \
        --build ${CHECKTEST_WORKDIR} \
        --scope ${CHECKTEST_SCOPE} \
        --output ${CHECKTEST_WORKDIR}/mutables.db \
        --limit ${CHECKTEST_MUTATION_MAXCOUNT} \
        ${@' '.join([ '--extensions=' + ext + ' ' for ext in d.getVar('CHECKTEST_EXTENSIONS', True).split()])} \
        ${@' '.join([ '--exclude=' + ext + ' ' for ext in d.getVar('CHECKTEST_EXCLUDES', True).split()])} \
        ${S} | shifttest_print_lines
    bbdebug 1 "end populate"
}

shifttest_checktest_mutate() {
    MUTABLE=$1

    sentinel mutate \
        --input ${MUTABLE} \
        --backup ${CHECKTEST_WORKDIR_BACKUP} \
        ${S} | shifttest_print_lines
}

shifttest_checktest_build() {
    cd ${B}
    bbdebug 1 "compile"
    do_compile
    bbdebug 1 "install"
    do_install
}

shifttest_checktest_evaluate() {
    MUTABLE=$1

    sentinel evaluate \
        --input ${MUTABLE} \
        --expected ${CHECKTEST_WORKDIR_ORIGINAL} \
        --actual ${CHECKTEST_WORKDIR_ACTUAL} \
        --output ${CHECKTEST_WORKDIR_EVAL} \
        | shifttest_print_lines
}

shifttest_checktest_report() {
    bbdebug 1 "checktest report"

    if [ -z "${TEST_REPORT_OUTPUT}" ]; then
        sentinel report \
            --input ${CHECKTEST_WORKDIR_EVAL} \
            ${S} | shifttest_print_lines
    else
        OUTPUT_PATH="${TEST_REPORT_OUTPUT}/${PF}/checktest"
        mkdir -p "${OUTPUT_PATH}"
        rm -rf "${OUTPUT_PATH}/*"
        sentinel report \
            --input ${CHECKTEST_WORKDIR_EVAL} \
            --output ${OUTPUT_PATH} \
            ${S} | shifttest_print_lines
    fi
    bbdebug 1 "checktest report end"
}

shifttest_do_checktest() {
    bbfatal "'inherit shifttest' is not allowed. You should inherit an appropriate bbclass instead."
}
