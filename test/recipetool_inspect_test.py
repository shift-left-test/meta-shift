#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import json
import pytest
import shutil
import tempfile


def test_default_format(bare_build):
    o = bare_build.shell.execute("recipetool inspect cpplint")
    assert o.stdout.containsAll("General Information",
                                "-------------------",
                                "Name: cpplint",
                                "Summary: CPPLint - a static code analyzer for C/C++",
                                "Description: A Static code analyzer for C/C++ written in python",
                                "Author: Google Inc.",
                                "Homepage: https://github.com/cpplint/cpplint",
                                "Bugtracker: https://github.com/cpplint/cpplint/issues",
                                "Section: devel/python",
                                "License: BSD-3-Clause",
                                "Version: 1.5.5",
                                "Revision: r0",
                                "Layer: meta-shift",
                                "Testable: False")


def test_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.json")
        o = bare_build.shell.execute("recipetool inspect cpplint --output {}".format(temp))
        assert not o.stdout.contains('"Name": "cpplint"')
        with open(temp, "r") as f:
            data = json.load(f)
            assert data["General Information"]["Name"] == "cpplint"
    finally:
        shutil.rmtree(d)


def test_inspect_unknown_recipe(bare_build):
    o = bare_build.shell.execute("recipetool inspect unknown-recipe")
    assert o.stderr.contains("Failed to find the recipe file for 'unknown-recipe'")


def test_inspect_unknown_recipe_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.json")
        o = bare_build.shell.execute("recipetool inspect unknown-recipe --output {}".format(temp))
        assert not os.path.exists(temp)
    finally:
        shutil.rmtree(d)


def test_cmake_project_without_test_enabled(release_build):
    o = release_build.shell.execute("recipetool inspect cmake-project")
    assert o.stdout.containsAll("Name: cmake-project",
                                "Layer: meta-sample",
                                "Testable: False")


def test_cmake_project_with_test_enabled(test_build):
    o = test_build.shell.execute("recipetool inspect cmake-project")
    assert o.stdout.containsAll("Name: cmake-project",
                                "Layer: meta-sample",
                                "Testable: True")
