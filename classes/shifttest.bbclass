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

DEBUG_BUILD = "1"

shifttest_print_lines() {
    while IFS= read line; do
        bbplain "${PF} do_${BB_CURRENTTASK}: $line"
    done
}


def plain(s, d):
    if bb.utils.to_boolean(d.getVar("SHIFTTEST_QUIET", True)):
        return
    bb.plain(d.expand("${PF} do_${BB_CURRENTTASK}: ") + s)


def exec_func(func, d):
    bb.debug(2, "Executing the function: %s" % func)
    try:
        cwd = os.getcwd()
        bb.build.exec_func(func, d)
    finally:
        os.chdir(cwd)


def exec_funcs(func, d, prefuncs=True, postfuncs=True):
    bb.debug(2, "Executing the function and its preceeding ones: %s" % func)
    def preceedtasks(task):
        preceed = set()
        tasks = d.getVar("__BBTASKS", False)
        if task not in tasks:
            return preceed
        preceed.update(d.getVarFlag(task, "deps", True) or [])
        return preceed

    def runTask(task):
        if prefuncs:
            for func in (d.getVarFlag(task, "prefuncs", True) or "").split():
                exec_func(func, d)
        exec_func(task, d)
        if postfuncs:
            for func in (d.getVarFlag(task, "postfuncs", True) or "").split():
                exec_func(func, d)

    for task in preceedtasks(func):
        runTask(task)
    runTask(func)


def exec_proc(cmd, d, **options):
    if not "shell" in options:
        options["shell"] = True

    bb.debug(2, 'Executing the command: "%s"' % cmd)
    proc = bb.process.Popen(cmd, **options)

    for line in proc.stdout:
        plain(line.decode("utf-8").rstrip(), d)


addtask checkcode after do_compile
do_checkcode[nostamp] = "1"
do_checkcode[doc] = "Runs static analysis for the target"

python shifttest_do_checkcode() {
    # Configure default arguments
    kwargs = {
        "source-path": d.getVar("S", True),
        "build-path": d.getVar("B", True),
        "tool-path": d.expand("${STAGING_DIR_NATIVE}${bindir}"),
        "target-triple": d.getVar("TARGET_SYS", True),
        "output-path": "",
        "tool-options": "",
    }

    # Configure the output path argument
    if d.getVar("TEST_REPORT_OUTPUT", True):
        report_dir = d.expand("${TEST_REPORT_OUTPUT}/${PF}/checkcode")
        bb.debug(2, "Configuring the checkcode output path: %s" % report_dir)
        bb.utils.remove(report_dir, True)
        bb.utils.mkdirhier(report_dir)
        kwargs["output-path"] = "--output-path=%s" % report_dir

    # Configure tool options
    bb.debug(2, "Configuring the checkcode tool options")
    for tool in (d.getVar("CHECKCODE_TOOLS", True) or "").split():
        kwargs["tool-options"] += " " + tool
        options = d.getVarFlag("CHECKCODE_TOOL_OPTIONS", tool, True)
        if options:
            kwargs["tool-options"] += ":" + options.replace(" ", "\ ")

    try:
        # Make sure that the compile_commands.json file is available
        json_file = d.expand("${B}/compile_commands.json")
        temporary = False

        if not os.path.exists(json_file):
            plain("Creating the compile_commands.json using compiledb", d)
            exec_proc("compiledb --command-style -n make", d, cwd=d.getVar("B", True))
            temporary = True

        # Run sage
        exec_proc("sage --verbose " \
                  "--source-path {source-path} " \
                  "--build-path {build-path} " \
                  "--tool-path {tool-path} " \
                  "--target-triple {target-triple} " \
                  "{output-path} " \
                  "{tool-options}".format(**kwargs), d, cwd=d.getVar("B", True))
    finally:
        if temporary:
            bb.utils.remove(json_file)
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
CHECKTEST_MUTANT_GENERATOR ?= "uniform"

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
        --work-dir ${CHECKTEST_WORKDIR} \
        --build-dir ${CHECKTEST_WORKDIR} \
        --output-dir ${CHECKTEST_WORKDIR} \
        --generator ${CHECKTEST_MUTANT_GENERATOR} \
        --scope ${CHECKTEST_SCOPE} \
        --limit ${CHECKTEST_MUTATION_MAXCOUNT} \
        --mutants-file-name "mutables.db" \
        ${@' '.join([ '--extensions=' + ext + ' ' for ext in d.getVar('CHECKTEST_EXTENSIONS', True).split()])} \
        ${@' '.join([ '--exclude=' + ext + ' ' for ext in d.getVar('CHECKTEST_EXCLUDES', True).split()])} \
        ${S} | shifttest_print_lines
    bbdebug 1 "end populate"
}

shifttest_checktest_mutate() {
    MUTANT=$1

    bbdebug 1 "MUTANT: ${MUTANT}"

    sentinel mutate \
        --mutant "${MUTANT}" \
        --work-dir ${CHECKTEST_WORKDIR_BACKUP} \
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
    MUTANT=$1

    sentinel evaluate \
        --mutant "${MUTANT}" \
        --expected ${CHECKTEST_WORKDIR_ORIGINAL} \
        --actual ${CHECKTEST_WORKDIR_ACTUAL} \
        --output-dir ${CHECKTEST_WORKDIR_EVAL} \
        --test-state $2 \
        ${S} | shifttest_print_lines
}

shifttest_checktest_report() {
    bbdebug 1 "checktest report"

    if [ ! -z "${TEST_REPORT_OUTPUT}" ]; then
        OUTPUT_PATH="${TEST_REPORT_OUTPUT}/${PF}/checktest"
        mkdir -p "${OUTPUT_PATH}"
        rm -rf "${OUTPUT_PATH}/*"
    fi

    sentinel report \
        --evaluation-file ${CHECKTEST_WORKDIR_EVAL}/EvaluationResults \
        ${OUTPUT_PATH:+"--output-dir"} ${OUTPUT_PATH} \
        ${S} | shifttest_print_lines

    unset OUTPUT_PATH
    bbdebug 1 "checktest report end"
}

shifttest_do_checktest() {
    bbfatal "'inherit shifttest' is not allowed. You should inherit an appropriate bbclass instead."
}
