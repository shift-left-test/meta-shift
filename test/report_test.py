#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 Sung Gon Kim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import pytest


NORMAL_GT_PLUS_TEST_FAILED_LOG = 'testsuite name="PlusTest" tests="2" failures="1" disabled="0" errors="0"'
NORMAL_GT_MINUS_TEST_FAILED_LOG = 'testsuite name="MinusTest" tests="2" failures="1" disabled="0" errors="0"'
CMAKE_GT_PLUS_TEST_FAILED_LOG = 'testsuite name="PlusTest" tests="1" failures="1" disabled="0" errors="0"'
CMAKE_GT_MINUS_TEST_FAILED_LOG = 'testsuite name="MinusTest" tests="1" failures="1" disabled="0" errors="0"'
QT_PLUS_TEST_FAILED_LOG = 'testsuite errors="0" failures="1" tests="4" name="qmake5-project.PlusTest"'
QT_MINUS_TEST_FAILED_LOG = 'testsuite errors="0" failures="1" tests="4" name="qmake5-project.MinusTest"'
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'


class TEST:
    PF = {
        "cmake-project": "cmake-project-1.0.0-r0",
        "qmake5-project": "qmake5-project-1.0.0-r0",
        "autotools-project": "autotools-project-1.0.0-r0",
        "humidifier-project": "humidifier-project-1.0.0-r0",
        "sqlite3wrapper": "sqlite3wrapper-0.1.0-r0",
        "stringutils": "stringutils-0.0.1-r0",
    }

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
    def CHECKRECIPE(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checkrecipe", path)


def test_core_image_minimal_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(TEST.RESULT("cmake-project", "OperatorTest.xml"))
    assert EXISTS(TEST.COVERAGE("cmake-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("cmake-project", "coverage.xml"))

    assert EXISTS(TEST.RESULT("qmake5-project", "test-qt5-gtest.xml"))
    assert EXISTS(TEST.RESULT("qmake5-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(TEST.RESULT("qmake5-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(TEST.COVERAGE("qmake5-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("qmake5-project", "coverage.xml"))

    assert EXISTS(TEST.RESULT("autotools-project", "operatorTest.xml"))
    assert EXISTS(TEST.COVERAGE("autotools-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("autotools-project", "coverage.xml"))

    assert EXISTS(TEST.RESULT("humidifier-project", "unittest.xml"))
    assert EXISTS(TEST.COVERAGE("humidifier-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("humidifier-project", "coverage.xml"))

    assert EXISTS(TEST.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml"))
    assert EXISTS(TEST.COVERAGE("sqlite3wrapper", "index.html"))
    assert EXISTS(TEST.COVERAGE("sqlite3wrapper", "coverage.xml"))

    assert EXISTS(TEST.RESULT("stringutils", "unittest.bin.xml"))
    assert EXISTS(TEST.COVERAGE("stringutils", "index.html"))
    assert EXISTS(TEST.COVERAGE("stringutils", "coverage.xml"))

    assert EXISTS(TEST.CHECK("cmake-project", "sage_report.json"))

    assert EXISTS(TEST.CHECK("qmake5-project", "sage_report.json"))

    assert EXISTS(TEST.CHECK("autotools-project", "sage_report.json"))

    assert EXISTS(TEST.CHECK("humidifier-project", "sage_report.json"))

    assert EXISTS(TEST.CHECK("sqlite3wrapper", "sage_report.json"))

    assert EXISTS(TEST.CHECK("stringutils", "sage_report.json"))

    assert EXISTS(TEST.CHECKRECIPE("cmake-project", "recipe_violations.json"))

    assert EXISTS(TEST.CHECKRECIPE("qmake5-project", "recipe_violations.json"))

    assert EXISTS(TEST.CHECKRECIPE("autotools-project", "recipe_violations.json"))

    assert EXISTS(TEST.CHECKRECIPE("humidifier-project", "recipe_violations.json"))

    assert EXISTS(TEST.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json"))

    assert EXISTS(TEST.CHECKRECIPE("stringutils", "recipe_violations.json"))


def test_cmake_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake cmake-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    with READ(TEST.RESULT("cmake-project", "OperatorTest_1.xml")) as f:
        assert f.contains('classname="cmake-project.PlusTest"')
        assert f.contains(CMAKE_GT_PLUS_TEST_FAILED_LOG)

    with READ(TEST.RESULT("cmake-project", "OperatorTest_3.xml")) as f:
        assert f.contains('classname="cmake-project.MinusTest"')
        assert f.contains(CMAKE_GT_MINUS_TEST_FAILED_LOG)

    assert READ(TEST.COVERAGE("cmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(TEST.COVERAGE("cmake-project", "coverage.xml")) as f:
        assert f.contains('name="cmake-project.plus.src"')
        assert f.contains('<method name="arithmetic::plus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('name="cmake-project.minus.src"')
        assert f.contains('<method name="arithmetic::minus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')


def test_cmake_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(TEST.CHECK("cmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')


def test_cmake_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(TEST.CHECKRECIPE("cmake-project", "recipe_violations.json")) as f:
        assert f.contains('cmake-project_1.0.0.bb')
        assert f.contains('cmake-project_1.0.0.bbappend')


def test_cmake_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake cmake-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(TEST.RESULT("cmake-project", "OperatorTest.xml"))
    assert EXISTS(TEST.COVERAGE("cmake-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("cmake-project", "coverage.xml"))

    assert EXISTS(TEST.CHECK("cmake-project", "sage_report.json"))

    assert EXISTS(TEST.CHECKRECIPE("cmake-project", "recipe_violations.json"))


def test_qmake5_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake qmake5-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    with READ(TEST.RESULT("qmake5-project", "test-qt5-gtest.xml")) as f:
        assert f.contains('classname="qmake5-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="qmake5-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    with READ(TEST.RESULT("qmake5-project", "tests/plus_test/test_result.xml")) as f:
        assert f.contains('name="qmake5-project.PlusTest"')
        assert f.contains(QT_PLUS_TEST_FAILED_LOG)

    with READ(TEST.RESULT("qmake5-project", "tests/minus_test/test_result.xml")) as f:
        assert f.contains('name="qmake5-project.MinusTest"')
        assert f.contains(QT_MINUS_TEST_FAILED_LOG)

    assert READ(TEST.COVERAGE("qmake5-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(TEST.COVERAGE("qmake5-project", "coverage.xml")) as f:
        assert f.contains('name="qmake5-project.plus.src"')
        assert f.contains('<method name="arithmetic::plus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('name="qmake5-project.minus.src"')
        assert f.contains('<method name="arithmetic::minus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')


def test_qmake5_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake qmake5-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(TEST.CHECK("qmake5-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')


def test_qmake5_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake qmake5-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(TEST.CHECKRECIPE("qmake5-project", "recipe_violations.json")) as f:
        assert f.contains('qmake5-project_1.0.0.bb')
        assert f.contains('qmake5-project_1.0.0.bbappend')

def test_qmake5_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake qmake5-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(TEST.RESULT("qmake5-project", "test-qt5-gtest.xml"))
    assert EXISTS(TEST.RESULT("qmake5-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(TEST.RESULT("qmake5-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(TEST.COVERAGE("qmake5-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("qmake5-project", "coverage.xml"))

    assert EXISTS(TEST.CHECK("qmake5-project", "sage_report.json"))

    assert EXISTS(TEST.CHECKRECIPE("qmake5-project", "recipe_violations.json"))


def test_autotools_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake autotools-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    with READ(TEST.RESULT("autotools-project", "operatorTest.xml")) as f:
        assert f.contains('classname="autotools-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="autotools-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    assert READ(TEST.COVERAGE("autotools-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(TEST.COVERAGE("autotools-project", "coverage.xml")) as f:
        assert f.contains('name="autotools-project.plus.src"')
        assert f.contains('<method name="arithmetic::plus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('name="autotools-project.minus.src"')
        assert f.contains('<method name="arithmetic::minus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')


def test_autotools_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake autotools-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(TEST.CHECK("autotools-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')


def test_autotools_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake autotools-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(TEST.CHECKRECIPE("autotools-project", "recipe_violations.json")) as f:
        assert f.contains('autotools-project_1.0.0.bb')
        assert f.contains('autotools-project_1.0.0.bbappend')


def test_autotools_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake autotools-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(TEST.RESULT("autotools-project", "operatorTest.xml"))
    assert EXISTS(TEST.COVERAGE("autotools-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("autotools-project", "coverage.xml"))

    assert EXISTS(TEST.CHECK("autotools-project", "sage_report.json"))

    assert EXISTS(TEST.CHECKRECIPE("autotools-project", "recipe_violations.json"))


def test_humidifier_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake humidifier-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    assert READ(TEST.RESULT("humidifier-project", "unittest.xml")).contains('classname="humidifier-project.HumidifierTest"')

    assert READ(TEST.COVERAGE("humidifier-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(TEST.COVERAGE("humidifier-project", "coverage.xml")) as f:
        assert f.contains('name="humidifier-project.humidifier.src"')
        assert f.contains('<method name="Humidifier::setPreferredHumidity(int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('<method name="Atomizer_Set(int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('<method name="FakeHumiditySensor::getHumidityLevel() const" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('<method name="FakeHumiditySensor::gmock_getHumidityLevel() const" signature="" line-rate="1.0" branch-rate="1.0">')


def test_humidifier_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake humidifier-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(TEST.CHECK("humidifier-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')


def test_humidifier_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake humidifier-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(TEST.CHECKRECIPE("humidifier-project", "recipe_violations.json")) as f:
        assert f.contains('humidifier-project_1.0.0.bb')
        assert f.contains('humidifier-project_1.0.0.bbappend')


def test_humidifier_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake humidifier-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(TEST.RESULT("humidifier-project", "unittest.xml"))
    assert EXISTS(TEST.COVERAGE("humidifier-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("humidifier-project", "coverage.xml"))

    assert EXISTS(TEST.CHECK("humidifier-project", "sage_report.json"))

    assert EXISTS(TEST.CHECKRECIPE("humidifier-project", "recipe_violations.json"))


def test_sqlite3logger_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake sqlite3logger -c coverageall").stderr.empty()

    READ = report_build.files.read

    assert READ(TEST.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml")).contains('classname="sqlite3wrapper.DatabaseTest"')
    assert READ(TEST.COVERAGE("sqlite3wrapper", "index.html")).contains(LCOV_HTML_TITLE)
    with READ(TEST.COVERAGE("sqlite3wrapper", "coverage.xml")) as f:
        assert f.contains('name="sqlite3wrapper.src"')
        assert f.contains('<method name="SQLite3Wrapper::Column::getName() const" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('<method name="SQLite3Wrapper::Statement::check(int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('<method name="SQLite3Wrapper::Database::check(int)" signature="" line-rate="1.0" branch-rate="1.0">')

    assert READ(TEST.RESULT("stringutils", "unittest.bin.xml")).contains('classname="stringutils.StringTest"')
    assert READ(TEST.COVERAGE("stringutils", "index.html")).contains(LCOV_HTML_TITLE)
    with READ(TEST.COVERAGE("stringutils", "coverage.xml")) as f:
        assert f.contains('name="stringutils.include.util"')
        assert f.contains('<method name="bool util::string::contains&lt;char&gt;(char const*, char const*)" signature="" line-rate="1.0" branch-rate="1.0">')


def test_sqlite3logger_do_checkcodeall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake sqlite3logger -c checkcodeall").stderr.empty()

    READ = report_build.files.read

    with READ(TEST.CHECK("stringutils", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    with READ(TEST.CHECK("sqlite3wrapper", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    
def test_sqlite3logger_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake sqlite3logger -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(TEST.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json")) as f:
        assert f.contains('sqlite3wrapper_0.1.0.bb')
        assert f.contains('sqlite3wrapper_0.1.0.bbappend')

    with READ(TEST.CHECKRECIPE("stringutils", "recipe_violations.json")) as f:
        assert f.contains('stringutils_0.0.1.bb')
        assert f.contains('stringutils_0.0.1.bbappend')


def test_sqlite3logger_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake sqlite3logger -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(TEST.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml"))
    assert EXISTS(TEST.COVERAGE("sqlite3wrapper", "index.html"))
    assert EXISTS(TEST.COVERAGE("sqlite3wrapper", "coverage.xml"))

    assert EXISTS(TEST.RESULT("stringutils", "unittest.bin.xml"))
    assert EXISTS(TEST.COVERAGE("stringutils", "index.html"))
    assert EXISTS(TEST.COVERAGE("stringutils", "coverage.xml"))

    assert EXISTS(TEST.CHECK("sqlite3wrapper", "sage_report.json"))

    assert EXISTS(TEST.CHECK("stringutils", "sage_report.json"))

    assert EXISTS(TEST.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json"))

    assert EXISTS(TEST.CHECKRECIPE("stringutils", "recipe_violations.json"))
