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

import os
import json
import shutil
import tempfile


def test_unknown_recipe(bare_build):
    o = bare_build.shell.execute("devtool cache unknown-recipe")
    assert o.stdout.contains("ERROR: Nothing PROVIDES 'unknown-recipe'")


def test_cache(bare_build):
    o = bare_build.shell.execute("devtool cache cmake-native")
    assert o.stdout.matches(r"Wanted : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Found  : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Missed : [0-9]+ \([0-9]+%\)")


def test_cache_with_details(bare_build):
    o = bare_build.shell.execute("devtool cache cmake-native --found --missed")
    assert o.stdout.containsAll("cmake-native:do_populate_lic",
                                "cmake-native:do_populate_sysroot",
                                "cmake-native")


def test_cache_with_unknown_cmd_option(bare_build):
    o = bare_build.shell.execute("devtool cache cmake-native -c unknown_task")
    assert o.stdout.contains("ERROR: Task do_unknown_task does not exist")


def test_cache_with_known_cmd_option(bare_build):
    o = bare_build.shell.execute("devtool cache cmake-native -c configure")
    assert o.stdout.matches(r"Wanted : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Found  : [0-9]+ \([0-9]+%\)")
    assert o.stdout.matches(r"Missed : [0-9]+ \([0-9]+%\)")


def test_cache_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        report_file_path = os.path.join(d, "cmake-native_cache_check.json")
        bare_build.shell.execute("devtool cache cmake-native -o=%s" % report_file_path)

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


def test_cache_save_as_file_with_unknown_cmd_option(bare_build):
    d = tempfile.mkdtemp()
    try:
        report_file_path = os.path.join(d, "cmake-native_cache_check.json")
        o = bare_build.shell.execute("devtool cache cmake-native -c unknown_task -o=%s" % report_file_path)
        assert o.stdout.contains("ERROR: Task do_unknown_task does not exist")
        assert not os.path.exists(report_file_path)
    finally:
        shutil.rmtree(d)


def test_cache_save_as_file_with_known_cmd_option(bare_build):
    d = tempfile.mkdtemp()
    try:
        report_file_path = os.path.join(d, "cmake-native_configure_cache_check.json")
        bare_build.shell.execute("devtool cache cmake-native -c configure -o=%s" % report_file_path)

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

