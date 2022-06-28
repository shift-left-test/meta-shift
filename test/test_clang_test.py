#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_clang_build):
    return test_clang_build.shell.execute("bitbake core-image-minimal -c reportall").stdout


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


def test_do_checktest_seed_option(test_clang_build):
    o = test_clang_build.shell.execute("bitbake cmake-project -c checktest")
    assert o.stdout.contains("cmake-project/1.0.0-r0/git/minus/src/minus.cpp,minus,30,12,30,13,*")
    assert o.stdout.contains("cmake-project/1.0.0-r0/git/program/main.cpp,main,37,39,37,40,*")

    o = test_clang_build.shell.execute("bitbake cmake-project -c checktestall")
    assert o.stdout.contains("cmake-project/1.0.0-r0/git/minus/src/minus.cpp,minus,30,12,30,13,*")
    assert o.stdout.contains("cmake-project/1.0.0-r0/git/program/main.cpp,main,37,39,37,40,*")


def test_do_checktest_verbose_option(test_clang_build):
    o = test_clang_build.shell.execute("bitbake autotools-project -c checktest")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest: CommandPopulate [INFO] random seed:1234")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest: CommandMutate [INFO] mutant:")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest: CommandEvaluate [INFO] mutant:")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest: CommandReport [INFO] evaluation-file")
