#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.build import Environment
import pytest
import shutil


BRANCH = "master"


def _make_build(request, tmpdir_factory, conf_file):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir, ignore_errors=True)
        shutil.rmtree(build_dir, ignore_errors=True)

    request.addfinalizer(cleanup)
    try:
        return Environment(branch=BRANCH, conf_file=conf_file, repo_dir=repo_dir, build_dir=build_dir)
    except Exception as e:
        raise RuntimeError("Failed to set up workspace (branch={}, conf={}): {}".format(BRANCH, conf_file, e))


@pytest.fixture(scope="session")
def release_build(request, tmpdir_factory):
    return _make_build(request, tmpdir_factory, "conf/release.conf")


@pytest.fixture(scope="session")
def test_build(request, tmpdir_factory):
    return _make_build(request, tmpdir_factory, "conf/test.conf")


@pytest.fixture(scope="session")
def verify_build(request, tmpdir_factory):
    return _make_build(request, tmpdir_factory, "conf/verify.conf")


@pytest.fixture(scope="module")
def _verify_run(request, verify_build):
    # Run the consolidated verify once per module (keyed on the module's RECIPE)
    # and expose both the populated build env and the captured stdout, so the
    # report/stdout fixtures share a single bitbake invocation.
    recipe = request.module.RECIPE
    verify_build.files.remove("report")
    o = verify_build.shell.execute("bitbake {} -c verify".format(recipe))
    assert o.stderr.empty()
    return verify_build, o.stdout


@pytest.fixture(scope="module")
def report(_verify_run):
    return _verify_run[0]


@pytest.fixture(scope="module")
def stdout(_verify_run):
    return _verify_run[1]
