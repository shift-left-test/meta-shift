#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 Sung Gon Kim

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

import pytest


def test_core_image_minimal_do_checkcode(test_clang_build):
    o = test_clang_build.shell.execute("bitbake core-image-minimal -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkcodeall(test_clang_build):
    o = test_clang_build.shell.execute("bitbake core-image-minimal -c checkcodeall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")


def test_core_image_minimal_do_checktest(test_clang_build):
    o = test_clang_build.shell.execute("bitbake core-image-minimal -c checktest")
    assert o.stderr.contains("ERROR: Task do_checktest does not exist for target core-image-minimal")


def test_core_image_minimal_do_checktestall(test_clang_build):
    o = test_clang_build.shell.execute("bitbake core-image-minimal -c checktestall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checktest:                    Mutant Population Report")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checktest:                              Mutation Coverage Report")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checktest:                    Mutant Population Report")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checktest:                              Mutation Coverage Report")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest:                    Mutant Population Report")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest:                              Mutation Coverage Report")


def test_cmake_project_do_checkcode(test_clang_build):
    o = test_clang_build.shell.execute("bitbake cmake-project -c checkcode")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")


def test_cmake_project_do_checktest(test_clang_build):
    o = test_clang_build.shell.execute("bitbake cmake-project -c checktest")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checktest:                    Mutant Population Report")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checktest:                              Mutation Coverage Report")


def test_qmake5_project_do_checkcode(test_clang_build):
    o = test_clang_build.shell.execute("bitbake qmake5-project -c checkcode")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")


def test_qmake5_project_do_checktest(test_clang_build):
    o = test_clang_build.shell.execute("bitbake qmake5-project -c checktest")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checktest:                    Mutant Population Report")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checktest:                              Mutation Coverage Report")


def test_autotools_project_do_checkcode(test_clang_build):
    o = test_clang_build.shell.execute("bitbake autotools-project -c checkcode")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* clang-tidy is running...")


def test_autotools_project_do_checktest(test_clang_build):
    o = test_clang_build.shell.execute("bitbake autotools-project -c checktest")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest:                    Mutant Population Report")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest:                              Mutation Coverage Report")
