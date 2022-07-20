#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest
import re


def validateMetadata(build, directory):
    data = build.files.readAsJson(os.path.join(directory, "metadata.json"))
    assert "S" in data
    assert "PWD" in data


def validateGTestReport(build, path, name, tests, failures):
    data = build.files.readAsXml(path)
    data = data["testsuites/testsuite"]
    matcher = lambda x: x["name"] == name and x["tests"] == tests and x["failures"] == failures
    if isinstance(data, list):
        assert any(map(matcher, data))
    else:
        assert matcher(data)


def validateQTestReport(build, path, name, tests, failures):
    data = build.files.readAsXml(path)
    data = data["testsuite"]
    matcher = lambda x: x["name"] == name and x["tests"] == tests and x["failures"] == failures
    assert matcher(data)


def validateCoverageReport(build, directory):
    data = build.files.readAsHtml(os.path.join(directory, "coverage/index.html"))
    assert data["html/body/table/tr/td"][1] == "LCOV - code coverage report"

    data = build.files.readAsXml(os.path.join(directory, "coverage/coverage.xml"))
    method_data = data["coverage/packages/package/classes/class/methods/method"]
    assert any(map(lambda x: x["name"] == "arithmetic::minus(int, int)" and x["line-rate"] == "1.0", method_data))
    assert any(map(lambda x: x["name"] == "arithmetic::plus(int, int)" and x["line-rate"] == "1.0", method_data))
    class_data = data["coverage/packages/package/classes/class"]
    assert any(map(lambda x: x["name"] == "test.MinusTest.cpp" and x["branch-rate"] != "0.0", class_data))
    assert any(map(lambda x: x["name"] == "test.PlusTest.cpp" and x["branch-rate"] != "0.0", class_data))


def validateCheckcodeReport(build, directory):
    data = build.files.readAsHtml(os.path.join(directory, "checkcode/index.html"))
    assert data["html/body/h1"] == "Sage Report"

    data = build.files.readAsJson(os.path.join(directory, "checkcode/sage_report.json"))
    assert "properties" in data
    assert "complexity" in data
    assert "duplications" in data
    assert "size" in data
    assert "violations" in data


def validateCheckcacheReport(build, directory):
    data = build.files.readAsJson(os.path.join(directory, "checkcache/caches.json"))
    assert "Missed" in data["Premirror"]
    assert "Found" in data["Premirror"]["Summary"]


def validateCheckrecipeReport(build, directory):
    data = build.files.readAsJson(os.path.join(directory, "checkrecipe/recipe_violations.json"))
    assert len(data["issues"]) == 0

    data = build.files.readAsJson(os.path.join(directory, "checkrecipe/files.json"))
    recipe = re.match(r"(?:.+\/)(.+)(?:-\d+(\.\d+)+)(?:-.+)", directory).group(1)
    assert data["lines_of_code"][0]["file"].endswith(recipe + "_1.0.0.bb")
    assert data["lines_of_code"][1]["file"].endswith(recipe + "_1.0.0.bbappend")


@pytest.fixture(scope="module")
def shared_report_build(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()
    return report_build


def test_cmake_project(shared_report_build):
    validateMetadata(shared_report_build, "report/cmake-project-1.0.0-r0")


def test_cmake_project_do_test(shared_report_build):
    validateGTestReport(shared_report_build, "report/cmake-project-1.0.0-r0/test/OperatorTest_1.xml", "PlusTest", "1", "1")
    validateGTestReport(shared_report_build, "report/cmake-project-1.0.0-r0/test/OperatorTest_3.xml", "MinusTest", "1", "1")


def test_cmake_project_do_coverage(shared_report_build):
    validateCoverageReport(shared_report_build, "report/cmake-project-1.0.0-r0")


def test_cmake_project_do_checkcode(shared_report_build):
    validateCheckcodeReport(shared_report_build, "report/cmake-project-1.0.0-r0")


def test_cmake_project_do_checkcache(shared_report_build):
    validateCheckcacheReport(shared_report_build, "report/cmake-project-1.0.0-r0")


def test_cmake_project_do_checkrecipe(shared_report_build):
    validateCheckrecipeReport(shared_report_build, "report/cmake-project-1.0.0-r0")


def test_qmake_project(shared_report_build):
    validateMetadata(shared_report_build, "report/qmake-project-1.0.0-r0")


def test_qmake_project_do_test(shared_report_build):
    validateGTestReport(shared_report_build, "report/qmake-project-1.0.0-r0/test/test-qt-gtest.xml", "PlusTest", "2", "1")
    validateGTestReport(shared_report_build, "report/qmake-project-1.0.0-r0/test/test-qt-gtest.xml", "MinusTest", "2", "1")
    validateQTestReport(shared_report_build, "report/qmake-project-1.0.0-r0/test/tests/plus_test/test_result.xml", "qmake-project.PlusTest", "4", "1")
    validateQTestReport(shared_report_build, "report/qmake-project-1.0.0-r0/test/tests/minus_test/test_result.xml", "qmake-project.MinusTest", "4", "1")


def test_qmake_project_do_coverage(shared_report_build):
    validateCoverageReport(shared_report_build, "report/qmake-project-1.0.0-r0")


def test_qmake_project_do_checkcode(shared_report_build):
    validateCheckcodeReport(shared_report_build, "report/qmake-project-1.0.0-r0")


def test_qmake_project_do_checkcache(shared_report_build):
    validateCheckcacheReport(shared_report_build, "report/qmake-project-1.0.0-r0")


def test_qmake_project_do_checkrecipe(shared_report_build):
    validateCheckrecipeReport(shared_report_build, "report/qmake-project-1.0.0-r0")


def test_autotools_project(shared_report_build):
    validateMetadata(shared_report_build, "report/autotools-project-1.0.0-r0")


def test_autotools_project_do_test(shared_report_build):
    validateGTestReport(shared_report_build, "report/autotools-project-1.0.0-r0/test/operatorTest.xml", "MinusTest", "2", "1")
    validateGTestReport(shared_report_build, "report/autotools-project-1.0.0-r0/test/operatorTest.xml", "PlusTest", "2", "1")


def test_autotools_project_do_coverage(shared_report_build):
    validateCoverageReport(shared_report_build, "report/autotools-project-1.0.0-r0")


def test_autotools_project_do_checkcode(shared_report_build):
    validateCheckcodeReport(shared_report_build, "report/autotools-project-1.0.0-r0")


def test_autotools_project_do_checkcache(shared_report_build):
    validateCheckcacheReport(shared_report_build, "report/autotools-project-1.0.0-r0")


def test_autotools_project_do_checkrecipe(shared_report_build):
    validateCheckrecipeReport(shared_report_build, "report/autotools-project-1.0.0-r0")
