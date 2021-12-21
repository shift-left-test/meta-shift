#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest


SENTINEL_HTML_TITLE = '<h1>Sentinel Mutation Coverage Report</h1>'
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


def test_core_image_minimal_do_reportall(report_clang_qt6_build):
    report_clang_qt6_build.files.remove("report")

    assert report_clang_qt6_build.shell.execute("bitbake core-image-minimal -c reportall").stderr.empty()

    EXISTS = report_clang_qt6_build.files.exists
    READ = report_clang_qt6_build.files.read

    # qmake-project
    assert EXISTS(REPORT.ROOT("qmake-project", "metadata.json"))
    assert EXISTS(REPORT.CHECK("qmake-project", "sage_report.json"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "style.css"))

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)

    # qmake-project:do_checkcode
    with READ(REPORT.CHECK("qmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    # qmake-project:do_checktest
    with READ(REPORT.CHECKTEST("qmake-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(REPORT.CHECKTEST("qmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)
