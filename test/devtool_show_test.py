#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

def test_show_global_unknown_variable(bare_build):
    o = bare_build.shell.execute("devtool show UNKNOWN_VARIABLE")
    assert o.stderr.contains("WARNING: Requested variable 'UNKNOWN_VARIABLE' does not exist")


def test_show_global_variables(bare_build):
    o = bare_build.shell.execute("devtool show TUNE_ARCH BUILD_ARCH")
    assert o.stdout.matchesAll(r'BUILD_ARCH=".+"',
                               r'TUNE_ARCH=".+"')

def test_show_global_unexpanded_variables(bare_build):
    o = bare_build.shell.execute("devtool show MACHINE_ARCH -u")
    assert o.stdout.contains("# MACHINE_ARCH=${@[d.getVar('TUNE_PKGARCH'), d.getVar('MACHINE')][bool(d.getVar('MACHINE'))].replace('-', '_')}")


def test_show_global_variable_flags(bare_build):
    o = bare_build.shell.execute("devtool show BUILD_ARCH -f")
    assert o.stdout.contains('BUILD_ARCH[doc]="The name of the building architecture (e.g. i686)."')


def test_show_unknown_recipe(bare_build):
    o = bare_build.shell.execute("devtool show -r UNKNOWN_RECIPE TUNE_ARCH")
    assert o.stderr.contains("ERROR: Failed to find the recipe file for 'UNKNOWN_RECIPE'")


def test_show_recipe_unknown_variable(bare_build):
    o = bare_build.shell.execute("devtool show -r cmake UNKNOWN_VARIABLE")
    assert o.stderr.contains("WARNING: Requested variable 'UNKNOWN_VARIABLE' does not exist")


def test_show_recipe_variable(bare_build):
    o = bare_build.shell.execute("devtool show -r cmake cmake_do_configure")
    assert not o.stdout.contains("bbnote () {")
    assert o.stdout.contains("cmake_do_configure () {")


def test_show_recipe_dependent_variables(bare_build):
    o = bare_build.shell.execute("devtool show -r cmake cmake_do_configure -x")
    assert o.stdout.contains("bbnote () {")
    assert o.stdout.contains("cmake_do_configure () {")
