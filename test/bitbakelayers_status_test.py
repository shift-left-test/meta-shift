#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

def test_default_format(bare_build):
    o = bare_build.shell.execute("bitbake-layers status")
    assert o.stdout.containsAll("Project Configuration",
                                "---------------------",
                                "Machine:",
                                "Codename:",
                                "Distro: poky",
                                "Parallelism: True",
                                "own-mirrors: True",
                                "Additional Information",
                                "----------------------",
                                "Images:",
                                "core-image-minimal",
                                "Machines:",
                                "qemuarm64",
                                "raspberrypi",
                                "Distros:",
                                "poky")
