#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest
from contextlib import contextmanager


CMAKE_GT_PLUS_TEST_FAILED_LOG = 'testsuite name="PlusTest" tests="1" failures="1" disabled="0" errors="0"'
CMAKE_GT_MINUS_TEST_FAILED_LOG = 'testsuite name="MinusTest" tests="1" failures="1" disabled="0" errors="0"'
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
SAGE_HTML_TITLE = '<h1>Sage Report</h1>'
METADATA_S = '"S": "'


class REPORT:
    PF = {
        "cmake-project": "cmake-project-1.0.0-r0",
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


@contextmanager
def externalsrc_execute(build, recipe, task):
    try:
        build.shell.run("devtool modify %s" % recipe)
        assert build.files.exists(os.path.join("workspace", "sources", recipe))
        yield build.shell.execute("bitbake %s -c %s" % (recipe, task))
    finally:
        build.shell.run("devtool reset %s" % recipe)
        build.shell.run("bitbake-layers remove-layer workspace")
        build.files.remove("workspace")


@pytest.fixture(scope="module")
def shared_report_build(report_build):
    report_build.files.remove("report")
    with externalsrc_execute(report_build, "cmake-project", "report") as o:
        assert o.stderr.empty()
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
    assert EXISTS(REPORT.CHECKRECIPE("cmake-project", "recipe_violations.json"))

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
        assert f.contains('cmake-project_1.0.0.bbappend')
