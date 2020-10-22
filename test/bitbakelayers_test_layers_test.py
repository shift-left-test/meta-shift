#!/usr/bin/python

"""
MIT License

Copyright (c) 2020 Sung Gon Kim

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
import re


def test_mutually_exclusive_options(release_build):
    assert not release_build.shell.execute("recipetool test-layers --show --add").stderr.empty()
    assert not release_build.shell.execute("recipetool test-layers --show --remove").stderr.empty()
    assert not release_build.shell.execute("recipetool test-layers --add --remove").stderr.empty()


def test_default_action(release_build):
    o = release_build.shell.execute("recipetool test-layers")
    assert o.stdout.contains("meta-sample-test")


def test_show_layers(release_build):
    o = release_build.shell.execute("recipetool test-layers --show")
    assert o.stdout.contains("meta-sample-test")


def test_show_with_basepath(release_build):
    o = release_build.shell.execute("recipetool test-layers --show --basepath /dev/null")
    assert not o.stdout.contains("meta-sample-test")


def test_add_layers(release_build):
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    release_build.shell.execute("recipetool test-layers --add")
    assert release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    release_build.shell.execute("recipetool test-layers --remove")
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")


def test_add_layers_twice(release_build):
    release_build.shell.execute("recipetool test-layers --add")
    assert release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    o = release_build.shell.execute("recipetool test-layers --add")
    regexp = re.compile("Specified layer .+/meta-sample-test is already in BBLAYERS", re.MULTILINE)
    assert bool(re.match(regexp, o.stderr.output))
    release_build.shell.execute("recipetool test-layers --remove")


def test_remove_layers(release_build):
    release_build.shell.execute("recipetool test-layers --add")
    assert release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    release_build.shell.execute("recipetool test-layers --remove")
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")


def test_remove_layers_twice(release_build):
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    o = release_build.shell.execute("recipetool test-layers --remove")
    regexp = re.compile("No layers matching .+/meta-sample-test found in BBLAYERS", re.MULTILINE)
    assert bool(re.match(regexp, o.stderr.output))
