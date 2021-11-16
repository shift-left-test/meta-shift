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

    assert EXISTS(REPORT.ROOT("qmake-project", "metadata.json"))

    assert EXISTS(REPORT.CHECK("qmake-project", "sage_report.json"))

    assert EXISTS(REPORT.CHECKTEST("qmake-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "style.css"))


def test_qmake_project_do_checkcodeall(report_clang_qt6_build):
    report_clang_qt6_build.files.remove("report")
    assert report_clang_qt6_build.shell.execute("bitbake qmake-project -c checkcodeall").stderr.empty()
    READ = report_clang_qt6_build.files.read
    with READ(REPORT.CHECK("qmake-project", "sage_report.json")) as f:
        assert f.contains('"complexity": [')
        assert f.contains('"duplications": [')
        assert f.contains('"size": [')
        assert f.contains('"violations": [')

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)


def test_qmake_project_do_checktestall(report_clang_qt6_build):
    report_clang_qt6_build.files.remove("report")
    assert report_clang_qt6_build.shell.execute("bitbake qmake-project -c checktestall").stderr.empty()
    READ = report_clang_qt6_build.files.read
    with READ(REPORT.CHECKTEST("qmake-project", "mutations.xml")) as f:
        assert f.contains('</mutations>')
    with READ(REPORT.CHECKTEST("qmake-project", "index.html")) as f:
        assert f.contains(SENTINEL_HTML_TITLE)

    assert READ(REPORT.ROOT("qmake-project", "metadata.json")).contains(METADATA_S)


def test_qmake_project_do_reportall(report_clang_qt6_build):
    report_clang_qt6_build.files.remove("report")

    assert report_clang_qt6_build.shell.execute("bitbake qmake-project -c reportall").stderr.empty()

    EXISTS = report_clang_qt6_build.files.exists

    assert EXISTS(REPORT.ROOT("qmake-project", "metadata.json"))

    assert EXISTS(REPORT.CHECK("qmake-project", "sage_report.json"))

    assert EXISTS(REPORT.CHECKTEST("qmake-project", "mutations.xml"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "index.html"))
    assert EXISTS(REPORT.CHECKTEST("qmake-project", "style.css"))