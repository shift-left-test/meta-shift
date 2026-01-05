#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_default_format(release_build):
    o = release_build.shell.execute("bitbake-layers inspect meta")
    assert o.stdout.containsAll("General Information",
                                "-------------------",
                                "Layer: meta",
                                "Name: core",
                                "Path:",
                                "Conf:",
                                "Priority: 5",
                                "Compatibilities:",
                                "Dependencies:",
                                "Additional Information",
                                "----------------------",
                                "Images:",
                                "Machines:")


def test_json_format_save_as_file(release_build):
    with release_build.files.tempfile("report.json") as f:
        o = release_build.shell.execute("bitbake-layers inspect meta --output {}".format(f))
        assert not o.stdout.contains('"Name": "core"')
        with release_build.files.readAsJson("report.json") as data:
            assert data["General Information"]["Name"] == "core"
            assert data["General Information"]["Layer"] == "meta"
            assert data["General Information"]["Priority"] == "5"


def test_inspect_unknown_layer(release_build):
    o = release_build.shell.execute("bitbake-layers inspect unknown-layer")
    assert o.stderr.contains("Specified layer 'unknown-layer' doesn't exist")


def test_inspect_unknown_layer_save_as_file(release_build):
    with release_build.files.tempfile("report.json") as f:
        o = release_build.shell.execute("bitbake-layers inspect unknown-layer --output {}".format(f))
        assert not release_build.files.exists("report.json")
