#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import glob
import json
import os


def test_verify_runs_under_externalsrc(test_build):
    # The shift tasks must still work when the recipe source is an external
    # (devtool-modified) tree rather than an unpacked SRC_URI.
    with test_build.externalsrc("cmake-project"):
        o = test_build.shell.execute("bitbake cmake-project -c verify")
        assert o.stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")


def test_report_metadata_under_externalsrc(test_build):
    # S must point at the externalsrc tree, not the unpacked SRC_URI location
    with test_build.externalsrc("cmake-project"):
        with test_build.files.conf() as conf:
            conf.set("SHIFT_REPORT_DIR", "${TOPDIR}/report")
            test_build.shell.execute("bitbake cmake-project -c test")
        matches = glob.glob(os.path.join(
            test_build.files.build_dir, "report/cmake-project-*/test/metadata.json"))
        assert matches
        with open(matches[0]) as f:
            data = json.load(f)
        assert data["S"].endswith("workspace/sources/cmake-project")
        assert os.path.isdir(data["S"])
    test_build.files.remove("report")
