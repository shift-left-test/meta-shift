#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
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


def test_json_format_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.json")
        o = bare_build.shell.execute("bitbake-layers inspect meta-poky --output {}".format(temp))
        assert not o.stdout.contains('"Name": "yocto"')
        with open(temp, "r") as f:
            data = json.load(f)
            assert data["General Information"]["Name"] == "yocto"
            assert data["General Information"]["Layer"] == "meta-poky"
            assert data["General Information"]["Priority"] == "5"
            assert data["General Information"]["Version"] == "3"
            assert data["General Information"]["Dependencies"] == "core"
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
