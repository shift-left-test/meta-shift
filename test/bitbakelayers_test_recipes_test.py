#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 LG Electronics, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import pytest


def test_show_recipes(test_build):
    o = test_build.shell.execute("recipetool test-recipes")
    assert o.stdout.containsAll("autotools-project              1.0.0                meta-sample",
                                "cmake-project                  1.0.0                meta-sample",
                                "humidifier-project             1.0.0                meta-sample",
                                "qmake-project                  1.0.0                meta-sample",
                                "sqlite3wrapper                 0.1.0                meta-sample",
                                "stringutils                    0.0.1                meta-sample")


def test_show_no_recipes_without_test_enabled(release_build):
    o = release_build.shell.execute("recipetool test-recipes")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake-project",
                                    "sqlite3wrapper",
                                    "stringutils")


def test_show_recipes_with_pnspec(test_build):
    o = test_build.shell.execute("recipetool test-recipes *-project")
    assert o.stdout.containsAll("autotools-project              1.0.0                meta-sample",
                                "cmake-project                  1.0.0                meta-sample",
                                "humidifier-project             1.0.0                meta-sample",
                                "qmake-project                  1.0.0                meta-sample")
    assert not o.stdout.containsAll("sqlite3wrapper                 0.1.0                meta-sample",
                                    "stringutils                    0.0.1                meta-sample")


def test_show_no_recipes_without_test_enabled(release_build):
    o = release_build.shell.execute("recipetool test-recipes *-project")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake-project",
                                    "sqlite3wrapper",
                                    "stringutils")
