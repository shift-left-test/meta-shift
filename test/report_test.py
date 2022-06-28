#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest


NORMAL_GT_PLUS_TEST_FAILED_LOG = 'testsuite name="PlusTest" tests="2" failures="1" disabled="0" errors="0"'
NORMAL_GT_MINUS_TEST_FAILED_LOG = 'testsuite name="MinusTest" tests="2" failures="1" disabled="0" errors="0"'
CMAKE_GT_PLUS_TEST_FAILED_LOG = 'testsuite name="PlusTest" tests="1" failures="1" disabled="0" errors="0"'
CMAKE_GT_MINUS_TEST_FAILED_LOG = 'testsuite name="MinusTest" tests="1" failures="1" disabled="0" errors="0"'
QT_PLUS_TEST_FAILED_LOG = 'testsuite errors="0" failures="1" tests="4" name="qmake-project.PlusTest"'
QT_MINUS_TEST_FAILED_LOG = 'testsuite errors="0" failures="1" tests="4" name="qmake-project.MinusTest"'
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
SAGE_HTML_TITLE = '<h1>Sage Report</h1>'
METADATA_S = '"S": "'


class REPORT:
    PF = {
        "cmake-project": "cmake-project-1.0.0-r0",
        "qmake-project": "qmake-project-1.0.0-r0",
        "autotools-project": "autotools-project-1.0.0-r0",
        "humidifier-project": "humidifier-project-1.0.0-r0",
        "sqlite3wrapper": "sqlite3wrapper-0.1.0-r0",
    }

    @classmethod
    def ROOT(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], path)

    @classmethod
    def RESULT(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "test", path)

    @classmethod
    def COVERAGE(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "coverage", path)

    @classmethod
    def CHECK(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checkcode", path)

    @classmethod
    def CHECKCACHE(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checkcache", path)

    @classmethod
    def CHECKRECIPE(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checkrecipe", path)


@pytest.fixture(scope="module")
def shared_report_build(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()
    return report_build


def test_cmake_project(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("cmake-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("cmake-project", "OperatorTest.xml"))
    assert EXISTS(REPORT.COVERAGE("cmake-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("cmake-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("cmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("cmake-project", "index.html"))
    assert EXISTS(REPORT.CHECK("cmake-project", "style.css"))
    assert EXISTS(REPORT.CHECKCACHE("cmake-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("cmake-project", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("cmake-project", "files.json"))

    assert READ(REPORT.ROOT("cmake-project", "metadata.json")).contains(METADATA_S)


def test_cmake_project_do_test(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.RESULT("cmake-project", "OperatorTest_1.xml")) as f:
        assert f.contains('classname="cmake-project.PlusTest"')
        assert f.contains(CMAKE_GT_PLUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("cmake-project", "OperatorTest_3.xml")) as f:
        assert f.contains('classname="cmake-project.MinusTest"')
        assert f.contains(CMAKE_GT_MINUS_TEST_FAILED_LOG)


def test_cmake_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert READ(REPORT.COVERAGE("cmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("cmake-project", "coverage.xml")) as f:
        assert f.contains('name="cmake-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="cmake-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_cmake_project_do_checkcode(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECK("cmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')
    with READ(REPORT.CHECK("cmake-project", "index.html")) as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_cmake_project_do_checkcache(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKCACHE("cmake-project", "caches.json")) as f:
        assert f.contains('"Premirror": {')
        assert f.contains('"Summary": {')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')


def test_cmake_project_do_checkrecipe(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKRECIPE("cmake-project", "recipe_violations.json")) as f:
        assert f.contains('"issues": []')

    with READ(REPORT.CHECKRECIPE("cmake-project", "files.json")) as f:
        assert f.contains('cmake-project_1.0.0.bb')
        assert f.contains('cmake-project_1.0.0.bbappend')


def test_qmake_project(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("qmake-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("qmake-project", "test-qt-gtest.xml"))
    assert EXISTS(REPORT.RESULT("qmake-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(REPORT.RESULT("qmake-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(REPORT.COVERAGE("qmake-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("qmake-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("qmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("qmake-project", "index.html"))
    assert EXISTS(REPORT.CHECK("qmake-project", "style.css"))
    assert EXISTS(REPORT.CHECKCACHE("qmake-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake-project", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake-project", "files.json"))

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)


def test_qmake_project_do_test(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.RESULT("qmake-project", "test-qt-gtest.xml")) as f:
        assert f.contains('classname="qmake-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="qmake-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("qmake-project", "tests/plus_test/test_result.xml")) as f:
        assert f.contains('name="qmake-project.PlusTest"')
        assert f.contains(QT_PLUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("qmake-project", "tests/minus_test/test_result.xml")) as f:
        assert f.contains('name="qmake-project.MinusTest"')
        assert f.contains(QT_MINUS_TEST_FAILED_LOG)


def test_qmake_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert READ(REPORT.COVERAGE("qmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("qmake-project", "coverage.xml")) as f:
        assert f.contains('name="qmake-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="qmake-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_qmake_project_do_checkcode(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECK("qmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')
    with READ(REPORT.CHECK("qmake-project", "index.html")) as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_qmake_project_do_checkcache(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKCACHE("qmake-project", "caches.json")) as f:
        assert f.contains('"Premirror": {')
        assert f.contains('"Summary": {')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')


def test_qmake_project_do_checkrecipe(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKRECIPE("qmake-project", "recipe_violations.json")) as f:
        assert f.contains('"issues": []')

    with READ(REPORT.CHECKRECIPE("qmake-project", "files.json")) as f:
        assert f.contains('qmake-project_1.0.0.bb')
        assert f.contains('qmake-project_1.0.0.bbappend')


def test_autotools_project(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("autotools-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("autotools-project", "operatorTest.xml"))
    assert EXISTS(REPORT.COVERAGE("autotools-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("autotools-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("autotools-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("autotools-project", "index.html"))
    assert EXISTS(REPORT.CHECK("autotools-project", "style.css"))
    assert EXISTS(REPORT.CHECKCACHE("autotools-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("autotools-project", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("autotools-project", "files.json"))

    assert READ(REPORT.ROOT("autotools-project", "metadata.json")).contains(METADATA_S)


def test_autotools_project_do_test(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.RESULT("autotools-project", "operatorTest.xml")) as f:
        assert f.contains('classname="autotools-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="autotools-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)


def test_autotools_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert READ(REPORT.COVERAGE("autotools-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("autotools-project", "coverage.xml")) as f:
        assert f.contains('name="autotools-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="autotools-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_autotools_project_do_checkcode(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECK("autotools-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')
    with READ(REPORT.CHECK("autotools-project", "index.html")) as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_autotools_project_do_checkcache(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKCACHE("autotools-project", "caches.json")) as f:
        assert f.contains('"Premirror": {')
        assert f.contains('"Summary": {')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')


def test_autotools_project_do_checkrecipe(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKRECIPE("autotools-project", "recipe_violations.json")) as f:
        assert f.contains('"issues": []')

    with READ(REPORT.CHECKRECIPE("autotools-project", "files.json")) as f:
        assert f.contains('autotools-project_1.0.0.bb')
        assert f.contains('autotools-project_1.0.0.bbappend')


def test_humidifier_project(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("humidifier-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("humidifier-project", "unittest.xml"))
    assert EXISTS(REPORT.COVERAGE("humidifier-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("humidifier-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("humidifier-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("humidifier-project", "index.html"))
    assert EXISTS(REPORT.CHECK("humidifier-project", "style.css"))
    assert EXISTS(REPORT.CHECKCACHE("humidifier-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("humidifier-project", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("humidifier-project", "files.json"))

    assert READ(REPORT.ROOT("humidifier-project", "metadata.json")).contains(METADATA_S)


def test_humidifier_project_do_test(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert READ(REPORT.RESULT("humidifier-project", "unittest.xml")).contains('classname="humidifier-project.HumidifierTest"')


def test_humidifier_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert READ(REPORT.COVERAGE("humidifier-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("humidifier-project", "coverage.xml")) as f:
        assert f.contains('name="humidifier-project.humidifier.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="Humidifier::setPreferredHumidity(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="Atomizer_Set(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="FakeHumiditySensor::getHumidityLevel() const" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="FakeHumiditySensor::gmock_getHumidityLevel() const" signature="">')


def test_humidifier_project_do_checkcode(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECK("humidifier-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')
    with READ(REPORT.CHECK("humidifier-project", "index.html")) as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_humidifier_project_do_checkcache(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKCACHE("humidifier-project", "caches.json")) as f:
        assert f.contains('"Premirror": {')
        assert f.contains('"Summary": {')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')


def test_humidifier_project_do_checkcache(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKRECIPE("humidifier-project", "recipe_violations.json")) as f:
        assert f.contains('"issues": []')

    with READ(REPORT.CHECKRECIPE("humidifier-project", "files.json")) as f:
        assert f.contains('humidifier-project_1.0.0.bb')
        assert f.contains('humidifier-project_1.0.0.bbappend')


def test_sqlite3wrapper(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("sqlite3wrapper", "metadata.json"))
    assert EXISTS(REPORT.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml"))
    assert EXISTS(REPORT.COVERAGE("sqlite3wrapper", "index.html"))
    assert EXISTS(REPORT.COVERAGE("sqlite3wrapper", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("sqlite3wrapper", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("sqlite3wrapper", "index.html"))
    assert EXISTS(REPORT.CHECK("sqlite3wrapper", "style.css"))
    assert EXISTS(REPORT.CHECKCACHE("sqlite3wrapper", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("sqlite3wrapper", "files.json"))

    assert READ(REPORT.ROOT("sqlite3wrapper", "metadata.json")).contains(METADATA_S)


def test_sqlite3wrapper_do_test(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert READ(REPORT.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml")).contains('classname="sqlite3wrapper.DatabaseTest"')


def test_sqlite3wrapper_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert READ(REPORT.COVERAGE("sqlite3wrapper", "index.html")).contains(LCOV_HTML_TITLE)
    with READ(REPORT.COVERAGE("sqlite3wrapper", "coverage.xml")) as f:
        assert f.contains('name="sqlite3wrapper.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Column::getName() const" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Statement::check(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Database::check(int)" signature="">')


def test_sqlite3wrapper_do_checkcode(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECK("sqlite3wrapper", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')
    with READ(REPORT.CHECK("sqlite3wrapper", "index.html")) as f:
        assert f.contains(SAGE_HTML_TITLE)


def test_sqlite3wrapper_do_checkcache(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKCACHE("sqlite3wrapper", "caches.json")) as f:
        assert f.contains('"Premirror": {')
        assert f.contains('"Summary": {')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')


def test_sqlite3wrapper_do_checkrecipe(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json")) as f:
        assert f.contains('"issues": []')

    with READ(REPORT.CHECKRECIPE("sqlite3wrapper", "files.json")) as f:
        assert f.contains('sqlite3wrapper_0.1.0.bb')
        assert f.contains('sqlite3wrapper_0.1.0.bbappend')
