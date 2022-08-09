#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_cmake_project_excludes(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_EXCLUDES", "program *us/*.cpp test/MinusTest.cpp")
        assert report_build.shell.execute("bitbake cmake-project -c coverage").stderr.empty()

        coverage = report_build.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "minus/minus.cpp"
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "plus/plus.cpp"
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "program/main.cpp"
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "test/MinusTest.cpp"
        assert coverage["coverage/packages/package/classes/class"]["filename"] == "test/PlusTest.cpp"
        assert coverage["coverage/packages/package/classes/class"]["line-rate"] == "1.0"
        assert coverage["coverage/packages/package/classes/class"]["branch-rate"] != "0.0"


def test_qmake_project_excludes(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_EXCLUDES", "program *us/*.cpp test/MinusTest.cpp")
        assert report_build.shell.execute("bitbake qmake-project -c coverage").stderr.empty()

        coverage = report_build.files.readAsXml("report/qmake-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage["coverage/packages/package/classes/class"][0]["filename"] != "minus/minus.cpp"
        assert coverage["coverage/packages/package/classes/class"][0]["filename"] != "plus/plus.cpp"
        assert coverage["coverage/packages/package/classes/class"][0]["filename"] != "program/main.cpp"
        assert coverage["coverage/packages/package/classes/class"][0]["filename"] != "test/MinusTest.cpp"
        assert coverage["coverage/packages/package/classes/class"][0]["filename"] == "test/PlusTest.cpp"
        assert coverage["coverage/packages/package/classes/class"][0]["line-rate"] == "1.0"
        assert coverage["coverage/packages/package/classes/class"][0]["branch-rate"] != "0.0"


def test_autotools_project_excludes(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_EXCLUDES", "program *us/*.cpp test/MinusTest.cpp")
        assert report_build.shell.execute("bitbake autotools-project -c coverage").stderr.empty()

        coverage = report_build.files.readAsXml("report/autotools-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "minus/minus.cpp"
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "plus/plus.cpp"
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "program/main.cppd"
        assert coverage["coverage/packages/package/classes/class"]["filename"] != "test/MinusTest.cpp"
        assert coverage["coverage/packages/package/classes/class"]["filename"] == "test/PlusTest.cpp"
        assert coverage["coverage/packages/package/classes/class"]["line-rate"] == "1.0"
        assert coverage["coverage/packages/package/classes/class"]["branch-rate"] != "0.0"


def test_cmake_project_branch_on(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_BRANCH", "1")
        assert report_build.shell.execute("bitbake cmake-project -c coverage").stderr.empty()
        coverage = report_build.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage["coverage"]["branch-rate"] != "0.0"


def test_cmake_project_branch_off(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_BRANCH", "0")
        assert report_build.shell.execute("bitbake cmake-project -c coverage").stderr.empty()
        coverage = report_build.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage["coverage"]["branch-rate"] == "0.0"
