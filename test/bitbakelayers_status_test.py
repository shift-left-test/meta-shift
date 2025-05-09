#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

def test_default_format(release_build):
    o = release_build.shell.execute("bitbake-layers status")
    assert o.stdout.containsAll("Project Configuration",
                                "---------------------",
                                "Machine:",
                                "Codename:",
                                "Distro: poky",
                                "Parallelism: True",
                                "own-mirrors: ",
                                "Additional Information",
                                "----------------------",
                                "Images:",
                                "core-image-minimal",
                                "Machines:",
                                "qemuarm64",
                                "Distros:",
                                "poky")
