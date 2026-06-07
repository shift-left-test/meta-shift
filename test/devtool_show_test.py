#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_show_global_unknown_variable(release_build):
    o = release_build.shell.execute("devtool show UNKNOWN_VARIABLE")
    assert o.stderr.contains("WARNING: Requested variable 'UNKNOWN_VARIABLE' does not exist")


def test_show_global_variables(release_build):
    o = release_build.shell.execute("devtool show TUNE_ARCH BUILD_ARCH")
    assert o.stdout.matchesAll(r'BUILD_ARCH=".+"',
                               r'TUNE_ARCH=".+"')


def test_show_global_unexpanded_variables(release_build):
    o = release_build.shell.execute("devtool show MACHINE_ARCH -u")
    # Assert the variable is rendered unexpanded (leading "# NAME=${@") without
    # binding to the exact upstream OE-core expression, which drifts by version.
    assert o.stdout.matches(r"^# MACHINE_ARCH=\$\{@")


def test_show_global_variable_flags(release_build):
    o = release_build.shell.execute("devtool show BUILD_ARCH -f")
    # Validate the flag-rendering (NAME[doc]="...") without pinning the exact
    # upstream doc string, which is OE-core-owned and version-dependent.
    assert o.stdout.matches(r'BUILD_ARCH\[doc\]=".+"')


def test_show_unknown_recipe(release_build):
    o = release_build.shell.execute("devtool show -r UNKNOWN_RECIPE TUNE_ARCH")
    assert o.stderr.contains("ERROR: Failed to find the recipe file for 'UNKNOWN_RECIPE'")


def test_show_recipe_unknown_variable(release_build):
    o = release_build.shell.execute("devtool show -r cmake UNKNOWN_VARIABLE")
    assert o.stderr.contains("WARNING: Requested variable 'UNKNOWN_VARIABLE' does not exist")


def test_show_recipe_variable(release_build):
    o = release_build.shell.execute("devtool show -r cmake cmake_do_configure")
    assert not o.stdout.contains("bbnote () {")
    assert o.stdout.contains("cmake_do_configure () {")


def test_show_recipe_dependent_variables(release_build):
    o = release_build.shell.execute("devtool show -r cmake cmake_do_configure -x")
    assert o.stdout.contains("bbnote () {")
    assert o.stdout.contains("cmake_do_configure () {")
