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
import os
import shutil
import tempfile


def test_populate_sdk(sdk_build):
    pkgs = sdk_build.files.read("buildhistory/sdk/{SDK_NAME}{SDK_EXT}/{IMAGE_BASENAME}/host/installed-packages.txt")
    assert pkgs.contains("nativesdk-cmake_3.8.2-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-cppcheck_2.4.1-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-cpplint_1.4.5-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-gcovr_4.2-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-lcov_1.11-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-qemu_2.10.0-r0_x86_64-nativesdk.ipk")

    pkgs = sdk_build.files.read("buildhistory/sdk/{SDK_NAME}{SDK_EXT}/{IMAGE_BASENAME}/target/installed-packages.txt")
    assert pkgs.contains("fff_1.0-r0_{TUNE_PKGARCH}.ipk")
    assert pkgs.contains("gtest_1.8.0-r0_{TUNE_PKGARCH}.ipk")

    pkgs = sdk_build.files.read("buildhistory/sdk/{SDK_NAME}{SDK_EXT}/{IMAGE_BASENAME}/files-in-sdk.txt")
    assert pkgs.contains("{SDKTARGETSYSROOT}/usr/include/fff/fff.h")
    assert pkgs.contains("{SDKPATHNATIVE}/usr/share/cmake-3.8/Modules/CMakeUtils.cmake")
    assert pkgs.contains("{SDKPATHNATIVE}/usr/share/cmake-3.8/Modules/FindGMock.cmake")
    assert pkgs.contains("{SDKPATHNATIVE}/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake")


def test_humidifier_project(sdk_build):
    project_dir = tempfile.mkdtemp()
    sdk_build.sdk_shell.execute("git clone http://mod.lge.com/hub/yocto/sample/humidifier-project.git {}".format(project_dir))
    assert sdk_build.files.exists(project_dir)

    cd_cmd = "cd {0} && ".format(project_dir)
    o = sdk_build.sdk_shell.execute(cd_cmd + "cmake -DENABLE_TESTS=ON .")

    assert o.stdout.contains("gcc -- works")
    assert o.stdout.contains("g++ -- works")
    assert o.stdout.contains("-- Found cross-compiling emulator: TRUE")
    assert o.stdout.contains("-- Found CPPCHECK code checker: Unsupported")
    assert o.stdout.contains("-- Found CPPLINT code checker: TRUE")
    assert o.stdout.contains("-- Found gcovr program: TRUE")
    assert o.stdout.contains("-- Found GTest: {0}/sysroots/{1}/usr/lib/libgtest.a".format(sdk_build.sdk_dir, sdk_build.kwargs["REAL_MULTIMACH_TARGET_SYS"]))
    assert o.stdout.contains("-- Found GMock: {0}/sysroots/{1}/usr/lib/libgmock.a".format(sdk_build.sdk_dir, sdk_build.kwargs["REAL_MULTIMACH_TARGET_SYS"]))

    o = sdk_build.sdk_shell.execute(cd_cmd + "make all")
    assert o.returncode == 0

    o = sdk_build.sdk_shell.execute(cd_cmd + "make test")
    assert o.stdout.contains("HumidifierTest.testNothingHappensWhenInitialized .......................   Passed")
    assert o.stdout.contains("HumidifierTest.testNothingChangesWhenHumidityLevelAsDesired ............   Passed")
    assert o.stdout.contains("HumidifierTest.testIncreaseHumidityLevelWhenCurrentLowerThanDesired ....   Passed")
    assert o.stdout.contains("HumidifierTest.testDecreaseHumidityLevelWhenCurrentLargerThanDesired ...   Passed")
    assert o.stdout.contains("100% tests passed, 0 tests failed out of 4")

    o = sdk_build.sdk_shell.execute(cd_cmd + "make coverage")
    assert o.stdout.contains("Running gcovr...")
    assert o.stdout.contains("lines: 100.0%")

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
    assert o.stderr.contains("{}:1:  Missing space before {{{{  [whitespace/braces] [5]".format(f.name))
