#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 LG Electronics, Inc.

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
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
METADATA_S = '"S": "'


class REPORT:
    PF = {
        "qmake6-project": "qmake6-project-1.0.0-r0",
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


def test_core_image_minimal_do_reportall(report_qt6_build):
    report_qt6_build.files.remove("report")

    assert report_qt6_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()

    EXISTS = report_qt6_build.files.exists

    assert EXISTS(REPORT.ROOT("qmake6-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("qmake6-project", "test-qt5-gtest.xml"))
    assert EXISTS(REPORT.RESULT("qmake6-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(REPORT.RESULT("qmake6-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(REPORT.COVERAGE("qmake6-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("qmake6-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("qmake6-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("qmake6-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake6-project", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake6-project", "files.json"))


def test_qmake6_project_do_coverageall(report_qt6_build):
    report_qt6_build.files.remove("report")

    assert report_qt6_build.shell.execute("bitbake qmake6-project -c coverageall").stderr.empty()

    READ = report_qt6_build.files.read

    with READ(REPORT.RESULT("qmake6-project", "test-qt5-gtest.xml")) as f:
        assert f.contains('classname="qmake6-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="qmake6-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("qmake6-project", "tests/plus_test/test_result.xml")) as f:
        assert f.contains('name="qmake6-project.PlusTest"')

    with READ(REPORT.RESULT("qmake6-project", "tests/minus_test/test_result.xml")) as f:
        assert f.contains('name="qmake6-project.MinusTest"')

    assert READ(REPORT.COVERAGE("qmake6-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("qmake6-project", "coverage.xml")) as f:
        assert f.contains('name="qmake6-project.plus.src"')
        assert f.contains('<method name="arithmetic::plus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('name="qmake6-project.minus.src"')
        assert f.contains('<method name="arithmetic::minus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')

    assert READ(REPORT.ROOT("qmake6-project", "metadata.json")).contains(METADATA_S)


def test_qmake6_project_do_checkcodeall(report_qt6_build):
    report_qt6_build.files.remove("report")
    assert report_qt6_build.shell.execute("bitbake qmake6-project -c checkcodeall").stderr.empty()
    READ = report_qt6_build.files.read
    with READ(REPORT.CHECK("qmake6-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("qmake6-project", "metadata.json")).contains(METADATA_S)


def test_qmake6_project_do_checkcacheall(report_qt6_build):
    report_qt6_build.files.remove("report")
    assert report_qt6_build.shell.execute("bitbake qmake6-project -c checkcacheall").stderr.empty()
    READ = report_qt6_build.files.read
    with READ(REPORT.CHECKCACHE("qmake6-project", "caches.json")) as f:
        assert f.contains('"Shared State": {{')
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("qmake6-project", "metadata.json")).contains(METADATA_S)


def test_qmake6_project_do_checkrecipeall(report_qt6_build):
    report_qt6_build.files.remove("report")
    assert report_qt6_build.shell.execute("bitbake qmake6-project -c checkrecipeall").stderr.empty()
    READ = report_qt6_build.files.read

    with READ(REPORT.CHECKRECIPE("qmake6-project", "recipe_violations.json")) as f:
        assert f.contains('qmake6-project_1.0.0.bb')
        assert f.contains('qmake6-project_1.0.0.bbappend')

    with READ(REPORT.CHECKRECIPE("qmake6-project", "files.json")) as f:
        assert f.contains('qmake6-project_1.0.0.bb')
        assert f.contains('qmake6-project_1.0.0.bbappend')

    assert READ(REPORT.ROOT("qmake6-project", "metadata.json")).contains(METADATA_S)

def test_qmake6_project_do_reportall(report_qt6_build):
    report_qt6_build.files.remove("report")

    assert report_qt6_build.shell.execute("bitbake qmake6-project -c reportall").stderr.empty()

    EXISTS = report_qt6_build.files.exists

    assert EXISTS(REPORT.ROOT("qmake6-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("qmake6-project", "test-qt5-gtest.xml"))
    assert EXISTS(REPORT.RESULT("qmake6-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(REPORT.RESULT("qmake6-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(REPORT.COVERAGE("qmake6-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("qmake6-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("qmake6-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("qmake6-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake6-project", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake6-project", "files.json"))

