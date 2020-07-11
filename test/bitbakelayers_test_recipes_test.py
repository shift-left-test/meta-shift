#!/usr/bin/python

import pytest


def test_show_recipes(test_build):
    o = test_build.shell.execute("recipetool test-recipes")
    assert o.stdout.containsAll("autotools-project              1.0.0                meta-sample",
                                "cmake-project                  1.0.0                meta-sample",
                                "humidifier-project             1.0.0                meta-sample",
                                "qmake5-project                 1.0.0                meta-sample",
                                "sqlite3wrapper                 0.1.0                meta-sample",
                                "stringutils                    0.0.1                meta-sample")


def test_show_no_recipes_without_test_enabled(release_build):
    o = release_build.shell.execute("recipetool test-recipes")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake5-project",
                                    "sqlite3wrapper",
                                    "stringutils")


def test_show_recipes_with_pnspec(test_build):
    o = test_build.shell.execute("recipetool test-recipes *-project")
    assert o.stdout.containsAll("autotools-project              1.0.0                meta-sample",
                                "cmake-project                  1.0.0                meta-sample",
                                "humidifier-project             1.0.0                meta-sample",
                                "qmake5-project                 1.0.0                meta-sample")
    assert not o.stdout.containsAll("sqlite3wrapper                 0.1.0                meta-sample",
                                    "stringutils                    0.0.1                meta-sample")


def test_show_no_recipes_without_test_enabled(release_build):
    o = release_build.shell.execute("recipetool test-recipes *-project")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake5-project",
                                    "sqlite3wrapper",
                                    "stringutils")
