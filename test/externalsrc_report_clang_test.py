#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 Sangmo Kang

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
from contextlib import contextmanager


CMAKE_GT_PLUS_TEST_FAILED_LOG = 'testsuite name="PlusTest" tests="1" failures="1" disabled="0" errors="0"'
CMAKE_GT_MINUS_TEST_FAILED_LOG = 'testsuite name="MinusTest" tests="1" failures="1" disabled="0" errors="0"'
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
SENTINEL_HTML_TITLE = '<h1>Sentinel Mutation Coverage Report</h1>'


class TEST:
    PF = {
        "cmake-project": "cmake-project-1.0.0-r0",
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
    def CHECKTEST(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checktest", path)

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


def test_cmake_project_do_report(report_clang_build):
    report_clang_build.files.remove("report")

    with externalsrc_execute(report_clang_build, "cmake-project", "report") as o:
        assert o.stderr.empty()

    EXISTS = report_clang_build.files.exists

    assert EXISTS(TEST.RESULT("cmake-project", "OperatorTest.xml"))
    assert EXISTS(TEST.COVERAGE("cmake-project", "index.html"))
    assert EXISTS(TEST.COVERAGE("cmake-project", "coverage.xml"))

    assert EXISTS(TEST.CHECK("cmake-project", "sage_report.json"))

    assert EXISTS(TEST.CHECKTEST("cmake-project", "mutations.xml"))
    assert EXISTS(TEST.CHECKTEST("cmake-project", "index.html"))
    assert EXISTS(TEST.CHECKTEST("cmake-project", "style.css"))

    assert EXISTS(TEST.CHECKRECIPE("cmake-project", "recipe_violations.json"))


def test_cmake_project_do_coverage(report_clang_build):
    report_clang_build.files.remove("report")

    with externalsrc_execute(report_clang_build, "cmake-project", "coverage") as o:
        assert o.stderr.empty()

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
        assert f.contains('<method name="arithmetic::plus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')
        assert f.contains('name="cmake-project.minus.src"')
        assert f.contains('<method name="arithmetic::minus(int, int)" signature="" line-rate="1.0" branch-rate="1.0">')


def test_cmake_project_do_checkcode(report_clang_build):
    report_clang_build.files.remove("report")
    with externalsrc_execute(report_clang_build, "cmake-project", "checkcode") as o:
        assert o.stderr.empty()
    READ = report_clang_build.files.read
    with READ(TEST.CHECK("cmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')


def test_cmake_project_do_checktest(report_clang_build):
    report_clang_build.files.remove("report")
    with externalsrc_execute(report_clang_build, "cmake-project", "checktest") as o:
        assert o.stderr.empty()

    READ = report_clang_build.files.read
    with READ(TEST.CHECKTEST("cmake-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(TEST.CHECKTEST("cmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


def test_cmake_project_do_checkrecipe(report_clang_build):
    report_clang_build.files.remove("report")
    with externalsrc_execute(report_clang_build, "cmake-project", "checkrecipe") as o:
        assert o.stderr.empty()
    READ = report_clang_build.files.read

    with READ(TEST.CHECKRECIPE("cmake-project", "recipe_violations.json")) as f:
        assert f.contains('cmake-project_1.0.0.bb')
        assert f.contains('cmake-project_1.0.0.bbappend')
