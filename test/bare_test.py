#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_build_recipes(release_build):
    recipes = ["cmake-native", "nativesdk-cmake",
               "compiledb-native",
               "cppcheck-native", "nativesdk-cppcheck",
               "cpplint-native", "nativesdk-cpplint",
               "fff",
               "nativesdk-gcovr",
               "gtest",
               "gmock",
               "lcov-native", "nativesdk-lcov",
               "python3-bashlex",
               "python3-click",
               "python3-lcov-cobertura-native", "nativesdk-python3-lcov-cobertura",
               "python3-shutilwhich",
               "qemu-native", "nativesdk-qemu",
               "sage-native",
               "oelint-adv-native"]
    assert release_build.shell.execute("bitbake " + " ".join(recipes)).stderr.empty()
