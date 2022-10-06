inherit shifttest


do_compile:append:class-target() {
    bbnote "Installing node modules..."
    STATUS=0
    npm install || eval "STATUS=\$?"
    if [ ${STATUS} -ne 0 ]; then
        bbfatal "Failed to install node modules."
    fi

    bbnote "Checking if @enact/cli installed..."
    npm list @enact/cli || eval "STATUS=\$?"
    if [ ${STATUS} -ne 0 ]; then
        bbnote "Installing @enact/cli..."
        npm install @enact/cli
    fi

    bbnote "Checking if jest-junit installed..."
    npm list jest-junit || eval "STATUS=\$?"
    if [ ${STATUS} -ne 0 ]; then
        bbnote "Installing jest-junit..."
        npm install jest-junit --save-dev
    fi
}

python enacttest_do_checkcode() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    env = os.environ.copy()
    env["HOME"] = d.getVar("WORKDIR")

    cmd = ["npm", "run", "lint", "--"]
    excludes = shlex_split(d.getVar("SHIFT_CHECKCODE_EXCLUDES", True))
    if len(excludes) > 0:
        cmd.extend(["--ignore-pattern '%s'" % exclude for exclude in excludes])

    # Run enact lint
    try:
        exec_proc(cmd, d, env=env, cwd=d.getVar("S", True))
    except bb.process.ExecutionError as e:
        if e.exitcode != 1:  # Ignore linting errors
            error("Failed to run static analysis: %s" % e, d)

    # Configure the output path argument
    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcode")
        mkdirhier(report_dir, True)

        save_metadata(d)

        # Collect the lines of code data
        data = {}
        data["size"] = []

        patterns = ["*.js", "*.jsx", "*.ts", "*.tsx"]
        files = sum([find_files(d.getVar("S", True), pattern) for pattern in patterns], [])
        excludes = ["node_modules/", "build/", "dist/", "coverage/"]
        files = filter(lambda f: not any(exclude in f[len(d.getVar("S", True)):] for exclude in excludes), files)
        files = filter(lambda f: not os.path.basename(f).startswith("."), files)
        for f in files:
            with open(f, "r", encoding="utf-8", errors="ignore") as fd:
                data["size"].append({
                    "file": os.path.relpath(f, os.getcwd()),
                    "total_lines": sum(1 for line in fd)
                })
        save_as_json(data, d.expand("${SHIFT_REPORT_DIR}/${PF}/checkcode/sage_report.json"))
}

python enacttest_do_test() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    env = os.environ.copy()
    env["HOME"] = d.getVar("WORKDIR")

    cmd = ["npm", "test", "--"]

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        mkdirhier(report_dir, True)
        env["JEST_JUNIT_OUTPUT_DIR"] = report_dir
        cmd.append("--reporters=default")
        cmd.append("--reporters=jest-junit")
        save_metadata(d)

    # Redirect stderr to stdout to show test execution results.
    cmd.append("2>&1")

    plain("Running tests...", d)
    try:
        timeout(exec_proc, cmd, d, env=env, cwd=d.getVar("S", True))
    except bb.process.ExecutionError as e:
        if not bb.utils.to_boolean(d.getVar("SHIFT_TEST_SUPPRESS_FAILURES", True)):
            error(str(e), d)
}

python enacttest_do_coverage() {
    if isNativeCrossSDK(d.getVar("PN", True) or ""):
        warn("Unsupported class type of the recipe", d)
        return

    env = os.environ.copy()
    env["HOME"] = d.getVar("WORKDIR")

    cmd = ["npm", "test", "--", "--coverage"]

    if d.getVar("SHIFT_REPORT_DIR", True):
        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        mkdirhier(report_dir, True)
        env["JEST_JUNIT_OUTPUT_DIR"] = report_dir
        cmd.append('--reporters=default')
        cmd.append('--reporters=jest-junit')

        report_dir = d.expand("${SHIFT_REPORT_DIR}/${PF}/coverage")
        mkdirhier(report_dir, True)
        cmd.append('--coverageDirectory="%s"' % report_dir)
        cmd.append('--coverageReporters="text"')
        cmd.append('--coverageReporters="html"')
        cmd.append('--coverageReporters="cobertura"')

        save_metadata(d)

    # Redirect stderr to stdout to show test execution results.
    cmd.append("2>&1")

    plain("Running tests...", d)
    try:
        exec_proc(cmd, d, env=env, cwd=d.getVar("S", True))
    except bb.process.ExecutionError as e:
        if not bb.utils.to_boolean(d.getVar("SHIFT_TEST_SUPPRESS_FAILURES", True)):
            error(str(e), d)
}

enacttest_do_checktest() {
    :
}

python enacttest_do_checkrecipe() {
    shifttest_checkrecipe(d)
}

python enacttest_do_checkcache() {
    shifttest_checkcache(d)
}

python enacttest_do_report() {
    shifttest_report(d)
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage do_checktest do_checkrecipe do_checkcache do_report
