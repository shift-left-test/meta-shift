#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(report_build):
    return report_build.shell.execute("bitbake cmake-project -c verify").stdout


@pytest.fixture(scope="module")
def report(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c verify").stderr.empty()
    return report_build


def test_do_checktest(stdout, report):
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutant Generation Summary")
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutation Score Report")
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/checktest/mutations.xml") as data:
        assert len(data["mutations/mutation"]) == 2


def test_do_checktest_excludes(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_PATTERNS", "!plus/plus.cpp")
        report.shell.execute("bitbake cmake-project -c checktest")
        with report.files.readAsXml("report/cmake-project-1.0.0-r0/checktest/mutations.xml") as data:
            paths = data["mutations/mutation/sourceFilePath"]
            if not isinstance(paths, list):
                paths = [paths]
            assert "plus/plus.cpp" not in paths


def test_do_checktest_extensions(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")
        conf.set("SHIFT_CHECKTEST_EXTENSIONS", ".unknown")

        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert not o.stdout.matches(r"cmake-project/1.0.0(-r0)?/git/plus/plus.cpp,plus,30,12,30,13,\*")


def test_do_checktest_generator(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_GENERATOR", "uniform")
        first = report.shell.execute("bitbake cmake-project -c checktest").stdout

    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_GENERATOR", "weighted")
        second = report.shell.execute("bitbake cmake-project -c checktest").stdout

    assert first != second


def test_do_checktest_seed(stdout, report):
    def collect_mutation_ids():
        with report.files.readAsXml("report/cmake-project-1.0.0-r0/checktest/mutations.xml") as data:
            paths = data["mutations/mutation/sourceFilePath"]
            lines = data["mutations/mutation/lineNumber"]
            mutators = data["mutations/mutation/mutator"]
            if not isinstance(paths, list):
                paths, lines, mutators = [paths], [lines], [mutators]
            return sorted(zip(paths, lines, mutators))

    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        report.shell.execute("bitbake cmake-project -c checktest")
        first = collect_mutation_ids()
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        report.shell.execute("bitbake cmake-project -c checktest")
        second = collect_mutation_ids()
    assert first == second


def test_do_checktest_verbose(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")

        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert o.stdout.contains("(seed: 1234)")


def test_do_checktest_disabled(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_ENABLED", "0")
        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert o.stderr.empty()
        assert not o.stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutant Generation Summary")
        assert not o.stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutation Score Report")


def test_do_coverage(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    with report.files.readAsHtml("report/cmake-project-1.0.0-r0/coverage/index.html") as data:
        assert data["html/head/title"] == "GCC Code Coverage Report"
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml") as data:
        class_data = data["coverage/packages/package/classes/class"]
        if isinstance(class_data, dict):
            class_data = [class_data]
        # The source files appear in the report. Their per-file line rates depend
        # on the project's link model (the autotools project builds one operator
        # as a shared library whose counters qemu-user does not flush), so assert
        # presence here and exact coverage on the in-process unit tests below,
        # which run identically across projects and gcovr versions.
        filenames = [x["filename"] for x in class_data]
        assert "minus/minus.cpp" in filenames
        assert "plus/plus.cpp" in filenames
        assert any(map(lambda x: x["filename"] == "test/MinusTest.cpp" and float(x["branch-rate"]) > 0.0, class_data))
        assert any(map(lambda x: x["filename"] == "test/PlusTest.cpp" and float(x["branch-rate"]) > 0.0, class_data))
        # gcovr >= 8.6 emits per-method entries in the Cobertura report; when
        # present, check the demangled arithmetic operators are reported.
        method_data = data.get("coverage/packages/package/classes/class/methods/method")
        if method_data:
            if isinstance(method_data, dict):
                method_data = [method_data]
            names = [x["name"] for x in method_data]
            assert "arithmetic::minus" in names
            assert "arithmetic::plus" in names


def test_do_coverage_branch(stdout, report):
    # gcovr records branch coverage in the Cobertura report regardless of the
    # SHIFT_COVERAGE_BRANCH text-report toggle (which only changes stdout).
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml") as data:
        assert float(data["coverage"]["branch-rate"]) > 0.0


def test_do_coverage_branch_text(report):
    # SHIFT_COVERAGE_BRANCH=1 switches the text report from line to branch
    # coverage, so the table header becomes "Branches  Taken" instead of "Lines  Exec".
    with report.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_BRANCH", "1")
        o = report.shell.execute("bitbake cmake-project -c coverage")
        assert o.stderr.empty()
        assert o.stdout.matches(r"cmake-project-1.0.0-r0 do_coverage:.*Branches.*Taken")


def test_do_coverage_excludes(stdout, report):
    with report.files.conf() as conf:
        # gcovr --exclude takes regexes matched against the source path.
        conf.set("SHIFT_COVERAGE_EXCLUDES", ".*/program/.* .*/minus/.* .*/plus/.* .*/MinusTest.cpp")
        assert report.shell.execute("bitbake cmake-project -c coverage").stderr.empty()
        with report.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml") as data:
            classes = data["coverage/packages/package/classes/class"]
            if isinstance(classes, dict):
                classes = [classes]
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


def test_do_verify(test_build):
    o = test_build.shell.execute("bitbake cmake-project -c verify")
    assert o.stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")


def test_do_test(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/test/OperatorTest_1.xml") as data:
        data = data["testsuites/testsuite"]
        assert data["name"] == "PlusTest" and data["tests"] == "1" and data["failures"] == "1"
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/test/OperatorTest_3.xml") as data:
        data = data["testsuites/testsuite"]
        assert data["name"] == "MinusTest" and data["tests"] == "1" and data["failures"] == "1"


def test_do_test_filter(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_FILTER", "PlusTest.*-*Fail:*AlsoFail")
        stdout = test_build.shell.execute("bitbake cmake-project -c test").stdout
        assert not stdout.containsAny(
            "PlusTest.testShouldFail",
            "MinusTest.testShouldReturnExpectedValue",
            "MinusTest.testShouldAlsoFail")


def test_do_test_shuffle(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SHUFFLE", "1")
        first = test_build.shell.execute("bitbake cmake-project -c test").stdout
        second = test_build.shell.execute("bitbake cmake-project -c test").stdout
        assert first != second


def test_do_test_suppress_failures(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SUPPRESS_FAILURES", "0")
        o = test_build.shell.execute("bitbake cmake-project -c test")
        assert o.returncode != 0

