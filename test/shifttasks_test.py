#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_build):
    return test_build.shell.execute("bitbake core-image-minimal -c listtasks").stdout


def test_do_checkcacheall(stdout):
    assert stdout.contains("do_checkcacheall")


def test_do_checkcodeall(stdout):
    assert stdout.contains("do_checkcodeall")


def test_do_checkrecipeall(stdout):
    assert stdout.contains("do_checkrecipeall")


def test_do_coverageall(stdout, release_build):
    assert stdout.contains("do_coverageall")
    o = release_build.shell.execute("bitbake core-image-minimal -c coverageall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


def test_do_reportall(stdout, release_build):
    assert stdout.contains("do_reportall")
    o = release_build.shell.execute("bitbake core-image-minimal -c reportall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_reportall: No recipes found to run 'do_report' task.")


def test_do_testall(stdout, release_build):
    assert stdout.contains("do_testall")
    o = release_build.shell.execute("bitbake core-image-minimal -c testall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_testall: No recipes found to run 'do_test' task.")
