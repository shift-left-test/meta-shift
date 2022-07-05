#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest


TEST_LOG_TEST1_FAIL1 = {"tests":"1", "failures":"1"}
TEST_LOG_TEST2_FAIL1 = {"tests":"2", "failures":"1"}
TEST_LOG_TEST4_FAIL1 = {"tests":"4", "failures":"1"}
COVERAGE_LOG_100 = {"line-rate":"1.0", "branch-rate":"1.0"}
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
SAGE_HTML_TITLE = '<h1>Sage Report</h1>'
METADATAJSON_KEYS = {"S", "PWD"}
SAGEREPORTJSON_KEYS = {"properties", "complexity", "duplications", "size", "violations"}


@pytest.fixture(scope="module")
def shared_report_build(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()
    return report_build


def test_cmake_project(shared_report_build):
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/metadata.json")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/test/OperatorTest.xml")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/coverage/index.html")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/coverage/coverage.xml")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/checkcode/sage_report.json")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/checkcode/index.html")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/checkcode/style.css")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/checkcache/caches.json")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert shared_report_build.files.exists("report/cmake-project-1.0.0-r0/checkrecipe/files.json")

    assert METADATAJSON_KEYS == set(
        shared_report_build.files.asJson("report/cmake-project-1.0.0-r0/metadata.json").keys())


def test_cmake_project_do_test(shared_report_build):
    test1 = shared_report_build.files.asXml("report/cmake-project-1.0.0-r0/test/OperatorTest_1.xml")
    assert test1.containsElementWithAttrib("testcase", {"classname":"cmake-project.PlusTest"})
    assert test1.containsElementWithAttrib("testsuite", {"name":"PlusTest", **TEST_LOG_TEST1_FAIL1})

    test2 = shared_report_build.files.asXml("report/cmake-project-1.0.0-r0/test/OperatorTest_3.xml")
    assert test2.containsElementWithAttrib("testcase", {"classname":"cmake-project.MinusTest"})
    assert test2.containsElementWithAttrib("testsuite", {"name":"MinusTest", **TEST_LOG_TEST1_FAIL1})


def test_cmake_project_do_coverage(shared_report_build):
    assert shared_report_build.files.read("report/cmake-project-1.0.0-r0/coverage/index.html").contains(LCOV_HTML_TITLE)

    coverage = shared_report_build.files.asXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml")
    assert coverage.containsElementWithAttrib("package", {"name":"cmake-project.plus.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"arithmetic::plus(int, int)",
        **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("package", {"name":"cmake-project.minus.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"arithmetic::minus(int, int)",
        **COVERAGE_LOG_100})


def test_cmake_project_do_checkcode(shared_report_build):
    assert SAGEREPORTJSON_KEYS == set(
        shared_report_build.files.asJson("report/cmake-project-1.0.0-r0/checkcode/sage_report.json").keys())

    with shared_report_build.files.read("report/cmake-project-1.0.0-r0/checkcode/index.html") as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_cmake_project_do_checkcache(shared_report_build):
    caches = shared_report_build.files.asJson("report/cmake-project-1.0.0-r0/checkcache/caches.json")
    assert "Shared State" in caches
    assert "Missed" in caches["Premirror"]
    assert "Found" in caches["Premirror"]["Summary"]


def test_cmake_project_do_checkrecipe(shared_report_build):
    recipe_violations = shared_report_build.files.asJson("report/cmake-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert len(recipe_violations["issues"]) == 0

    files = shared_report_build.files.asJson("report/cmake-project-1.0.0-r0/checkrecipe/files.json")
    assert files["lines_of_code"][0]["file"].endswith('cmake-project_1.0.0.bb')
    assert files["lines_of_code"][1]["file"].endswith('cmake-project_1.0.0.bbappend')


def test_qmake_project(shared_report_build):
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/metadata.json")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/test/test-qt-gtest.xml")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/test/tests/plus_test/test_result.xml")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/test/tests/minus_test/test_result.xml")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/coverage/index.html")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/coverage/coverage.xml")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/checkcode/sage_report.json")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/checkcode/index.html")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/checkcode/style.css")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/checkcache/caches.json")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert shared_report_build.files.exists("report/qmake-project-1.0.0-r0/checkrecipe/files.json")

    assert METADATAJSON_KEYS == set(
        shared_report_build.files.asJson("report/qmake-project-1.0.0-r0/metadata.json").keys())


def test_qmake_project_do_test(shared_report_build):
    test1 = shared_report_build.files.asXml("report/qmake-project-1.0.0-r0/test/test-qt-gtest.xml")
    assert test1.containsElementWithAttrib("testcase", {"classname":"qmake-project.PlusTest"})
    assert test1.containsElementWithAttrib("testsuite", {"name":"PlusTest", **TEST_LOG_TEST2_FAIL1})
    assert test1.containsElementWithAttrib("testcase", {"classname":"qmake-project.MinusTest"})
    assert test1.containsElementWithAttrib("testsuite", {"name":"MinusTest", **TEST_LOG_TEST2_FAIL1})

    test2 = shared_report_build.files.asXml("report/qmake-project-1.0.0-r0/test/tests/plus_test/test_result.xml")
    assert test2.containsElementWithAttrib("testsuite", {"name":"qmake-project.PlusTest", **TEST_LOG_TEST4_FAIL1})

    test3 = shared_report_build.files.asXml("report/qmake-project-1.0.0-r0/test/tests/minus_test/test_result.xml")
    assert test3.containsElementWithAttrib("testsuite", {"name":"qmake-project.MinusTest", **TEST_LOG_TEST4_FAIL1})
    

def test_qmake_project_do_coverage(shared_report_build):
    assert shared_report_build.files.read("report/qmake-project-1.0.0-r0/coverage/index.html").contains(LCOV_HTML_TITLE)

    coverage = shared_report_build.files.asXml("report/qmake-project-1.0.0-r0/coverage/coverage.xml")
    assert coverage.containsElementWithAttrib("package", {"name":"qmake-project.plus.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"arithmetic::plus(int, int)",
        **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("package", {"name":"qmake-project.minus.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"arithmetic::minus(int, int)",
        **COVERAGE_LOG_100})


def test_qmake_project_do_checkcode(shared_report_build):
    assert SAGEREPORTJSON_KEYS == set(
        shared_report_build.files.asJson("report/qmake-project-1.0.0-r0/checkcode/sage_report.json").keys())

    with shared_report_build.files.read("report/qmake-project-1.0.0-r0/checkcode/index.html") as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_qmake_project_do_checkcache(shared_report_build):
    caches = shared_report_build.files.asJson("report/qmake-project-1.0.0-r0/checkcache/caches.json")
    assert "Shared State" in caches
    assert "Missed" in caches["Premirror"]
    assert "Found" in caches["Premirror"]["Summary"]


def test_qmake_project_do_checkrecipe(shared_report_build):
    recipe_violations = shared_report_build.files.asJson("report/qmake-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert len(recipe_violations["issues"]) == 0

    files = shared_report_build.files.asJson("report/qmake-project-1.0.0-r0/checkrecipe/files.json")
    assert files["lines_of_code"][0]["file"].endswith('qmake-project_1.0.0.bb')
    assert files["lines_of_code"][1]["file"].endswith('qmake-project_1.0.0.bbappend')


def test_autotools_project(shared_report_build):
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/metadata.json")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/test/operatorTest.xml")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/coverage/index.html")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/coverage/coverage.xml")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/checkcode/sage_report.json")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/checkcode/index.html")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/checkcode/style.css")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/checkcache/caches.json")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert shared_report_build.files.exists("report/autotools-project-1.0.0-r0/checkrecipe/files.json")

    assert METADATAJSON_KEYS == set(
        shared_report_build.files.asJson("report/autotools-project-1.0.0-r0/metadata.json").keys())


def test_autotools_project_do_test(shared_report_build):
    test = shared_report_build.files.asXml("report/autotools-project-1.0.0-r0/test/operatorTest.xml")
    assert test.containsElementWithAttrib("testcase", {"classname":"autotools-project.PlusTest"})
    assert test.containsElementWithAttrib("testsuite", {"name":"PlusTest", **TEST_LOG_TEST2_FAIL1})
    assert test.containsElementWithAttrib("testcase", {"classname":"autotools-project.MinusTest"})
    assert test.containsElementWithAttrib("testsuite", {"name":"MinusTest", **TEST_LOG_TEST2_FAIL1})


def test_autotools_project_do_coverage(shared_report_build):
    assert shared_report_build.files.read("report/autotools-project-1.0.0-r0/coverage/index.html").contains(LCOV_HTML_TITLE)

    coverage = shared_report_build.files.asXml("report/autotools-project-1.0.0-r0/coverage/coverage.xml")
    assert coverage.containsElementWithAttrib("package", {"name":"autotools-project.plus.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"arithmetic::plus(int, int)",
        **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("package", {"name":"autotools-project.minus.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"arithmetic::minus(int, int)",
        **COVERAGE_LOG_100})


def test_autotools_project_do_checkcode(shared_report_build):
    assert SAGEREPORTJSON_KEYS == set(
        shared_report_build.files.asJson("report/autotools-project-1.0.0-r0/checkcode/sage_report.json").keys())

    with shared_report_build.files.read("report/autotools-project-1.0.0-r0/checkcode/index.html") as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_autotools_project_do_checkcache(shared_report_build):
    caches = shared_report_build.files.asJson("report/autotools-project-1.0.0-r0/checkcache/caches.json")
    assert "Shared State" in caches
    assert "Missed" in caches["Premirror"]
    assert "Found" in caches["Premirror"]["Summary"]


def test_autotools_project_do_checkrecipe(shared_report_build):
    recipe_violations = shared_report_build.files.asJson("report/autotools-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert len(recipe_violations["issues"]) == 0

    files = shared_report_build.files.asJson("report/autotools-project-1.0.0-r0/checkrecipe/files.json")
    assert files["lines_of_code"][0]["file"].endswith('autotools-project_1.0.0.bb')
    assert files["lines_of_code"][1]["file"].endswith('autotools-project_1.0.0.bbappend') 


def test_humidifier_project(shared_report_build):
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/metadata.json")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/test/unittest.xml")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/coverage/index.html")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/coverage/coverage.xml")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/checkcode/sage_report.json")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/checkcode/index.html")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/checkcode/style.css")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/checkcache/caches.json")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert shared_report_build.files.exists("report/humidifier-project-1.0.0-r0/checkrecipe/files.json")

    assert METADATAJSON_KEYS == set(
        shared_report_build.files.asJson("report/humidifier-project-1.0.0-r0/metadata.json").keys())


def test_humidifier_project_do_test(shared_report_build):
    test = shared_report_build.files.asXml("report/humidifier-project-1.0.0-r0/test/unittest.xml")
    assert test.containsElementWithAttrib("testcase", {"classname":"humidifier-project.HumidifierTest"})


def test_humidifier_project_do_coverage(shared_report_build):
    assert shared_report_build.files.read("report/humidifier-project-1.0.0-r0/coverage/index.html").contains(LCOV_HTML_TITLE)

    coverage = shared_report_build.files.asXml("report/humidifier-project-1.0.0-r0/coverage/coverage.xml")
    assert coverage.containsElementWithAttrib("package", {"name":"humidifier-project.humidifier.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"Humidifier::setPreferredHumidity(int)",
        **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("method", {"name":"Atomizer_Set(int)",
        **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("method", {"name":"FakeHumiditySensor::getHumidityLevel() const",
        **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("method", {"name":"FakeHumiditySensor::gmock_getHumidityLevel() const",
        **COVERAGE_LOG_100})


def test_humidifier_project_do_checkcode(shared_report_build):
    assert SAGEREPORTJSON_KEYS == set(
        shared_report_build.files.asJson("report/humidifier-project-1.0.0-r0/checkcode/sage_report.json").keys())

    with shared_report_build.files.read("report/humidifier-project-1.0.0-r0/checkcode/index.html") as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_humidifier_project_do_checkcache(shared_report_build):
    caches = shared_report_build.files.asJson("report/humidifier-project-1.0.0-r0/checkcache/caches.json")
    assert "Shared State" in caches
    assert "Missed" in caches["Premirror"]
    assert "Found" in caches["Premirror"]["Summary"]


def test_humidifier_project_do_checkcache(shared_report_build):
    recipe_violations = shared_report_build.files.asJson("report/humidifier-project-1.0.0-r0/checkrecipe/recipe_violations.json")
    assert len(recipe_violations["issues"]) == 0

    files = shared_report_build.files.asJson("report/humidifier-project-1.0.0-r0/checkrecipe/files.json")
    assert files["lines_of_code"][0]["file"].endswith('humidifier-project_1.0.0.bb')
    assert files["lines_of_code"][1]["file"].endswith('humidifier-project_1.0.0.bbappend')


def test_sqlite3wrapper(shared_report_build):
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/metadata.json")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/test/SQLite3WrapperTest.exe.xml")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/coverage/index.html")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/coverage/coverage.xml")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/checkcode/sage_report.json")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/checkcode/index.html")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/checkcode/style.css")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/checkcache/caches.json")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/checkrecipe/recipe_violations.json")
    assert shared_report_build.files.exists("report/sqlite3wrapper-0.1.0-r0/checkrecipe/files.json")

    assert METADATAJSON_KEYS == set(
        shared_report_build.files.asJson("report/sqlite3wrapper-0.1.0-r0/metadata.json").keys())


def test_sqlite3wrapper_do_test(shared_report_build):
    test = shared_report_build.files.asXml("report/sqlite3wrapper-0.1.0-r0/test/SQLite3WrapperTest.exe.xml")
    assert test.containsElementWithAttrib("testcase", {"classname":"sqlite3wrapper.DatabaseTest"})


def test_sqlite3wrapper_do_coverage(shared_report_build):
    assert shared_report_build.files.read("report/sqlite3wrapper-0.1.0-r0/coverage/index.html").contains(LCOV_HTML_TITLE)

    coverage = shared_report_build.files.asXml("report/sqlite3wrapper-0.1.0-r0/coverage/coverage.xml")
    assert coverage.containsElementWithAttrib("package", {"name":"sqlite3wrapper.src"})
    assert coverage.containsElementWithAttrib("method", {"name":"SQLite3Wrapper::Column::getName() const",
         **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("method", {"name":"SQLite3Wrapper::Statement::check(int)",
         **COVERAGE_LOG_100})
    assert coverage.containsElementWithAttrib("method", {"name":"SQLite3Wrapper::Database::check(int)",
         **COVERAGE_LOG_100})


def test_sqlite3wrapper_do_checkcode(shared_report_build):
    assert SAGEREPORTJSON_KEYS == set(
        shared_report_build.files.asJson("report/sqlite3wrapper-0.1.0-r0/checkcode/sage_report.json").keys())

    with shared_report_build.files.read("report/sqlite3wrapper-0.1.0-r0/checkcode/index.html") as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_sqlite3wrapper_do_checkcache(shared_report_build):
    caches = shared_report_build.files.asJson("report/sqlite3wrapper-0.1.0-r0/checkcache/caches.json")
    assert "Shared State" in caches
    assert "Missed" in caches["Premirror"]
    assert "Found" in caches["Premirror"]["Summary"]


def test_sqlite3wrapper_do_checkrecipe(shared_report_build):
    recipe_violations = shared_report_build.files.asJson("report/sqlite3wrapper-0.1.0-r0/checkrecipe/recipe_violations.json")
    assert len(recipe_violations["issues"]) == 0

    files = shared_report_build.files.asJson("report/sqlite3wrapper-0.1.0-r0/checkrecipe/files.json")
    assert files["lines_of_code"][0]["file"].endswith('sqlite3wrapper_0.1.0.bb')
    assert files["lines_of_code"][1]["file"].endswith('sqlite3wrapper_0.1.0.bbappend')
