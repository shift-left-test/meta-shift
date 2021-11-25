#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import json
import shutil
import tempfile
import pytest


def test_check(bare_build):
    o = bare_build.shell.execute("recipetool check cmake-native")
    o.stdout.contains("INFO: Checking the specified recipes or files for the styling issues...")
    o.stdout.contains(":warning:")
    o.stdout.contains("INFO: Done.")


def test_check_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.json")
        o = bare_build.shell.execute("recipetool check cmake-native --output {}".format(temp))
        with open(temp, "r") as f:
            data = json.load(f)
            assert isinstance(data["issues"], list)
            assert len(data["issues"]) > 0
            for issue in data["issues"]:
                assert isinstance(issue, dict)
                assert isinstance(issue["file"], str)
                assert isinstance(issue["line"], int)
                assert isinstance(issue["severity"], str)
                assert isinstance(issue["rule"], str)
                assert isinstance(issue["description"], str)
    finally:
        shutil.rmtree(d)
