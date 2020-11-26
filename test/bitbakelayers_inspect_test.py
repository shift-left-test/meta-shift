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
import pytest
import shutil
import tempfile


def test_default_format(bare_build):
    o = bare_build.shell.execute("bitbake-layers inspect meta-poky")
    assert o.stdout.containsAll("General Information",
                                "-------------------",
                                "Layer: meta-poky",
                                "Name: yocto",
                                "Path:",
                                "Conf:",
                                "Priority: 5",
                                "Version: 3",
                                "Compatibilities:",
                                "Dependencies: core",
                                "Additional Information",
                                "----------------------",
                                "Images:",
                                "Machines:",
                                "Distros:",
                                "Classes:")


def test_default_format_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.plain")
        o = bare_build.shell.execute("bitbake-layers inspect meta-poky --output {}".format(temp))
        assert not o.stdout.contains("Name: yocto")
        with open(temp, "r") as f:
            assert "Name: yocto" in f.read()
    finally:
        shutil.rmtree(d)


def test_json_format(bare_build):
    o = bare_build.shell.execute("bitbake-layers inspect meta-poky --json")
    assert o.stdout.containsAll('"General Information": {{',
                                '"Layer": "meta-poky"',
                                '"Name": "yocto"',
                                '"Path":',
                                '"Conf":',
                                '"Priority": "5"',
                                '"Version": "3"',
                                '"Compatibilities":',
                                '"Dependencies": "core"',
                                '"Additional Information": {{',
                                '"Images": []',
                                '"Machines": []',
                                '"Distros": [',
                                '"Classes": [')


def test_json_format_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.json")
        o = bare_build.shell.execute("bitbake-layers inspect meta-poky --json --output {}".format(temp))
        assert not o.stdout.contains('"Name": "yocto"')
        with open(temp, "r") as f:
            data = json.load(f)
            assert data["General Information"]["Name"] == "yocto"
    finally:
        shutil.rmtree(d)


def test_inspect_unknown_layer(bare_build):
    o = bare_build.shell.execute("bitbake-layers inspect unknown-layer")
    assert o.stderr.contains("Specified layer 'unknown-layer' doesn't exist")


def test_inspect_unknown_layer_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.plain")
        o = bare_build.shell.execute("bitbake-layers inspect unknown-layer --output {}".format(temp))
        assert not os.path.exists(temp)
    finally:
        shutil.rmtree(d)
