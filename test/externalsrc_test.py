#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 LG Electronics, Inc.

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


def test_cmake_project_do_test(test_clang_build):
    with externalsrc_execute(test_clang_build, "cmake-project", "test") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")


def test_cmake_project_do_coverage(test_clang_build):
    with externalsrc_execute(test_clang_build, "cmake-project", "coverage") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_cmake_project_do_checkcode(test_clang_build):
    with externalsrc_execute(test_clang_build, "cmake-project", "checkcode") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_cmake_project_do_checkcache(test_clang_build):
    with externalsrc_execute(test_clang_build, "cmake-project", "checkcache") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")


def test_cmake_project_do_checktest(test_clang_build):
    with externalsrc_execute(test_clang_build, "cmake-project", "checktest") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checktest:                    Mutant Population Report")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checktest:                              Mutation Coverage Report")


def test_cmake_project_do_checkrecipe(test_clang_build):
    with externalsrc_execute(test_clang_build, "cmake-project", "checkrecipe") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Checking the specified recipes or files for the styling issues...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")


def test_sage_native_project_do_build(test_clang_build):
    # Test if the setuptools within devtool-modify works properly with the host python
    with externalsrc_execute(test_clang_build, "sage-native", "build") as o:
        assert o.stderr.empty()
        assert o.returncode == 0


def test_oelint_adv_native_project_do_build(test_clang_build):
    with externalsrc_execute(test_clang_build, "oelint-adv-native", "build") as o:
        assert o.stderr.empty()
        assert o.returncode == 0
