#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_clang_qt6_build):
    return test_clang_qt6_build.shell.execute("bitbake core-image-minimal -c reportall").stdout


def test_core_image_minimal_do_checkcodeall(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")


def test_core_image_minimal_do_checktestall(stdout):
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutant Population Report")
    assert stdout.matches("cmake-project-1.0.0-r0 do_checktest:[ ]+Mutation Coverage Report")
    assert stdout.matches("qmake-project-1.0.0-r0 do_checktest:[ ]+Mutant Population Report")
    assert stdout.matches("qmake-project-1.0.0-r0 do_checktest:[ ]+Mutation Coverage Report")
    assert stdout.matches("autotools-project-1.0.0-r0 do_checktest:[ ]+Mutant Population Report")
    assert stdout.matches("autotools-project-1.0.0-r0 do_checktest:[ ]+Mutation Coverage Report")
