inherit cmake
inherit shifttest
inherit shiftutils

OECMAKE_C_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"
OECMAKE_CXX_FLAGS_append = " -O0 -fprofile-arcs -ftest-coverage"

EXTRA_OECMAKE_append = " -DCMAKE_CROSSCOMPILING_EMULATOR='${@shiftutils_qemu_cmake_emulator(d)}'"
EXTRA_OECMAKE_append = " -DCMAKE_EXPORT_COMPILE_COMMANDS=ON"

cmake_do_compile_prepend() {
    export TARGET_SYS="${TARGET_SYS}"
}

python cmaketest_do_checkcode() {
    bb.build.exec_func("shifttest_do_checkcode", d)
}

python cmaketest_do_test() {
    dd = d.createCopy()
    env = os.environ.copy()

    # To access the shared libraries of other packages
    env["LD_LIBRARY_PATH"] = dd.expand("${SYSROOT_DESTDIR}${libdir}:${LD_LIBRARY_PATH}")

    configured = dd.getVar("SHIFT_REPORT_DIR", True)

    if configured:
        report_dir = dd.expand("${SHIFT_REPORT_DIR}/${PF}/test")
        mkdirhier(report_dir, True)

        # Create Google test report files
        env["GTEST_OUTPUT"] = "xml:%s/" % report_dir

    # Prepare for the coverage reports
    check_call(["lcov", "-c", "-i",
                "-d", dd.getVar("B", True),
                "-o", dd.expand("${B}/coverage_base.info"),
                "--ignore-errors", "gcov",
                "--gcov-tool", dd.expand("${TARGET_PREFIX}gcov"),
                "--rc", "lcov_branch_coverage=1"], dd)

    plain("Running tests...", dd)
    try:
        timeout(exec_proc, "ctest --output-on-failure", dd, env=env, cwd=dd.getVar("B", True))
    except bb.process.ExecutionError as e:
        if e.exitcode == 124:
            raise e
        pass

    if configured:
        if os.path.exists(report_dir):
            # Prepend the package name to each of the classname tags for GTest reports
            xml_files = find_files(report_dir, "*.xml")
            replace_files(xml_files, 'classname="', dd.expand('classname="${PN}.'))
        else:
            warn("No test report files found at %s" % report_dir, dd)
}

python cmaketest_do_coverage() {
    bb.build.exec_func("shifttest_do_coverage", d)
}

EXPORT_FUNCTIONS do_checkcode do_test do_coverage
