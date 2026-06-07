#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


def test_verify_runs_under_externalsrc(test_build):
    # The shift tasks must still work when the recipe source is an external
    # (devtool-modified) tree rather than an unpacked SRC_URI.
    with test_build.externalsrc("cmake-project"):
        o = test_build.shell.execute("bitbake cmake-project -c verify")
        assert o.stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")
