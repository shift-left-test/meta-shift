#-*- coding: utf-8 -*-
#!/usr/bin/python3

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
