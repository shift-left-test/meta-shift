#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT

These tests check that the required packages appear in the SDK packagegroups
(via bitbake -e) rather than generating a full SDK.
"""


def test_populate_sdk_target(release_build):
    stdout = release_build.shell.execute("bitbake packagegroup-core-standalone-sdk-target -e | grep ^RDEPENDS:packagegroup-core-standalone-sdk-target=").stdout
    assert stdout.containsAll("fff", "googletest")


def test_populate_sdk_host(release_build):
    stdout = release_build.shell.execute("bitbake nativesdk-packagegroup-sdk-host -e | grep ^RDEPENDS:nativesdk-packagegroup-sdk-host=").stdout
    assert stdout.containsAll("nativesdk-cmake",
                              "nativesdk-python3-gcovr",
                              "nativesdk-qemu")

    assert release_build.shell.execute("bitbake nativesdk-cmake").stderr.empty()
    f = "tmp*/work/x86_64-nativesdk-oesdk-linux/nativesdk-cmake/*/sysroot-destdir/" \
        "*/*/*/*/*/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake"
    with release_build.files.read(f) as data:
        assert data.containsAll('set(CMAKE_CROSSCOMPILING_EMULATOR "${QEMU_$ENV{OECORE_TARGET_ARCH}};${QEMU_EXTRAOPTIONS};',
                                '-L;$ENV{SDKTARGETSYSROOT};-E;',
                                'LD_LIBRARY_PATH=$ENV{SDKTARGETSYSROOT}/usr/lib:$ENV{SDKTARGETSYSROOT}/lib:$LD_LIBRARY_PATH"')
