#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import json
import shutil
import tempfile


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
    d = tempfile.mkdtemp()
    try:
        report_file_path = os.path.join(d, "cmake-native_cache_check.json")
        release_build.shell.execute("devtool cache cmake-native -o=%s" % report_file_path)

        with open(report_file_path) as f:
            data = json.load(f)
            for title in ["Shared State", "Premirror"]:
                assert isinstance(data[title]["Summary"]["Wanted"], int)
                assert isinstance(data[title]["Summary"]["Found"], int)
                assert isinstance(data[title]["Summary"]["Missed"], int)
                assert isinstance(data[title]["Found"], list)
                assert isinstance(data[title]["Missed"], list)
    finally:
        shutil.rmtree(d)


def test_cache_save_as_file_with_unknown_cmd_option(release_build):
    d = tempfile.mkdtemp()
    try:
        report_file_path = os.path.join(d, "cmake-native_cache_check.json")
        o = release_build.shell.execute("devtool cache cmake-native -c unknown_task -o=%s" % report_file_path)
        assert o.stderr.contains("ERROR: Task do_unknown_task does not exist")
        assert not os.path.exists(report_file_path)
    finally:
        shutil.rmtree(d)


def test_cache_save_as_file_with_known_cmd_option(release_build):
    d = tempfile.mkdtemp()
    try:
        report_file_path = os.path.join(d, "cmake-native_configure_cache_check.json")
        release_build.shell.execute("devtool cache cmake-native -c configure -o=%s" % report_file_path)

        with open(report_file_path) as f:
            data = json.load(f)
            for title in ["Shared State", "Premirror"]:
                assert isinstance(data[title]["Summary"]["Wanted"], int)
                assert isinstance(data[title]["Summary"]["Found"], int)
                assert isinstance(data[title]["Summary"]["Missed"], int)
                assert isinstance(data[title]["Found"], list)
                assert isinstance(data[title]["Missed"], list)
    finally:
        shutil.rmtree(d)
