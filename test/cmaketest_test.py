#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_build):
    return test_build.shell.execute("bitbake cmake-project -c report").stdout


@pytest.fixture(scope="module")
def report(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c report").stderr.empty()
    return report_build


def test_do_checkcache(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")
    with report.files.readAsJson("report/cmake-project-1.0.0-r0/checkcache/caches.json") as data:
        assert "Missed" in data["Premirror"]
        assert "Found" in data["Premirror"]["Summary"]


def test_do_checkcode(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    with report.files.readAsHtml("report/cmake-project-1.0.0-r0/checkcode/index.html") as data:
        assert data["html/body/h1"] == "Sage Report"
    with report.files.readAsJson("report/cmake-project-1.0.0-r0/checkcode/sage_report.json") as data:
        assert all(map(lambda x: x in data, ["properties", "complexity", "duplications", "size", "violations"]))


def test_do_checkrecipe(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    with report.files.readAsJson("report/cmake-project-1.0.0-r0/checkrecipe/recipe_violations.json") as data:
        assert len(data["issues"]) == 0
    with report.files.readAsJson("report/cmake-project-1.0.0-r0/checkrecipe/files.json") as data:
        assert data["lines_of_code"][0]["file"].endswith("cmake-project_1.0.0.bb")
        assert data["lines_of_code"][1]["file"].endswith("cmake-project_1.0.0.bbappend")


def test_do_checktest(stdout, report):
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutant Population Report")
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutation Coverage Report")
    with report.files.readAsHtml("report/cmake-project-1.0.0-r0/checktest/index.html") as data:
        assert data["html/body/h1"] == "Sentinel Mutation Coverage Report"
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/checktest/mutations.xml") as data:
        assert len(data["mutations/mutation"]) == 2


def test_do_checktest_excludes(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")
        conf.set("SHIFT_CHECKTEST_EXCLUDES", "minus.cpp plus/plus.cpp")

        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert o.stdout.contains("exclude: plus/plus.cpp")
        assert o.stdout.contains("Mutation Coverage Report")
        assert not o.stdout.contains("AOR : plus/plus.cpp (30:12-30:13 -> *)")
        assert not o.stdout.contains("exclude: minus.cpp")


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
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")

        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert o.stdout.contains("AOR : plus/plus.cpp (30:12-30:13 -> *)")
        assert o.stdout.contains("AOR : program/main.cpp (37:39-37:40 -> *)")

        o = report.shell.execute("bitbake cmake-project -c checktestall")
        assert o.stdout.contains("AOR : plus/plus.cpp (30:12-30:13 -> *)")
        assert o.stdout.contains("AOR : program/main.cpp (37:39-37:40 -> *)")


def test_do_checktest_verbose(stdout, report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")

        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checktest: CommandPopulate [INFO] random seed:1234")


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


def test_do_report(stdout, report):
    assert stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")


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
