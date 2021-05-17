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
METADATA_S = '"S": "'


class REPORT:
    PF = {
        "cmake-project": "cmake-project-1.0.0-r0",
        "qmake5-project": "qmake5-project-1.0.0-r0",
        "autotools-project": "autotools-project-1.0.0-r0",
        "humidifier-project": "humidifier-project-1.0.0-r0",
        "sqlite3wrapper": "sqlite3wrapper-0.1.0-r0",
        "stringutils": "stringutils-0.0.1-r0",
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


def test_core_image_minimal_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(REPORT.ROOT("cmake-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("cmake-project", "OperatorTest.xml"))
    assert EXISTS(REPORT.COVERAGE("cmake-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("cmake-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("cmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("cmake-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("cmake-project", "recipe_violations.json"))

    assert EXISTS(REPORT.ROOT("qmake5-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("qmake5-project", "test-qt5-gtest.xml"))
    assert EXISTS(REPORT.RESULT("qmake5-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(REPORT.RESULT("qmake5-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(REPORT.COVERAGE("qmake5-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("qmake5-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("qmake5-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("qmake5-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake5-project", "recipe_violations.json"))

    assert EXISTS(REPORT.ROOT("autotools-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("autotools-project", "operatorTest.xml"))
    assert EXISTS(REPORT.COVERAGE("autotools-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("autotools-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("autotools-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("autotools-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("autotools-project", "recipe_violations.json"))

    assert EXISTS(REPORT.ROOT("humidifier-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("humidifier-project", "unittest.xml"))
    assert EXISTS(REPORT.COVERAGE("humidifier-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("humidifier-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("humidifier-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("humidifier-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("humidifier-project", "recipe_violations.json"))

    assert EXISTS(REPORT.ROOT("sqlite3wrapper", "metadata.json"))
    assert EXISTS(REPORT.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml"))
    assert EXISTS(REPORT.COVERAGE("sqlite3wrapper", "index.html"))
    assert EXISTS(REPORT.COVERAGE("sqlite3wrapper", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("sqlite3wrapper", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("sqlite3wrapper", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json"))

    assert EXISTS(REPORT.ROOT("stringutils", "metadata.json"))
    assert EXISTS(REPORT.RESULT("stringutils", "unittest.bin.xml"))
    assert EXISTS(REPORT.COVERAGE("stringutils", "index.html"))
    assert EXISTS(REPORT.COVERAGE("stringutils", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("stringutils", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("stringutils", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("stringutils", "recipe_violations.json"))


def test_cmake_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake cmake-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    with READ(REPORT.RESULT("cmake-project", "OperatorTest_1.xml")) as f:
        assert f.contains('classname="cmake-project.PlusTest"')
        assert f.contains(CMAKE_GT_PLUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("cmake-project", "OperatorTest_3.xml")) as f:
        assert f.contains('classname="cmake-project.MinusTest"')
        assert f.contains(CMAKE_GT_MINUS_TEST_FAILED_LOG)

    assert READ(REPORT.COVERAGE("cmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("cmake-project", "coverage.xml")) as f:
        assert f.contains('name="cmake-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="cmake-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')

    assert READ(REPORT.ROOT("cmake-project", "metadata.json")).contains(METADATA_S)


def test_cmake_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECK("cmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("cmake-project", "metadata.json")).contains(METADATA_S)


def test_cmake_project_do_checkcacheall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c checkcacheall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECKCACHE("cmake-project", "caches.json")) as f:
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("cmake-project", "metadata.json")).contains(METADATA_S)


def test_cmake_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(REPORT.CHECKRECIPE("cmake-project", "recipe_violations.json")) as f:
        assert f.contains('cmake-project_1.0.0.bb')
        assert f.contains('cmake-project_1.0.0.bbappend')

    assert READ(REPORT.ROOT("cmake-project", "metadata.json")).contains(METADATA_S)


def test_cmake_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake cmake-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(REPORT.ROOT("cmake-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("cmake-project", "OperatorTest.xml"))
    assert EXISTS(REPORT.COVERAGE("cmake-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("cmake-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("cmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("cmake-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("cmake-project", "recipe_violations.json"))


def test_qmake5_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake qmake5-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    with READ(REPORT.RESULT("qmake5-project", "test-qt5-gtest.xml")) as f:
        assert f.contains('classname="qmake5-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="qmake5-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("qmake5-project", "tests/plus_test/test_result.xml")) as f:
        assert f.contains('name="qmake5-project.PlusTest"')
        assert f.contains(QT_PLUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("qmake5-project", "tests/minus_test/test_result.xml")) as f:
        assert f.contains('name="qmake5-project.MinusTest"')
        assert f.contains(QT_MINUS_TEST_FAILED_LOG)

    assert READ(REPORT.COVERAGE("qmake5-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("qmake5-project", "coverage.xml")) as f:
        assert f.contains('name="qmake5-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="qmake5-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')

    assert READ(REPORT.ROOT("qmake5-project", "metadata.json")).contains(METADATA_S)


def test_qmake5_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake qmake5-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECK("qmake5-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("qmake5-project", "metadata.json")).contains(METADATA_S)


def test_qmake5_project_do_checkcacheall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake qmake5-project -c checkcacheall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECKCACHE("qmake5-project", "caches.json")) as f:
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("qmake5-project", "metadata.json")).contains(METADATA_S)


def test_qmake5_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake qmake5-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(REPORT.CHECKRECIPE("qmake5-project", "recipe_violations.json")) as f:
        assert f.contains('qmake5-project_1.0.0.bb')
        assert f.contains('qmake5-project_1.0.0.bbappend')

    assert READ(REPORT.ROOT("qmake5-project", "metadata.json")).contains(METADATA_S)

def test_qmake5_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake qmake5-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(REPORT.ROOT("qmake5-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("qmake5-project", "test-qt5-gtest.xml"))
    assert EXISTS(REPORT.RESULT("qmake5-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(REPORT.RESULT("qmake5-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(REPORT.COVERAGE("qmake5-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("qmake5-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("qmake5-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("qmake5-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake5-project", "recipe_violations.json"))


def test_autotools_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake autotools-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    with READ(REPORT.RESULT("autotools-project", "operatorTest.xml")) as f:
        assert f.contains('classname="autotools-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="autotools-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    assert READ(REPORT.COVERAGE("autotools-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("autotools-project", "coverage.xml")) as f:
        assert f.contains('name="autotools-project.plus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">')
        assert f.contains('name="autotools-project.minus.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')

    assert READ(REPORT.ROOT("autotools-project", "metadata.json")).contains(METADATA_S)


def test_autotools_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake autotools-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECK("autotools-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("autotools-project", "metadata.json")).contains(METADATA_S)


def test_autotools_project_do_checkcacheall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake autotools-project -c checkcacheall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECKCACHE("autotools-project", "caches.json")) as f:
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("autotools-project", "metadata.json")).contains(METADATA_S)


def test_autotools_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake autotools-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(REPORT.CHECKRECIPE("autotools-project", "recipe_violations.json")) as f:
        assert f.contains('autotools-project_1.0.0.bb')
        assert f.contains('autotools-project_1.0.0.bbappend')

    assert READ(REPORT.ROOT("autotools-project", "metadata.json")).contains(METADATA_S)


def test_autotools_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake autotools-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(REPORT.ROOT("autotools-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("autotools-project", "operatorTest.xml"))
    assert EXISTS(REPORT.COVERAGE("autotools-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("autotools-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("autotools-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("autotools-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("autotools-project", "recipe_violations.json"))


def test_humidifier_project_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake humidifier-project -c coverageall").stderr.empty()

    READ = report_build.files.read

    assert READ(REPORT.RESULT("humidifier-project", "unittest.xml")).contains('classname="humidifier-project.HumidifierTest"')

    assert READ(REPORT.COVERAGE("humidifier-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("humidifier-project", "coverage.xml")) as f:
        assert f.contains('name="humidifier-project.humidifier.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="Humidifier::setPreferredHumidity(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="Atomizer_Set(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="FakeHumiditySensor::getHumidityLevel() const" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="FakeHumiditySensor::gmock_getHumidityLevel() const" signature="">')

    assert READ(REPORT.ROOT("humidifier-project", "metadata.json")).contains(METADATA_S)


def test_humidifier_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake humidifier-project -c checkcodeall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECK("humidifier-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("humidifier-project", "metadata.json")).contains(METADATA_S)


def test_humidifier_project_do_checkcacheall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake humidifier-project -c checkcacheall").stderr.empty()
    READ = report_build.files.read
    with READ(REPORT.CHECKCACHE("humidifier-project", "caches.json")) as f:
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("humidifier-project", "metadata.json")).contains(METADATA_S)


def test_humidifier_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake humidifier-project -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(REPORT.CHECKRECIPE("humidifier-project", "recipe_violations.json")) as f:
        assert f.contains('humidifier-project_1.0.0.bb')
        assert f.contains('humidifier-project_1.0.0.bbappend')

    assert READ(REPORT.ROOT("humidifier-project", "metadata.json")).contains(METADATA_S)


def test_humidifier_project_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake humidifier-project -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(REPORT.ROOT("humidifier-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("humidifier-project", "unittest.xml"))
    assert EXISTS(REPORT.COVERAGE("humidifier-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("humidifier-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("humidifier-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("humidifier-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("humidifier-project", "recipe_violations.json"))


def test_sqlite3logger_do_coverageall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake sqlite3logger -c coverageall").stderr.empty()

    READ = report_build.files.read

    assert READ(REPORT.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml")).contains('classname="sqlite3wrapper.DatabaseTest"')
    assert READ(REPORT.COVERAGE("sqlite3wrapper", "index.html")).contains(LCOV_HTML_TITLE)
    with READ(REPORT.COVERAGE("sqlite3wrapper", "coverage.xml")) as f:
        assert f.contains('name="sqlite3wrapper.src"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Column::getName() const" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Statement::check(int)" signature="">')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Database::check(int)" signature="">')

    assert READ(REPORT.ROOT("sqlite3wrapper", "metadata.json")).contains(METADATA_S)

    assert READ(REPORT.RESULT("stringutils", "unittest.bin.xml")).contains('classname="stringutils.StringTest"')
    assert READ(REPORT.COVERAGE("stringutils", "index.html")).contains(LCOV_HTML_TITLE)
    with READ(REPORT.COVERAGE("stringutils", "coverage.xml")) as f:
        assert f.contains('name="stringutils.include.util"')
        assert f.contains('<method branch-rate="1.0" line-rate="1.0" name="bool util::string::contains&lt;char&gt;(char const*, char const*)" signature="">')

    assert READ(REPORT.ROOT("stringutils", "metadata.json")).contains(METADATA_S)


def test_sqlite3logger_do_checkcodeall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake sqlite3logger -c checkcodeall").stderr.empty()

    READ = report_build.files.read

    with READ(REPORT.CHECK("stringutils", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("stringutils", "metadata.json")).contains(METADATA_S)

    with READ(REPORT.CHECK("sqlite3wrapper", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("sqlite3wrapper", "metadata.json")).contains(METADATA_S)

def test_sqlite3logger_do_checkcacheall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake sqlite3logger -c checkcacheall").stderr.empty()

    READ = report_build.files.read

    with READ(REPORT.CHECKCACHE("stringutils", "caches.json")) as f:
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("stringutils", "metadata.json")).contains(METADATA_S)

    with READ(REPORT.CHECKCACHE("sqlite3wrapper", "caches.json")) as f:
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("sqlite3wrapper", "metadata.json")).contains(METADATA_S)


def test_sqlite3logger_project_do_checkrecipeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake sqlite3logger -c checkrecipeall").stderr.empty()
    READ = report_build.files.read

    with READ(REPORT.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json")) as f:
        assert f.contains('sqlite3wrapper_0.1.0.bb')
        assert f.contains('sqlite3wrapper_0.1.0.bbappend')

    assert READ(REPORT.ROOT("stringutils", "metadata.json")).contains(METADATA_S)

    with READ(REPORT.CHECKRECIPE("stringutils", "recipe_violations.json")) as f:
        assert f.contains('stringutils_0.0.1.bb')
        assert f.contains('stringutils_0.0.1.bbappend')

    assert READ(REPORT.ROOT("sqlite3wrapper", "metadata.json")).contains(METADATA_S)


def test_sqlite3logger_do_reportall(report_build):
    report_build.files.remove("report")

    assert report_build.shell.execute("bitbake sqlite3logger -c reportall").stderr.empty()

    EXISTS = report_build.files.exists

    assert EXISTS(REPORT.ROOT("sqlite3wrapper", "metadata.json"))
    assert EXISTS(REPORT.RESULT("sqlite3wrapper", "SQLite3WrapperTest.exe.xml"))
    assert EXISTS(REPORT.COVERAGE("sqlite3wrapper", "index.html"))
    assert EXISTS(REPORT.COVERAGE("sqlite3wrapper", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("sqlite3wrapper", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("sqlite3wrapper", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("sqlite3wrapper", "recipe_violations.json"))

    assert EXISTS(REPORT.ROOT("stringutils", "metadata.json"))
    assert EXISTS(REPORT.RESULT("stringutils", "unittest.bin.xml"))
    assert EXISTS(REPORT.COVERAGE("stringutils", "index.html"))
    assert EXISTS(REPORT.COVERAGE("stringutils", "coverage.xml"))
    assert EXISTS(REPORT.CHECKCACHE("stringutils", "caches.json"))
    assert EXISTS(REPORT.CHECK("stringutils", "sage_report.json"))
    assert EXISTS(REPORT.CHECKRECIPE("stringutils", "recipe_violations.json"))
