#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_qmake_project_do_test(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c test")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")


def test_qmake_project_do_coverage(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c coverage")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_qmake_project_do_checkcode(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkcode")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_qmake_project_do_checkcache(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkcache")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Source Availability")


def test_qmake_project_do_checkrecipe(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkrecipe")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
