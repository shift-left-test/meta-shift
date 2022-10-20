#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_unknown_recipe(release_build):
    o = release_build.shell.execute("devtool cache unknown-recipe")
    assert o.stderr.contains("ERROR: Nothing PROVIDES 'unknown-recipe'")


def test_cache(release_build):
    o = release_build.shell.execute("devtool cache cmake-native")
    assert o.stdout.matches(r"Wanted : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Found  : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Missed : [0-9]+ \([0-9]+%\)")


def test_cache_with_details(release_build):
    o = release_build.shell.execute("devtool cache cmake-native --found --missed")
    assert o.stdout.containsAll("cmake-native:do_populate_lic",
                                "cmake-native:do_populate_sysroot",
                                "cmake-native")


def test_cache_with_unknown_cmd_option(release_build):
    o = release_build.shell.execute("devtool cache cmake-native -c unknown_task")
    assert o.stderr.contains("ERROR: Task do_unknown_task does not exist")


def test_cache_with_known_cmd_option(release_build):
    o = release_build.shell.execute("devtool cache cmake-native -c configure")
    assert o.stdout.matches(r"Wanted : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Found  : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Missed : [0-9]+ \([0-9]+%\)")


def test_cache_save_as_file(release_build):
    with release_build.files.tempfile("report.json") as f:
        release_build.shell.execute("devtool cache cmake-native -o=%s" % f)
        with release_build.files.readAsJson("report.json") as data:
            for title in ["Shared State", "Premirror"]:
                assert isinstance(data[title]["Summary"]["Wanted"], int)
                assert isinstance(data[title]["Summary"]["Found"], int)
                assert isinstance(data[title]["Summary"]["Missed"], int)
                assert isinstance(data[title]["Found"], list)
                assert isinstance(data[title]["Missed"], list)


def test_cache_save_as_file_with_unknown_cmd_option(release_build):
    with release_build.files.tempfile("report.json") as f:
        o = release_build.shell.execute("devtool cache cmake-native -c unknown_task -o=%s" % f)
        assert o.stderr.contains("ERROR: Task do_unknown_task does not exist")
        assert not release_build.files.exists(f)


def test_cache_save_as_file_with_known_cmd_option(release_build):
    with release_build.files.tempfile("report.json") as f:
        release_build.shell.execute("devtool cache cmake-native -c configure -o=%s" % f)
        with release_build.files.readAsJson("report.json") as data:
            for title in ["Shared State", "Premirror"]:
                assert isinstance(data[title]["Summary"]["Wanted"], int)
                assert isinstance(data[title]["Summary"]["Found"], int)
                assert isinstance(data[title]["Summary"]["Missed"], int)
                assert isinstance(data[title]["Found"], list)
                assert isinstance(data[title]["Missed"], list)

