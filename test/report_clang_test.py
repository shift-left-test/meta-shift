#-*- coding: utf-8 -*-
#!/usr/bin/python3

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
SENTINEL_HTML_TITLE = '<h1>Sentinel Mutation Coverage Report</h1>'
SAGE_HTML_TITLE = '<h1>Sage Report</h1>'
METADATA_S = '"S": "'


class REPORT:
    PF = {
        "cmake-project": "cmake-project-1.0.0-r0",
        "qmake-project": "qmake-project-1.0.0-r0",
        "autotools-project": "autotools-project-1.0.0-r0",
    }

    @classmethod
    def ROOT(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], path)

    @classmethod
    def CHECK(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checkcode", path)

    @classmethod
    def CHECKTEST(cls, recipe, path):
        return os.path.join("report", cls.PF[recipe], "checktest", path)


@pytest.fixture(scope="module")
def shared_report_build(report_clang_build):
    report_clang_build.files.remove("report")
    assert report_clang_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()
    return report_clang_build


def test_cmake_project(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("cmake-project", "metadata.json"))
    assert EXISTS(REPORT.CHECK("cmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("cmake-project", "index.html"))
    assert EXISTS(REPORT.CHECK("cmake-project", "style.css"))
    assert EXISTS(REPORT.CHECKTEST("cmake-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("cmake-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("cmake-project", "style.css"))

    assert READ(REPORT.ROOT("cmake-project", "metadata.json")).contains(METADATA_S)


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


def test_cmake_project_do_checktest(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKTEST("cmake-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(REPORT.CHECKTEST("cmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


def test_qmake_project(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("qmake-project", "metadata.json"))
    assert EXISTS(REPORT.CHECK("qmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("qmake-project", "index.html"))
    assert EXISTS(REPORT.CHECK("qmake-project", "style.css"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "style.css"))

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)


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


def test_qmake_project_do_checktest(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKTEST("qmake-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(REPORT.CHECKTEST("qmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)


def test_autotools_project(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    assert EXISTS(REPORT.ROOT("autotools-project", "metadata.json"))
    assert EXISTS(REPORT.CHECK("autotools-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECK("autotools-project", "index.html"))
    assert EXISTS(REPORT.CHECK("autotools-project", "style.css"))
    assert EXISTS(REPORT.CHECKTEST("autotools-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("autotools-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("autotools-project", "style.css"))

    assert READ(REPORT.ROOT("autotools-project", "metadata.json")).contains(METADATA_S)


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


def test_autotools_project_do_checktest(shared_report_build):
    EXISTS = shared_report_build.files.exists
    READ = shared_report_build.files.read

    with READ(REPORT.CHECKTEST("autotools-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(REPORT.CHECKTEST("autotools-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)
