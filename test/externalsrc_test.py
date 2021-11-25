#-*- coding: utf-8 -*-
#!/usr/bin/python3

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


def test_cmake_project_do_test(test_build):
    with externalsrc_execute(test_build, "cmake-project", "test") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")


def test_cmake_project_do_coverage(test_build):
    with externalsrc_execute(test_build, "cmake-project", "coverage") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_cmake_project_do_checkcode(test_build):
    with externalsrc_execute(test_build, "cmake-project", "checkcode") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_cmake_project_do_checkcache(test_build):
    with externalsrc_execute(test_build, "cmake-project", "checkcache") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")


def test_cmake_project_do_checkrecipe(test_build):
    with externalsrc_execute(test_build, "cmake-project", "checkrecipe") as o:
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Checking the specified recipes or files for the styling issues...")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")


def test_sage_native_project_do_build(test_build):
    # Test if the setuptools within devtool-modify works properly with the host python
    with externalsrc_execute(test_build, "sage-native", "build") as o:
        assert o.stderr.empty()
        assert o.returncode == 0


def test_oelint_adv_native_project_do_build(test_build):
    with externalsrc_execute(test_build, "oelint-adv-native", "build") as o:
        assert o.stderr.empty()
        assert o.returncode == 0

