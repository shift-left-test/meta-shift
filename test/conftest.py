#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.build import Environment
import pytest
import shutil


BRANCH = "kirkstone"


@pytest.fixture(scope="session")
def release_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir, ignore_errors=True)
        shutil.rmtree(build_dir, ignore_errors=True)

    request.addfinalizer(cleanup)
    return Environment(branch=BRANCH, conf_file="conf/release.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def test_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir, ignore_errors=True)
        shutil.rmtree(build_dir, ignore_errors=True)

    request.addfinalizer(cleanup)
    return Environment(branch=BRANCH, conf_file="conf/test.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def report_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir, ignore_errors=True)
        shutil.rmtree(build_dir, ignore_errors=True)

    request.addfinalizer(cleanup)
    return Environment(branch=BRANCH, conf_file="conf/report.conf", repo_dir=repo_dir, build_dir=build_dir)
