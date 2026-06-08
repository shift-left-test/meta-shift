#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.parsers.data import asList


RECIPE = "enact-project"


def test_do_coverage(stdout, report):
    assert stdout.matches("enact-project-1.0.0-r0 do_coverage: File(.+?)Stmts(.+?)Branch(.+?)Funcs(.+?)Lines")
    with report.files.readAsHtml("report/enact-project-1.0.0-r0/coverage/index.html") as data:
        assert data["html/head/title"] == "Code coverage report for All files"
    with report.files.readAsXml("report/enact-project-1.0.0-r0/coverage/cobertura-coverage.xml") as data:
        class_data = asList(data["coverage/packages/package/classes/class"])
        assert any(map(lambda x: x["name"] == "converter.js" and float(x["line-rate"]) == 1.0 and float(x["branch-rate"]) > 0.0, class_data))


def test_do_verify(test_build):
    o = test_build.shell.execute("bitbake enact-project -c verify")
    assert o.stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")


def test_do_coverage_junit_report(stdout, report):
    # enact's do_verify runs coverage + checktest (not do_test), so the jest-junit
    # report under <PF>/test/ is emitted by the coverage run; validate it here.
    assert stdout.contains("enact-project-1.0.0-r0 do_coverage: Running tests with coverage...")
    with report.files.readAsXml("report/enact-project-1.0.0-r0/test/junit.xml") as data:
        suites = asList(data["testsuites/testsuite"])
        assert any(x["name"] == "undefined" and x["tests"] == "2" and x["failures"] == "1" for x in suites)
        assert any(x["name"] == "test suite for converter" and x["tests"] == "4" and x["failures"] == "0" for x in suites)


def test_do_test_suppress_failures(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SUPPRESS_FAILURES", "0")
        o = test_build.shell.execute("bitbake enact-project -c test")
        assert o.returncode != 0
