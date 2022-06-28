#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest
import re


def test_mutually_exclusive_options(release_build):
    assert not release_build.shell.execute("recipetool test-layers --add --remove").stderr.empty()


def test_show_layers(release_build):
    o = release_build.shell.execute("recipetool test-layers --show")
    assert o.stdout.contains("meta-sample-test")


def test_show_layers_with_depth(release_build):
    o = release_build.shell.execute("recipetool test-layers --show --depth 0")
    assert not o.stdout.contains("meta-sample-test")


def test_show_with_basepath(release_build):
    o = release_build.shell.execute("recipetool test-layers --show --basepath /dev/null")
    assert not o.stdout.contains("meta-sample-test")


def test_add_layers(release_build):
    try:
        release_build.shell.execute("recipetool test-layers --add")
        assert release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    finally:
        release_build.shell.execute("recipetool test-layers --remove")


def test_remove_layers(release_build):
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
