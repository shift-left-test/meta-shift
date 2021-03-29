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
CPPCHECK_NO_ERRORS_FOUND = '<cppcheck version="2.0"/>\n    <errors>\n    </errors>'
LCOV_HTML_TITLE = '<tr><td class="title">LCOV - code coverage report</td></tr>'
SENTINEL_HTML_TITLE = '<h1>Sentinel Mutation Coverage Report</h1>'


class TEST:
    PF = {
        "cmake-project": "cmake-project-1.0.0-r0",
        "qmake5-project": "qmake5-project-1.0.0-r0",
        "autotools-project": "autotools-project-1.0.0-r0",
    }

    @classmethod
    def CHECK(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checkcode", path)

    @classmethod
    def CHECKTEST(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checktest", path)


def test_core_image_minimal_do_reportall(report_clang_build):
    report_clang_build.files.remove("report")
    report_clang_build.shell.execute("bitbake core-image-minimal -c reportall")

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

    assert EXISTS(TEST.CHECKTEST("cmake-project", "mutations.xml"))
    assert EXISTS(TEST.CHECKTEST("cmake-project", "index.html"))
    assert EXISTS(TEST.CHECKTEST("cmake-project", "style.css"))

    assert EXISTS(TEST.CHECKTEST("qmake5-project", "mutations.xml"))
    assert EXISTS(TEST.CHECKTEST("qmake5-project", "index.html"))
    assert EXISTS(TEST.CHECKTEST("qmake5-project", "style.css"))

    assert EXISTS(TEST.CHECKTEST("autotools-project", "mutations.xml"))
    assert EXISTS(TEST.CHECKTEST("autotools-project", "index.html"))
    assert EXISTS(TEST.CHECKTEST("autotools-project", "style.css"))


def test_cmake_project_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake cmake-project -c checkcodeall").stderr.empty()
    READ = report_clang_build.files.read
    # assert READ(TEST.CHECK("cmake-project", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert READ(TEST.CHECK("cmake-project", "cpplint_report.txt")).empty()
    assert READ(TEST.CHECK("cmake-project", "clang-tidy-report.txt")).empty()


def test_cmake_project_do_checktestall(report_clang_build):
    report_clang_build.files.remove("report")
    report_clang_build.shell.execute("bitbake cmake-project -c checktestall")
    READ = report_clang_build.files.read
    with READ(TEST.CHECKTEST("cmake-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(TEST.CHECKTEST("cmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


def test_cmake_project_do_reportall(report_clang_build):
    report_clang_build.files.remove("report")
    report_clang_build.shell.execute("bitbake cmake-project -c reportall")

    EXISTS = report_clang_build.files.exists

    assert EXISTS(TEST.CHECK("cmake-project", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("cmake-project", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("cmake-project", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECKTEST("cmake-project", "mutations.xml"))
    assert EXISTS(TEST.CHECKTEST("cmake-project", "index.html"))
    assert EXISTS(TEST.CHECKTEST("cmake-project", "style.css"))


def test_qmake5_project_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake qmake5-project -c checkcodeall").stderr.empty()
    # NOTE: auto-generated files violate the static analysis rules
    READ = report_clang_build.files.read
    # assert not READ(TEST.CHECK("qmake5-project", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert not READ(TEST.CHECK("qmake5-project", "cpplint_report.txt")).empty()
    # assert not READ(TEST.CHECK("qmake5-project", "clang-tidy-report.txt")).empty()


def test_qmake5_project_do_checktestall(report_clang_build):
    report_clang_build.files.remove("report")
    report_clang_build.shell.execute("bitbake qmake5-project -c checktestall")
    READ = report_clang_build.files.read
    with READ(TEST.CHECKTEST("qmake5-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(TEST.CHECKTEST("qmake5-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


def test_qmake5_project_do_reportall(report_clang_build):
    report_clang_build.files.remove("report")

    report_clang_build.shell.execute("bitbake qmake5-project -c reportall")

    EXISTS = report_clang_build.files.exists

    assert EXISTS(TEST.CHECK("qmake5-project", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("qmake5-project", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("qmake5-project", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECKTEST("qmake5-project", "mutations.xml"))
    assert EXISTS(TEST.CHECKTEST("qmake5-project", "index.html"))
    assert EXISTS(TEST.CHECKTEST("qmake5-project", "style.css"))


def test_autotools_project_do_checkcodeall(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake autotools-project -c checkcodeall").stderr.empty()
    READ = report_clang_build.files.read
    # assert READ(TEST.CHECK("autotools-project", "cppcheck_report.xml")).contains(CPPCHECK_NO_ERRORS_FOUND)
    assert READ(TEST.CHECK("autotools-project", "cpplint_report.txt")).empty()
    assert READ(TEST.CHECK("autotools-project", "clang-tidy-report.txt")).empty()


def test_autotools_project_do_checktestall(report_clang_build):
    report_clang_build.files.remove("report")
    report_clang_build.shell.execute("bitbake autotools-project -c checktestall")
    READ = report_clang_build.files.read
    with READ(TEST.CHECKTEST("autotools-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(TEST.CHECKTEST("autotools-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


def test_autotools_project_do_reportall(report_clang_build):
    report_clang_build.files.remove("report")
    report_clang_build.shell.execute("bitbake autotools-project -c reportall")

    EXISTS = report_clang_build.files.exists

    assert EXISTS(TEST.CHECK("autotools-project", "cppcheck_report.xml"))
    assert EXISTS(TEST.CHECK("autotools-project", "cpplint_report.txt"))
    assert EXISTS(TEST.CHECK("autotools-project", "clang-tidy-report.txt"))

    assert EXISTS(TEST.CHECKTEST("autotools-project", "mutations.xml"))
    assert EXISTS(TEST.CHECKTEST("autotools-project", "index.html"))
    assert EXISTS(TEST.CHECKTEST("autotools-project", "style.css"))
