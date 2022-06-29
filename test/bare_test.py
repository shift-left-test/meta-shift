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
               "python-bashlex",
               "python-click",
               "python-enum34",
               "python-lcov-cobertura-native", "nativesdk-python-lcov-cobertura",
               "python-shutilwhich",
               "qemu-native", "nativesdk-qemu",
               "sage-native",
               "oelint-adv-native"]
    assert release_build.shell.execute("bitbake " + " ".join(recipes)).stderr.empty()
