#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import pytest
from contextlib import contextmanager


@contextmanager
def externalsrc_execute(build, recipe, task):
    try:
        build.shell.run("devtool modify %s" % recipe)
        assert build.files.exists(os.path.join("workspace", "sources", recipe))
        yield build.shell.execute("bitbake %s -c %s" % (recipe, task))
    finally:
        build.shell.run("devtool reset %s" % recipe)
        build.shell.run("bitbake-layers remove-layer workspace")
        build.files.remove("workspace")


@pytest.fixture(scope="module")
def stdout(test_build):
    with externalsrc_execute(test_build, "cmake-project", "report") as o:
        return o.stdout


def test_cmake_project_do_test(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")


def test_cmake_project_do_coverage(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_cmake_project_do_checkcode(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_cmake_project_do_checkcache(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")


def test_cmake_project_do_checkrecipe(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Checking the specified recipes or files for the styling issues...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")


def test_cmake_project_report(report_build):
    report_build.files.remove("report")
    with externalsrc_execute(report_build, "cmake-project", "report") as o:
        assert o.stderr.empty()
        assert report_build.files.exists("report/cmake-project-1.0.0-r0/metadata.json")
        assert report_build.files.exists("report/cmake-project-1.0.0-r0/test/OperatorTest.xml")
        assert report_build.files.exists("report/cmake-project-1.0.0-r0/coverage/coverage.xml")
        assert report_build.files.exists("report/cmake-project-1.0.0-r0/checkcode/sage_report.json")
        assert report_build.files.exists("report/cmake-project-1.0.0-r0/checkrecipe/recipe_violations.json")


def test_sage_native_project_do_build(test_build):
    # Test if the setuptools within devtool-modify works properly with the host python
    with externalsrc_execute(test_build, "sage-native", "build") as o:
        assert o.stderr.empty()
        assert o.returncode == 0
