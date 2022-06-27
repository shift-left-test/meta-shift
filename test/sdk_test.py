#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest
import os
import shutil
import tempfile


def test_populate_sdk(sdk_build):
    pkgs = sdk_build.files.read("buildhistory/sdk/*/*/files-in-sdk.txt")
    assert pkgs.matches(r".+/usr/share/cmake-\d+(\.\d+)+/Modules/CMakeUtils.cmake")
    assert pkgs.matches(r".+/usr/share/cmake-\d+(\.\d+)+/Modules/FindGMock.cmake")
    assert pkgs.matches(r".+/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake")
    assert pkgs.matches(r".+/usr/bin/cmake")
    assert pkgs.matches(r".+/usr/bin/cppcheck")
    assert pkgs.matches(r".+/usr/bin/cpplint")
    assert pkgs.matches(r".+/usr/bin/gcovr")
    assert pkgs.matches(r".+/usr/bin/lcov")
    assert pkgs.matches(r".+/usr/bin/qemu-")
    assert pkgs.matches(r".+/usr/include/fff/fff.h")
    assert pkgs.matches(r".+/usr/include/gtest/gtest.h")


def test_sqlite3wrapper_do_build(sdk_build):
    project_dir = tempfile.mkdtemp()
    try:
        sdk_build.sdk_shell.execute("git clone https://github.com/shift-left-test/SQLite3Wrapper.git {}".format(project_dir))
        assert sdk_build.files.exists(project_dir)

        cd_cmd = "cd {0} && ".format(project_dir)
        o = sdk_build.sdk_shell.execute(cd_cmd + "cmake -DWITH_TESTS=ON .")

        assert o.stdout.contains("-- Found cross-compiling emulator: TRUE")
        assert o.stdout.contains("-- Found CPPCHECK code checker: TRUE")
        assert o.stdout.contains("-- Found CPPLINT code checker: TRUE")
        assert o.stdout.contains("-- Found gcovr program: TRUE")
        assert o.stdout.matches(r"-- Found GTest: {0}/sysroots/.+/usr/lib/cmake/GTest/GTestConfig.cmake".format(sdk_build.sdk_dir))
        assert o.stdout.matches(r"-- Found GMock: {0}/sysroots/.+/usr/lib/libgmock.a".format(sdk_build.sdk_dir))

        o = sdk_build.sdk_shell.execute(cd_cmd + "make all")
        assert o.returncode == 0

        o = sdk_build.sdk_shell.execute(cd_cmd + "make test")
        assert o.stdout.contains("DatabaseTest.testExecuteOKWhenValidQueryGiven ..........   Passed")
        assert o.stdout.contains("StatementTest.testExecuteOKWhenValidQueryGiven .........   Passed")
        assert o.stdout.contains("ColumnTest.testGetColumnOKWhenValidIndexGiven ..........   Passed")
        assert o.stdout.matches(r"\d+(\.\d+)?% tests passed, \d+ tests failed out of \d+")

        o = sdk_build.sdk_shell.execute(cd_cmd + "make coverage")
        assert o.stdout.contains("Running gcovr...")
        assert o.stdout.matches(r"lines: \d+(\.\d+)?% \(\d+ out of \d+\)")
        assert o.stdout.matches(r"branches: \d+(\.\d+)?% \(\d+ out of \d+\)")

    finally:
        shutil.rmtree(project_dir)


def test_cppcheck(sdk_build):
    cppcheck_path = "{0}/usr/bin/cppcheck".format(sdk_build.oecore_native_sysroot)
    assert os.path.exists(cppcheck_path), "{0} not found: {1}".format("cppcheck", cppcheck_path)

    f =  tempfile.NamedTemporaryFile(mode="w", suffix=".cpp")
    f.write("int main(){int a[10]; a[10] = 0;}")
    f.flush()

    o = sdk_build.sdk_shell.execute("{} --enable=all {}".format(cppcheck_path, f.name))
    assert o.stderr.contains("{}:1:24: error: Array 'a[10]' accessed at index 10, which is out of bounds.".format(f.name)), o.stderr
    assert o.stderr.contains("{}:1:29: style: Variable 'a[10]' is assigned a value that is never used.".format(f.name)), o.stderr


def test_cpplint(sdk_build):
    cpplint_path = "{0}/usr/bin/cpplint".format(sdk_build.oecore_native_sysroot)
    assert os.path.exists(cpplint_path), "{0} not found: {1}".format("cpplint", cpplint_path)

    f = tempfile.NamedTemporaryFile(mode="w", suffix=".cpp")
    f.write("int main(){int a[10]; a[10] = 0;}")
    f.flush()

    o = sdk_build.sdk_shell.execute("{} {}".format(cpplint_path, f.name))
    assert o.stderr.contains("{}:0:  No copyright message found.  You should have a line: \"Copyright [year] <Copyright Owner>\"  [legal/copyright] [5]".format(f.name))
    assert o.stderr.contains("{}:1:  Missing space before {{  [whitespace/braces] [5]".format(f.name))
