#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_show_recipes(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes")
    assert o.stdout.matchesAll("autotools-project[ ]+1.0.0[ ]+meta-sample",
                               "cmake-project[ ]+1.0.0[ ]+meta-sample",
                               "humidifier-project[ ]+1.0.0[ ]+meta-sample",
                               "qmake-project[ ]+1.0.0[ ]+meta-sample",
                               "sqlite3wrapper[ ]+0.1.0[ ]+meta-sample")


def test_show_no_recipes_without_test_enabled(release_build):
    o = release_build.shell.execute("bitbake-layers test-recipes")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake-project",
                                    "sqlite3wrapper")


def test_show_recipes_with_pnspec(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes *-project")
    assert o.stdout.matchesAll("autotools-project[ ]+1.0.0[ ]+meta-sample",
                               "cmake-project[ ]+1.0.0[ ]+meta-sample",
                               "humidifier-project[ ]+1.0.0[ ]+meta-sample",
                               "qmake-project[ ]+1.0.0[ ]+meta-sample")
    assert not o.stdout.matchesAll("sqlite3wrapper[ ]+0.1.0[ ]+meta-sample")


def test_show_no_recipes_without_test_enabled(release_build):
    o = release_build.shell.execute("bitbake-layers test-recipes *-project")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake-project",
                                    "sqlite3wrapper")


def test_show_no_untestable_recipes(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes")
    assert not o.stdout.matchesAny(r"nativesdk-.+-project", r".+-project-native")
