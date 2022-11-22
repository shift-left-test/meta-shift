#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_build):
    with test_build.externalsrc("cmake-project"):
        return test_build.shell.execute("bitbake cmake-project -c report").stdout


@pytest.fixture(scope="module")
def report(report_build):
    report_build.files.remove("report")
    with report_build.externalsrc("cmake-project"):
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


def test_sage_native_project_do_build(report_build):
    # Test if the setuptools within devtool-modify works properly with the host python
    with report_build.externalsrc("sage-native"):
        o = report_build.shell.execute("bitbake sage-native -c build")
        assert o.stderr.empty()
        assert o.returncode == 0

