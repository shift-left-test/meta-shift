#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_qt6_build):
    return test_qt6_build.shell.execute("bitbake qmake-project -c report").stdout


def test_qmake_project_do_test(stdout):
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")


def test_qmake_project_do_coverage(stdout):
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_qmake_project_do_checkcode(stdout):
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_qmake_project_do_checkcache(stdout):
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Source Availability")


def test_qmake_project_do_checkrecipe(stdout):
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
