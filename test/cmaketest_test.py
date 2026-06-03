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
        assert not o.stdout.contains("AOR : plus/plus.cpp (30:12-30:13 -> *)")


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
        assert data["html/body/table/tr/td"][1] == "LCOV - code coverage report"
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml") as data:
        method_data = data["coverage/packages/package/classes/class/methods/method"]
        assert any(map(lambda x: x["name"] == "arithmetic::minus(int, int)" and x["line-rate"] == "1.0", method_data))
        assert any(map(lambda x: x["name"] == "arithmetic::plus(int, int)" and x["line-rate"] == "1.0", method_data))
        class_data = data["coverage/packages/package/classes/class"]
        assert any(map(lambda x: x["name"] == "test.MinusTest.cpp" and x["branch-rate"] != "0.0", class_data))
        assert any(map(lambda x: x["name"] == "test.PlusTest.cpp" and x["branch-rate"] != "0.0", class_data))


def test_do_coverage_branch(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_BRANCH", "0")
        assert report.shell.execute("bitbake cmake-project -c coverage").stderr.empty()
        with report.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml") as data:
            assert data["coverage"]["branch-rate"] == "0.0"


def test_do_coverage_excludes(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_EXCLUDES", "program *us/*.cpp test/MinusTest.cpp")
        assert report.shell.execute("bitbake cmake-project -c coverage").stderr.empty()
        with report.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml") as data:
            assert data["coverage/packages/package/classes/class"]["filename"] != "minus/minus.cpp"
            assert data["coverage/packages/package/classes/class"]["filename"] != "plus/plus.cpp"
            assert data["coverage/packages/package/classes/class"]["filename"] != "program/main.cpp"
            assert data["coverage/packages/package/classes/class"]["filename"] != "test/MinusTest.cpp"
            assert data["coverage/packages/package/classes/class"]["filename"] == "test/PlusTest.cpp"
            assert data["coverage/packages/package/classes/class"]["line-rate"] == "1.0"
            assert data["coverage/packages/package/classes/class"]["branch-rate"] != "0.0"


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
