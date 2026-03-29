#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_default_format(release_build):
    o = release_build.shell.execute("recipetool inspect googletest")
    assert o.stdout.containsAll("General Information",
                                "-------------------",
                                "Name: googletest")


def test_save_as_file(release_build):
    with release_build.files.tempfile("report.json") as f:
        o = release_build.shell.execute("recipetool inspect googletest --output {}".format(f))
        assert not o.stdout.contains('"Name": "googletest"')
        with release_build.files.readAsJson("report.json") as data:
            assert data["General Information"]["Name"] == "googletest"


def test_inspect_recursive(release_build):
    o = release_build.shell.execute("recipetool inspect googletest --recursive")
    assert o.stdout.containsAll("Depends:",
                                "Indirect Depends:",
                                "Incoming Depends:",
                                "Indirect Incoming Depends:")


def test_inspect_unknown_recipe(release_build):
    o = release_build.shell.execute("recipetool inspect unknown-recipe")
    assert o.stderr.contains("Failed to find the recipe file for 'unknown-recipe'")


def test_inspect_unknown_recipe_save_as_file(release_build):
    with release_build.files.tempfile("report.json") as f:
        o = release_build.shell.execute("recipetool inspect unknown-recipe --output {}".format(f))
        assert not release_build.files.exists("report.json")


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
