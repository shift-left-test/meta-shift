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
    pkgs = sdk_build.files.read("buildhistory/sdk/{SDK_NAME}/{IMAGE_BASENAME}/host/installed-packages.txt")
    assert pkgs.contains("nativesdk-cmake_3.3.1-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-cppcheck_2.6-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-cpplint_1.5.5-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-gcovr_4.2-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-lcov_1.11-r0_x86_64-nativesdk.ipk")
    assert pkgs.contains("nativesdk-qemu_2.4.0-r1_x86_64-nativesdk.ipk")

    pkgs = sdk_build.files.read("buildhistory/sdk/{SDK_NAME}/{IMAGE_BASENAME}/target/installed-packages.txt")
    assert pkgs.contains("fff_1.1-r0_{TUNE_PKGARCH}.ipk")
    assert pkgs.contains("gtest_1.7.0-r0_{TUNE_PKGARCH}.ipk")

    pkgs = sdk_build.files.read("buildhistory/sdk/{SDK_NAME}/{IMAGE_BASENAME}/files-in-sdk.txt")
    assert pkgs.contains("{SDKTARGETSYSROOT}/usr/include/fff/fff.h")
    assert pkgs.contains("{SDKPATHNATIVE}/usr/share/cmake-3.3/Modules/CMakeUtils.cmake")
    assert pkgs.contains("{SDKPATHNATIVE}/usr/share/cmake-3.3/Modules/FindGMock.cmake")
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
    assert o.stdout.contains("-- Found CPPLINT code checker: Unsupported")
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
