#!/usr/bin/python

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
CPPCHECK_NO_ERRORS_FOUND = '<cppcheck version="2.0"/>\n    <errors>\n    </errors>'
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


def test_core_image_minimal_do_coverageall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake core-image-minimal -c coverageall").stderr.empty()

    EXISTS = report_clang_build.files.exists

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


def test_core_image_minimal_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake core-image-minimal -c checkcodeall").stderr.empty()

    EXISTS = report_clang_build.files.exists

    assert EXISTS(TEST.CHECK("cmake-project", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("cmake-project", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("cmake-project", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECK("qmake5-project", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("qmake5-project", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("qmake5-project", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECK("autotools-project", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("autotools-project", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("autotools-project", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECK("humidifier-project", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("humidifier-project", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("humidifier-project", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECK("sqlite3wrapper", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("sqlite3wrapper", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("sqlite3wrapper", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECK("stringutils", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("stringutils", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("stringutils", "clang-tidy-report.txt"))


def test_cmake_project_do_coverageall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake cmake-project -c coverageall").stderr.empty()

    READ = report_clang_build.files.read

    with READ(TEST.RESULT("cmake-project", "OperatorTest_1.xml")) as f:
        assert f.contains('classname="cmake-project.PlusTest"')
        assert f.contains(CMAKE_GT_PLUS_TEST_FAILED_LOG)

    with READ(TEST.RESULT("cmake-project", "OperatorTest_3.xml")) as f:
        assert f.contains('classname="cmake-project.MinusTest"')
        assert f.contains(CMAKE_GT_MINUS_TEST_FAILED_LOG)

    assert READ(TEST.COVERAGE("cmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(TEST.COVERAGE("cmake-project", "coverage.xml")) as f:
        assert f.contains('name="cmake-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="cmake-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_cmake_project_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake cmake-project -c checkcodeall").stderr.empty()
    READ = report_clang_build.files.read
    # assert READ(TEST.CHECK("cmake-project", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert READ(TEST.CHECK("cmake-project", "cpplint_report.txt")).empty()
    assert READ(TEST.CHECK("cmake-project", "clang-tidy-report.txt")).empty()


def test_qmake5_project_do_coverageall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake qmake5-project -c coverageall").stderr.empty()

    READ = report_clang_build.files.read

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
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="qmake5-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_qmake5_project_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake qmake5-project -c checkcodeall").stderr.empty()
    # NOTE: auto-generated files violate the static analysis rules
    READ = report_clang_build.files.read
    # assert not READ(TEST.CHECK("qmake5-project", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert not READ(TEST.CHECK("qmake5-project", "cpplint_report.txt")).empty()
    # assert not READ(TEST.CHECK("qmake5-project", "clang-tidy-report.txt")).empty()


def test_autotools_project_do_coverageall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake autotools-project -c coverageall").stderr.empty()

    READ = report_clang_build.files.read

    with READ(TEST.RESULT("autotools-project", "operatorTest.xml")) as f:
        assert f.contains('classname="autotools-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="autotools-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    assert READ(TEST.COVERAGE("autotools-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(TEST.COVERAGE("autotools-project", "coverage.xml")) as f:
        assert f.contains('name="autotools-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="autotools-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_autotools_project_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake autotools-project -c checkcodeall").stderr.empty()
    READ = report_clang_build.files.read
    # assert READ(TEST.CHECK("autotools-project", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert READ(TEST.CHECK("autotools-project", "cpplint_report.txt")).empty()
    assert READ(TEST.CHECK("autotools-project", "clang-tidy-report.txt")).empty()


def test_humidifier_project_do_coverageall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake humidifier-project -c coverageall").stderr.empty()

    READ = report_clang_build.files.read

    assert READ(TEST.RESULT("humidifier-project", "unittest.xml")).contains('classname="humidifier-project.HumidifierTest"')

    assert READ(TEST.COVERAGE("humidifier-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(TEST.COVERAGE("humidifier-project", "coverage.xml")) as f:
        assert f.contains('name="humidifier-project.humidifier.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="Humidifier::setPreferredHumidity(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="Atomizer_Set(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="FakeHumiditySensor::getHumidityLevel() const" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="FakeHumiditySensor::gmock_getHumidityLevel() const" signature="">')


def test_humidifier_project_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake humidifier-project -c checkcodeall").stderr.empty()
    READ = report_clang_build.files.read
    # assert READ(TEST.CHECK("humidifier-project", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert READ(TEST.CHECK("humidifier-project", "cpplint_report.txt")).empty()
    assert READ(TEST.CHECK("humidifier-project", "clang-tidy-report.txt")).empty()


def test_sqlite3logger_do_coverageall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake sqlite3logger -c coverageall").stderr.empty()

    READ = report_clang_build.files.read

    assert READ(TEST.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml")).contains('classname="sqlite3wrapper.DatabaseTest"')
    assert READ(TEST.COVERAGE("sqlite3wrapper", "index.html")).contains(LCOV_HTML_TITLE)
    with READ(TEST.COVERAGE("sqlite3wrapper", "coverage.xml")) as f:
        assert f.contains('name="sqlite3wrapper.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Column::getName() const" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Statement::check(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Database::check(int)" signature="">')

    assert READ(TEST.RESULT("stringutils", "unittest.bin.xml")).contains('classname="stringutils.StringTest"')
    assert READ(TEST.COVERAGE("stringutils", "index.html")).contains(LCOV_HTML_TITLE)
    with READ(TEST.COVERAGE("stringutils", "coverage.xml")) as f:
        assert f.contains('name="stringutils.include.util"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="bool util::string::contains&lt;char&gt;(char const*, char const*)" signature="">')


def test_sqlite3logger_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")

    assert report_clang_build.shell.execute("bitbake sqlite3logger -c checkcodeall").stderr.empty()

    READ = report_clang_build.files.read

    # assert READ(TEST.CHECK("sqlite3wrapper", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert READ(TEST.CHECK("sqlite3wrapper", "cpplint_report.txt")).empty()
    assert READ(TEST.CHECK("sqlite3wrapper", "clang-tidy-report.txt")).empty()

    # assert READ(TEST.CHECK("stringutils", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert READ(TEST.CHECK("stringutils", "cpplint_report.txt")).empty()
    assert READ(TEST.CHECK("stringutils", "clang-tidy-report.txt")).empty()
