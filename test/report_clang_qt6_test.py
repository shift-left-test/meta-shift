#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest


SENTINEL_HTML_TITLE = '<h1>Sentinel Mutation Coverage Report</h1>'
SAGE_HTML_TITLE = '<h1>Sage Report</h1>'
METADATA_S = '"S": "'


class REPORT:
    PF = {
        "qmake-project": "qmake-project-1.0.0-r0",
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
def shared_report_build(report_clang_qt6_build):
    report_clang_qt6_build.files.remove("report")
    assert report_clang_qt6_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()
    return report_clang_qt6_build


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
