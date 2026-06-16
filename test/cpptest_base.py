#-*- coding: utf-8 -*-

"""
Copyright (c) 2026 LG Electronics Inc.
SPDX-License-Identifier: MIT

Shared assertions for the C/C++ build-system test modules
(cmaketest/autotoolstest/qmaketest). Only build-system-independent behaviour
lives here; per-build-system banners and test-report layouts stay in the
individual *_test.py modules. This is a helper module, not a test module
(its name does not match python_files, so pytest never collects it).
"""

from selftest.parsers.data import asList


def assert_checktest_summary(stdout, report, recipe):
    assert stdout.matches(recipe + "-1.0.0-r0 do_checktest:[ ]+Mutant Generation Summary")
    assert stdout.matches(recipe + "-1.0.0-r0 do_checktest:[ ]+Mutation Score Report")
    # do_checktest synthesises its own run.do_test for sentinel; the streamed
    # output must not carry do_test's "<PF> do_test:" prefix on top of the outer
    # "<PF> do_checktest:" one.
    assert not stdout.contains(recipe + "-1.0.0-r0 do_checktest: " + recipe + "-1.0.0-r0 do_test:")
    with report.files.readAsXml("report/" + recipe + "-1.0.0-r0/checktest/mutations.xml") as data:
        assert len(data["mutations/mutation"]) == 2


def assert_arithmetic_coverage(report, recipe):
    with report.files.readAsHtml("report/" + recipe + "-1.0.0-r0/coverage/index.html") as data:
        assert data["html/head/title"] == "GCC Code Coverage Report"
    with report.files.readAsXml("report/" + recipe + "-1.0.0-r0/coverage/coverage.xml") as data:
        class_data = asList(data["coverage/packages/package/classes/class"])
        # Per-file line rates depend on the project link model and qemu-user
        # counter flushing, so assert presence here and exact coverage on the
        # in-process unit tests, which run identically across projects and gcovr
        # versions.
        filenames = [x["filename"] for x in class_data]
        assert "minus/minus.cpp" in filenames
        assert "plus/plus.cpp" in filenames
        assert any(x["filename"] == "test/MinusTest.cpp" and float(x["branch-rate"]) > 0.0 for x in class_data)
        assert any(x["filename"] == "test/PlusTest.cpp" and float(x["branch-rate"]) > 0.0 for x in class_data)
        # gcovr >= 8.6 emits per-method entries in the Cobertura report; when
        # present, check the demangled arithmetic operators are reported.
        method_data = asList(data.get("coverage/packages/package/classes/class/methods/method"))
        if method_data:
            names = [x["name"] for x in method_data]
            assert "arithmetic::minus" in names
            assert "arithmetic::plus" in names


def assert_coverage_branch_in_xml(report, recipe):
    # gcovr records branch coverage in the Cobertura report regardless of the
    # SHIFT_COVERAGE_BRANCH text-report toggle (which only changes stdout).
    with report.files.readAsXml("report/" + recipe + "-1.0.0-r0/coverage/coverage.xml") as data:
        assert float(data["coverage"]["branch-rate"]) > 0.0


def assert_coverage_branch_text(report, recipe):
    # SHIFT_COVERAGE_BRANCH=1 switches the text report from line to branch
    # coverage, so the table header becomes "Branches  Taken" instead of "Lines  Exec".
    with report.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_BRANCH", "1")
        o = report.shell.execute("bitbake " + recipe + " -c coverage")
        assert o.stderr.empty()
        assert o.stdout.matches(recipe + "-1.0.0-r0 do_coverage:.*Branches.*Taken")


def assert_coverage_excludes(report, recipe):
    with report.files.conf() as conf:
        # gcovr --exclude takes regexes matched against the source path.
        conf.set("SHIFT_COVERAGE_EXCLUDES", ".*/program/.* .*/minus/.* .*/plus/.* .*/MinusTest.cpp")
        assert report.shell.execute("bitbake " + recipe + " -c coverage").stderr.empty()
        with report.files.readAsXml("report/" + recipe + "-1.0.0-r0/coverage/coverage.xml") as data:
            classes = asList(data["coverage/packages/package/classes/class"])
            filenames = [c["filename"] for c in classes]
            assert "minus/minus.cpp" not in filenames
            assert "plus/plus.cpp" not in filenames
            assert "program/main.cpp" not in filenames
            assert "test/MinusTest.cpp" not in filenames
            assert "test/PlusTest.cpp" in filenames
            plus = next(c for c in classes if c["filename"] == "test/PlusTest.cpp")
            # The exact per-file line rate depends on the GCC/gcovr version (newer
            # toolchains count the exception-cleanup lines around the failing test),
            # so assert the kept file carries real coverage rather than a fixed rate.
            assert float(plus["line-rate"]) > 0.0
            assert float(plus["branch-rate"]) > 0.0


def assert_coverage_extra_options(report, recipe):
    with report.files.conf() as conf:
        # SHIFT_COVERAGE_EXTRA_OPTIONS is passed verbatim to gcovr; --print-summary
        # makes gcovr emit a "lines: NN%" summary the default text report omits.
        conf.set("SHIFT_COVERAGE_EXTRA_OPTIONS", "--print-summary")
        o = report.shell.execute("bitbake " + recipe + " -c coverage")
        assert o.stderr.empty()
        assert o.stdout.matches(recipe + "-1.0.0-r0 do_coverage:.*lines:.*%")


def assert_verify_without_report_dir(test_build, recipe):
    o = test_build.shell.execute("bitbake " + recipe + " -c verify")
    assert o.stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")
    # do_checktest now runs console-only without a report dir (it used to be
    # skipped); sentinel still prints the mutation score.
    assert o.stdout.matches(recipe + "-1.0.0-r0 do_checktest:[ ]+Mutation Score Report")


def assert_test_html_report(report, recipe):
    # do_test renders the merged JUnit XML into a single index.html titled after PF.
    pf = recipe + "-1.0.0-r0"
    with report.files.readAsHtml("report/" + pf + "/test/index.html") as data:
        assert data["html/head/title"] == pf


def assert_test_filter(test_build, recipe):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_FILTER", "PlusTest.*-*Fail:*AlsoFail")
        stdout = test_build.shell.execute("bitbake " + recipe + " -c test").stdout
        # The runner stdout format differs per build system (cmake echoes gtest
        # case names; autotools' make-check and qmake's Qt test do not), so this
        # asserts only the excluded cases are absent, matching the original test.
        assert not stdout.containsAny(
            "PlusTest.testShouldFail",
            "MinusTest.testShouldReturnExpectedValue",
            "MinusTest.testShouldAlsoFail")


def assert_test_shuffle(test_build, recipe):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SHUFFLE", "1")
        first = test_build.shell.execute("bitbake " + recipe + " -c test").stdout
        second = test_build.shell.execute("bitbake " + recipe + " -c test").stdout
        assert first != second


def assert_test_suppress_failures(test_build, recipe):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SUPPRESS_FAILURES", "0")
        o = test_build.shell.execute("bitbake " + recipe + " -c test")
        assert o.returncode != 0
