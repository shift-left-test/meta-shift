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


def test_cmake_project_srcrev(test_build):
    def check_cmake_project_srcrev(target_srcrev):
        try:
            o = test_build.shell.execute("devtool clone cmake-project %s" % target_srcrev)
            assert o.returncode == 0
            gitdir = os.path.join("workspace", "sources", "cmake-project")
            assert test_build.files.exists(gitdir)

            o = test_build.shell.execute("git --git-dir %s/.git rev-parse HEAD" % os.path.join(test_build.build_dir, gitdir))
            assert o.returncode == 0
            assert o.stdout.contains(target_srcrev)
        finally:
            test_build.shell.run("devtool reset cmake-project")
            test_build.shell.run("bitbake-layers remove-layer workspace")
            test_build.files.remove("workspace")

    check_cmake_project_srcrev("4dc56f8d6145f5b54583e0ac0c7ca508e9b3f987")
    check_cmake_project_srcrev("1579cd9e0db8a63ffaeb40a25cf17031787d4ea8")


def test_wrong_srcrev(test_build):
    try:
        o = test_build.shell.execute("devtool clone sage-native ffffffffffffffffffffffffffffffffffffffff")
        assert o.returncode != 0
        assert not test_build.files.exists(os.path.join("workspace", "sources", "sage-native"))
    finally:
        test_build.shell.run("bitbake-layers remove-layer workspace")
        test_build.files.remove("workspace")


def test_fail_patch(test_build):
    try:
        o = test_build.shell.execute("devtool clone oelint-adv-native 8c9b4d2a0c9bb7bce995de0268edcd886fd9ed13")
        assert o.stderr.contains("ERROR: Applying '0001-compatibility-with-python2.patch' failed")
        assert o.returncode != 0
        assert not test_build.files.exists(os.path.join("workspace", "sources", "oelint-adv-native"))
    finally:
        test_build.shell.run("bitbake-layers remove-layer workspace")
        test_build.files.remove("workspace")

