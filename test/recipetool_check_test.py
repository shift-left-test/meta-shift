#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_check(release_build):
    o = release_build.shell.execute("recipetool check cmake-native")
    o.stdout.contains("INFO: Checking the specified recipes or files for the styling issues...")
    o.stdout.contains(":warning:")
    o.stdout.contains("INFO: Done.")


def test_check_save_as_file(release_build):
    with release_build.files.tempfile("report.json") as f:
        o = release_build.shell.execute("recipetool check cmake-native --output {}".format(f))
        with release_build.files.readAsJson("report.json") as data:
            assert isinstance(data["issues"], list)
            assert len(data["issues"]) > 0
            for issue in data["issues"]:
                assert isinstance(issue, dict)
                assert isinstance(issue["file"], str)
                assert isinstance(issue["line"], int)
                assert isinstance(issue["severity"], str)
                assert isinstance(issue["rule"], str)
                assert isinstance(issue["description"], str)
