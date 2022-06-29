#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_populate_sdk_target(release_build):
    # Simply check whether required packages exist in a packagegroup, instead of generating the sdk file.
    stdout = release_build.shell.execute("bitbake packagegroup-core-standalone-sdk-target -e | grep ^RDEPENDS_packagegroup-core-standalone-sdk-target=").stdout
    assert stdout.containsAll("fff", "gtest")


def test_populate_sdk_host(release_build):
    # Simply check whether required packages exist in a packagegroup, instead of generating the sdk file.
    stdout = release_build.shell.execute("bitbake nativesdk-packagegroup-sdk-host -e | grep ^RDEPENDS_nativesdk-packagegroup-sdk-host=").stdout
    assert stdout.containsAll("nativesdk-cmake",
                              "nativesdk-cppcheck",
                              "nativesdk-cpplint",
                              "nativesdk-gcovr",
                              "nativesdk-lcov",
                              "nativesdk-qemu")

    # nativesdk-cmake
    assert release_build.shell.execute("bitbake nativesdk-cmake").stderr.empty()
    f = "tmp/work/x86_64-nativesdk-pokysdk-linux/nativesdk-cmake/*/sysroot-destdir/" \
        "*/*/*/*/*/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake"
    assert release_build.files.read(f).containsAll('set(CMAKE_CROSSCOMPILING_EMULATOR "${QEMU_$ENV{OECORE_TARGET_ARCH}};${QEMU_EXTRAOPTIONS};',
                                                   '-L;$ENV{SDKTARGETSYSROOT};-E;',
                                                   'LD_LIBRARY_PATH=$ENV{SDKTARGETSYSROOT}/usr/lib:$ENV{SDKTARGETSYSROOT}/lib:$LD_LIBRARY_PATH"')
