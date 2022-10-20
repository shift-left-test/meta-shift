#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_build):
    return test_build.shell.execute("bitbake enact-project -c report").stdout


@pytest.fixture(scope="module")
def report(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake enact-project -c report").stderr.empty()
    return report_build


def test_do_checkcache(stdout, report):
    assert stdout.contains("enact-project-1.0.0-r0 do_checkcache: Source Availability")
    with report.files.readAsJson("report/enact-project-1.0.0-r0/checkcache/caches.json") as data:
        assert "Missed" in data["Premirror"]
        assert "Found" in data["Premirror"]["Summary"]


def test_do_checkcode(stdout, report):
    assert stdout.contains("enact-project-1.0.0-r0 do_checkcode: > enact lint")


def test_do_checkrecipe(stdout, report):
    assert stdout.contains("enact-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    with report.files.readAsJson("report/enact-project-1.0.0-r0/checkrecipe/recipe_violations.json") as data:
        assert len(data["issues"]) == 0
    with report.files.readAsJson("report/enact-project-1.0.0-r0/checkrecipe/files.json") as data:
        assert data["lines_of_code"][0]["file"].endswith("enact-project_1.0.0.bb")
        assert data["lines_of_code"][1]["file"].endswith("enact-project_1.0.0.bbappend")


def test_do_checktest(stdout, report):
    pass


def test_do_checktest_excludes(stdout, report):
    pass


def test_do_checktest_extensions(stdout, report):
    pass


def test_do_checktest_generator(stdout, report):
    pass


def test_do_checktest_seed(stdout, report):
    pass


def test_do_checktest_verbose(stdout, report):
    pass


def test_do_coverage(stdout, report):
    assert stdout.matches("enact-project-1.0.0-r0 do_coverage: File(.+?)Stmts(.+?)Branch(.+?)Funcs(.+?)Lines")
    with report.files.readAsHtml("report/enact-project-1.0.0-r0/coverage/index.html") as data:
        assert data["html/head/title"] == "Code coverage report for All files"
    with report.files.readAsXml("report/enact-project-1.0.0-r0/coverage/cobertura-coverage.xml") as data:
        class_data = data["coverage/packages/package/classes/class"]
        assert any(map(lambda x: x["name"] == "converter.js" and x["line-rate"] == "1" and x["branch-rate"] != "0.0", class_data))


def test_do_coverage_branch(stdout, report):
    pass


def test_do_coverage_excludes(stdout, report):
    pass


def test_do_report(stdout, report):
    assert stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")


def test_do_test(stdout, report):
    assert stdout.contains("enact-project-1.0.0-r0 do_coverage: Running tests...")
    with report.files.readAsXml("report/enact-project-1.0.0-r0/test/junit.xml") as data:
        data = data["testsuites/testsuite"]
        assert any(map(lambda x: x["name"] == "undefined" and x["tests"] == "2" and x["failures"] == "1", data))
        assert any(map(lambda x: x["name"] == "test suite for converter" and x["tests"] == "4" and x["failures"] == "0", data))


def test_do_test_filter(test_build):
    pass


def test_do_test_shuffle(test_build):
    pass


def test_do_test_suppress_failures(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SUPPRESS_FAILURES", "0")
        o = test_build.shell.execute("bitbake enact-project -c test")
        assert o.returncode != 0
