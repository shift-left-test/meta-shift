#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_core_image_minimal_do_testall(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c testall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_testall: No recipes found to run 'do_test' task.")


def test_core_image_minimal_do_reportall(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c reportall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_reportall: No recipes found to run 'do_report' task.")


def test_cmake_project_do_build(release_build):
    stdout = release_build.shell.execute("bitbake cmake-project -e | grep ^DEPENDS=").stdout
    assert stdout.contains("cmake-native")
    assert not stdout.contains("lcov-native")
    assert not stdout.containsAny("gtest", "googletest")


def test_qmake_project_do_build(release_build):
    stdout = release_build.shell.execute("bitbake qmake-project -e | grep ^DEPENDS=").stdout
    assert stdout.contains("qtbase")
    assert not stdout.contains("lcov-native")


def test_autotools_project_do_build(release_build):
    stdout = release_build.shell.execute("bitbake autotools-project -e | grep ^DEPENDS=").stdout
    assert not stdout.contains("lcov-native")
    assert not stdout.containsAny("gtest", "googletest")
