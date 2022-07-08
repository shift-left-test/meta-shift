#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_cmake_project_coverage_filter(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_EXCLUDES", "program */src/*.cpp test/MinusTest.cpp")
        assert report_build.shell.execute("bitbake cmake-project -c coverage").stderr.empty()
        
        coverage = report_build.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage.containsElementWithAttrib("class", {"filename":"test/PlusTest.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"program/main.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"plus/src/plus.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"minius/src/minus.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"test/MinusTest.cpp"})


def test_qmake_project_coverage_filter(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_EXCLUDES", "program */src/*.cpp test/MinusTest.cpp")
        assert report_build.shell.execute("bitbake qmake-project -c coverage").stderr.empty()
        
        coverage = report_build.files.readAsXml("report/qmake-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage.containsElementWithAttrib("class", {"filename":"test/PlusTest.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"program/main.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"plus/src/plus.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"minius/src/minus.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"test/MinusTest.cpp"})


def test_autotools_project_coverage_filter(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_COVERAGE_EXCLUDES", "program */src/*.cpp test/MinusTest.cpp")
        assert report_build.shell.execute("bitbake autotools-project -c coverage").stderr.empty()
        
        coverage = report_build.files.readAsXml("report/autotools-project-1.0.0-r0/coverage/coverage.xml")
        assert coverage.containsElementWithAttrib("class", {"filename":"test/PlusTest.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"program/main.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"plus/src/plus.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"minius/src/minus.cpp"})
        assert not coverage.containsElementWithAttrib("class", {"filename":"test/MinusTest.cpp"})
