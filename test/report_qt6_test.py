#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest


NORMAL_GT_PLUS_TEST_FAILED_LOG = 'testsuite name="PlusTest" tests="2" failures="1" disabled="0" skipped="0" errors="0"'
NORMAL_GT_MINUS_TEST_FAILED_LOG = 'testsuite name="MinusTest" tests="2" failures="1" disabled="0" skipped="0" errors="0"'
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
METADATA_S = '"S": "'


class REPORT:
    PF = {
        "qmake-project": "qmake-project-1.0.0-r0",
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


def test_qmake_project_do_report(report_qt6_build):
    report_qt6_build.files.remove("report")

    assert report_qt6_build.shell.execute("bitbake qmake-project -c report").stderr.empty()

    EXISTS = report_qt6_build.files.exists
    READ = report_qt6_build.files.read

    assert EXISTS(REPORT.ROOT("qmake-project", "metadata.json"))
    assert EXISTS(REPORT.RESULT("qmake-project", "test-qt-gtest.xml"))
    assert EXISTS(REPORT.RESULT("qmake-project", "tests/plus_test/test_result.xml"))
    assert EXISTS(REPORT.RESULT("qmake-project", "tests/minus_test/test_result.xml"))
    assert EXISTS(REPORT.COVERAGE("qmake-project", "index.html"))
    assert EXISTS(REPORT.COVERAGE("qmake-project", "coverage.xml"))
    assert EXISTS(REPORT.CHECK("qmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKCACHE("qmake-project", "caches.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake-project", "recipe_violations.json"))
    assert EXISTS(REPORT.CHECKRECIPE("qmake-project", "files.json"))

    # do_test
    with READ(REPORT.RESULT("qmake-project", "test-qt-gtest.xml")) as f:
        assert f.contains('classname="qmake-project.PlusTest"')
        assert f.contains(NORMAL_GT_PLUS_TEST_FAILED_LOG)
        assert f.contains('classname="qmake-project.MinusTest"')
        assert f.contains(NORMAL_GT_MINUS_TEST_FAILED_LOG)

    with READ(REPORT.RESULT("qmake-project", "tests/plus_test/test_result.xml")) as f:
        assert f.contains('name="qmake-project.PlusTest"')

    with READ(REPORT.RESULT("qmake-project", "tests/minus_test/test_result.xml")) as f:
        assert f.contains('name="qmake-project.MinusTest"')

    # do_coverage
    assert READ(REPORT.COVERAGE("qmake-project", "index.html")).contains(LCOV_HTML_TITLE)

    with READ(REPORT.COVERAGE("qmake-project", "coverage.xml")) as f:
        assert f.contains('name="qmake-project.plus.src"')
        assert f.contains('<method name="arithmetic::plus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('name="qmake-project.minus.src"')
        assert f.contains('<method name="arithmetic::minus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)

    # do_checkcode
    with READ(REPORT.CHECK("qmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)

    # do_checkcache
    with READ(REPORT.CHECKCACHE("qmake-project", "caches.json")) as f:
        assert f.contains('"Shared State": {{')
        assert f.contains('"Premirror": {{')
        assert f.contains('"Summary": {{')
        assert f.contains('"Found": [')
        assert f.contains('"Missed": [')

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)

    # do_checkrecipe
    with READ(REPORT.CHECKRECIPE("qmake-project", "recipe_violations.json")) as f:
        assert f.contains('"issues": []')

    with READ(REPORT.CHECKRECIPE("qmake-project", "files.json")) as f:
        assert f.contains('qmake-project_1.0.0.bb')
        assert f.contains('qmake-project_1.0.0.bbappend')

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)
