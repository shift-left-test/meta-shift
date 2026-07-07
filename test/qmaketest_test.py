#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from cpptest_base import (
    assert_arithmetic_coverage,
    assert_checktest_summary,
    assert_coverage_branch_in_xml,
    assert_coverage_branch_text,
    assert_coverage_excludes,
    assert_task_metadata,
    assert_test_filter,
    assert_test_html_report,
    assert_test_shuffle,
    assert_test_suppress_failures,
    assert_verify_without_report_dir,
)


RECIPE = "qmake-project"


def test_do_checktest(stdout, report):
    assert_checktest_summary(stdout, report, RECIPE)


def test_do_coverage(stdout, report):
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert_arithmetic_coverage(report, RECIPE)


def test_do_coverage_branch(stdout, report):
    assert_coverage_branch_in_xml(report, RECIPE)


def test_do_coverage_branch_text(report):
    assert_coverage_branch_text(report, RECIPE)


def test_do_coverage_excludes(stdout, report):
    assert_coverage_excludes(report, RECIPE)


def test_do_verify(test_build):
    assert_verify_without_report_dir(test_build, RECIPE)


def test_do_test(stdout, report):
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    with report.files.readAsXml("report/qmake-project-1.0.0-r0/test/test-qt-gtest.xml") as data:
        data = data["testsuites/testsuite"]
        assert any(x["name"] == "PlusTest" and x["tests"] == "2" and x["failures"] == "1" for x in data)
        assert any(x["name"] == "MinusTest" and x["tests"] == "2" and x["failures"] == "1" for x in data)
    with report.files.readAsXml("report/qmake-project-1.0.0-r0/test/tests/plus_test/test_result.xml") as data:
        data = data["testsuite"]
        assert data["name"] == "qmake-project.PlusTest" and data["tests"] == "4" and data["failures"] == "1"
    with report.files.readAsXml("report/qmake-project-1.0.0-r0/test/tests/minus_test/test_result.xml") as data:
        data = data["testsuite"]
        assert data["name"] == "qmake-project.MinusTest" and data["tests"] == "4" and data["failures"] == "1"


def test_do_test_html_report(report):
    assert_test_html_report(report, RECIPE)
    # the flat and nested XMLs must be merged into the single report
    with report.files.read("report/qmake-project-1.0.0-r0/test/index.html") as html:
        assert html.containsAll("PlusTest", "MinusTest")


def test_do_test_filter(test_build):
    assert_test_filter(test_build, RECIPE)


def test_do_test_shuffle(test_build):
    assert_test_shuffle(test_build, RECIPE)


def test_do_test_suppress_failures(test_build):
    assert_test_suppress_failures(test_build, RECIPE)


def test_task_metadata(report):
    assert_task_metadata(report, RECIPE)
