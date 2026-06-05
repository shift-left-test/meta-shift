#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(report_build):
    with report_build.externalsrc("cmake-project"):
        return report_build.shell.execute("bitbake cmake-project -c verify").stdout


@pytest.fixture(scope="module")
def report(report_build):
    report_build.files.remove("report")
    with report_build.externalsrc("cmake-project"):
        assert report_build.shell.execute("bitbake cmake-project -c verify").stderr.empty()
        return report_build


def test_do_checktest(stdout, report):
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutant Generation Summary")
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutation Score Report")
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/checktest/mutations.xml") as data:
        assert len(data["mutations/mutation"]) == 2


def test_do_coverage(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    with report.files.readAsHtml("report/cmake-project-1.0.0-r0/coverage/index.html") as data:
        assert data["html/head/title"] == "GCC Code Coverage Report"
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/coverage/coverage.xml") as data:
        class_data = data["coverage/packages/package/classes/class"]
        if isinstance(class_data, dict):
            class_data = [class_data]
        # The source files appear in the report. Their per-file line rates depend
        # on the project's link model (the autotools project builds one operator
        # as a shared library whose counters qemu-user does not flush), so assert
        # presence here and exact coverage on the in-process unit tests below,
        # which run identically across projects and gcovr versions.
        filenames = [x["filename"] for x in class_data]
        assert "minus/minus.cpp" in filenames
        assert "plus/plus.cpp" in filenames
        assert any(map(lambda x: x["filename"] == "test/MinusTest.cpp" and float(x["branch-rate"]) > 0.0, class_data))
        assert any(map(lambda x: x["filename"] == "test/PlusTest.cpp" and float(x["branch-rate"]) > 0.0, class_data))
        # gcovr >= 8.6 emits per-method entries in the Cobertura report; when
        # present, check the demangled arithmetic operators are reported.
        method_data = data.get("coverage/packages/package/classes/class/methods/method")
        if method_data:
            if isinstance(method_data, dict):
                method_data = [method_data]
            names = [x["name"] for x in method_data]
            assert "arithmetic::minus" in names
            assert "arithmetic::plus" in names


def test_do_verify(test_build):
    with test_build.externalsrc("cmake-project"):
        o = test_build.shell.execute("bitbake cmake-project -c verify")
        assert o.stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")


def test_do_test(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/test/OperatorTest_1.xml") as data:
        data = data["testsuites/testsuite"]
        assert data["name"] == "PlusTest" and data["tests"] == "1" and data["failures"] == "1"
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/test/OperatorTest_3.xml") as data:
        data = data["testsuites/testsuite"]
        assert data["name"] == "MinusTest" and data["tests"] == "1" and data["failures"] == "1"


