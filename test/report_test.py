#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest


LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
SAGE_HTML_TITLE = '<h1>Sage Report</h1>'
SENTINEL_HTML_TITLE = '<h1>Sentinel Mutation Coverage Report</h1>'
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

    @classmethod
    def CHECKTEST(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checktest", path)


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
    assert EXISTS(REPORT.CHECKTEST("cmake-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("cmake-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("cmake-project", "style.css"))

    assert READ(REPORT.ROOT("cmake-project", "metadata.json")).contains(METADATA_S)


def test_cmake_project_do_test(shared_report_build):
    ASXML = shared_report_build.files.asXml

    data1 = ASXML(REPORT.RESULT("cmake-project", "OperatorTest_1.xml"))
    assert data1.containsElementWithAttrib("testcase", {"classname":"cmake-project.PlusTest"})
    assert data1.containsElementWithAttrib("testsuite", {"name":"PlusTest", "tests":"1", 
        "failures":"1", "disabled":"0",  "errors":"0"})

    data2= ASXML(REPORT.RESULT("cmake-project", "OperatorTest_3.xml"))
    assert data2.containsElementWithAttrib("testcase", {"classname":"cmake-project.MinusTest"})
    assert data2.containsElementWithAttrib("testsuite", {"name":"MinusTest", "tests":"1", 
        "failures":"1", "disabled":"0",  "errors":"0"})


def test_cmake_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    assert READ(REPORT.COVERAGE("cmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    data = ASXML(REPORT.COVERAGE("cmake-project", "coverage.xml"))
    assert data.containsElementWithAttrib("package", {"name":"cmake-project.plus.src"})
    assert data.containsElementWithAttrib("method", {"name":"arithmetic::plus(int, int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("package", {"name":"cmake-project.minus.src"})
    assert data.containsElementWithAttrib("method", {"name":"arithmetic::minus(int, int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})


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
        assert f.contains('"Shared State": {')
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


def test_cmake_project_do_checktest(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    data = ASXML(REPORT.CHECKTEST("cmake-project", "mutations.xml"))
    assert data.containsElement("mutations")

    with READ(REPORT.CHECKTEST("cmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


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
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "style.css"))

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)


def test_qmake_project_do_test(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    data1 = ASXML(REPORT.RESULT("qmake-project", "test-qt-gtest.xml"))
    assert data1.containsElementWithAttrib("testcase", {"classname":"qmake-project.PlusTest"})
    assert data1.containsElementWithAttrib("testsuite", {"name":"PlusTest", "tests":"2", 
        "failures":"1", "disabled":"0",  "errors":"0"})
    assert data1.containsElementWithAttrib("testcase", {"classname":"qmake-project.MinusTest"})
    assert data1.containsElementWithAttrib("testsuite", {"name":"MinusTest", "tests":"2", 
        "failures":"1", "disabled":"0",  "errors":"0"})

    data2 = ASXML(REPORT.RESULT("qmake-project", "tests/plus_test/test_result.xml"))
    assert data2.containsElementWithAttrib("testcase", {"classname":"PlusTest"})
    assert data2.containsElementWithAttrib("testsuite", {"name":"qmake-project.PlusTest",
        "tests":"4", "failures":"1", "errors":"0"})

    data3 = ASXML(REPORT.RESULT("qmake-project", "tests/minus_test/test_result.xml"))
    assert data3.containsElementWithAttrib("testcase", {"classname":"MinusTest"})
    assert data3.containsElementWithAttrib("testsuite", {"name":"qmake-project.MinusTest",
        "tests":"4", "failures":"1", "errors":"0"})
    

def test_qmake_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    assert READ(REPORT.COVERAGE("qmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    data = ASXML(REPORT.COVERAGE("qmake-project", "coverage.xml"))
    assert data.containsElementWithAttrib("package", {"name":"qmake-project.plus.src"})
    assert data.containsElementWithAttrib("method", {"name":"arithmetic::plus(int, int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("package", {"name":"qmake-project.minus.src"})
    assert data.containsElementWithAttrib("method", {"name":"arithmetic::minus(int, int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})


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
        assert f.contains('"Shared State": {')
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


def test_qmake_project_do_checktest(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    data = ASXML(REPORT.CHECKTEST("qmake-project", "mutations.xml"))
    assert data.containsElement("mutations")

    with READ(REPORT.CHECKTEST("qmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


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
    assert EXISTS(REPORT.CHECKTEST("autotools-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("autotools-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("autotools-project", "style.css"))

    assert READ(REPORT.ROOT("autotools-project", "metadata.json")).contains(METADATA_S)


def test_autotools_project_do_test(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    data = ASXML(REPORT.RESULT("autotools-project", "operatorTest.xml"))
    assert data.containsElementWithAttrib("testcase", {"classname":"autotools-project.PlusTest"})
    assert data.containsElementWithAttrib("testsuite", {"name":"PlusTest", "tests":"2", 
        "failures":"1", "disabled":"0",  "errors":"0"})
    assert data.containsElementWithAttrib("testcase", {"classname":"autotools-project.MinusTest"})
    assert data.containsElementWithAttrib("testsuite", {"name":"MinusTest", "tests":"2",
        "failures":"1", "disabled":"0",  "errors":"0"})


def test_autotools_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    assert READ(REPORT.COVERAGE("autotools-project", "index.html")).contains(LCOV_HTML_TITLE)

    data = ASXML(REPORT.COVERAGE("autotools-project", "coverage.xml"))
    assert data.containsElementWithAttrib("package", {"name":"autotools-project.plus.src"})
    assert data.containsElementWithAttrib("method", {"name":"arithmetic::plus(int, int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("package", {"name":"autotools-project.minus.src"})
    assert data.containsElementWithAttrib("method", {"name":"arithmetic::minus(int, int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})


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
        assert f.contains('"Shared State": {')
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


def test_autotools_project_do_checktest(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    data = ASXML(REPORT.CHECKTEST("autotools-project", "mutations.xml"))
    assert data.containsElement("mutations")

    with READ(REPORT.CHECKTEST("autotools-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


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
    ASXML = shared_report_build.files.asXml

    data = ASXML(REPORT.RESULT("humidifier-project", "unittest.xml"))
    assert data.containsElementWithAttrib("testcase", {"classname":"humidifier-project.HumidifierTest"})


def test_humidifier_project_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    assert READ(REPORT.COVERAGE("humidifier-project", "index.html")).contains(LCOV_HTML_TITLE)

    data = ASXML(REPORT.COVERAGE("humidifier-project", "coverage.xml"))
    assert data.containsElementWithAttrib("package", {"name":"humidifier-project.humidifier.src"})
    assert data.containsElementWithAttrib("method", {"name":"Humidifier::setPreferredHumidity(int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("method", {"name":"Atomizer_Set(int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("method", {"name":"FakeHumiditySensor::getHumidityLevel() const",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("method", {"name":"FakeHumiditySensor::gmock_getHumidityLevel() const",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})


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
        assert f.contains('"Shared State": {')
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
    ASXML = shared_report_build.files.asXml

    data = ASXML(REPORT.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml"))
    assert data.containsElementWithAttrib("testcase", {"classname":"sqlite3wrapper.DatabaseTest"})


def test_sqlite3wrapper_do_coverage(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read
    ASXML = shared_report_build.files.asXml

    assert READ(REPORT.COVERAGE("sqlite3wrapper", "index.html")).contains(LCOV_HTML_TITLE)

    data = ASXML(REPORT.COVERAGE("sqlite3wrapper", "coverage.xml"))
    assert data.containsElementWithAttrib("package", {"name":"sqlite3wrapper.src"})
    assert data.containsElementWithAttrib("method", {"name":"SQLite3Wrapper::Column::getName() const",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("method", {"name":"SQLite3Wrapper::Statement::check(int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})
    assert data.containsElementWithAttrib("method", {"name":"SQLite3Wrapper::Database::check(int)",
        "signature":"", "line-rate":"1.0", "branch-rate":"1.0"})


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
        assert f.contains('"Shared State": {')
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
