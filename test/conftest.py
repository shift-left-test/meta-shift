#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.build import Environment
import pytest
import shutil


BRANCH = "master"

# This is a workaround to avoid the following error in python 3.8
# "libgcc_s.so.1 must be installed for pthread_cancel to work"
# https://stackoverflow.com/questions/64797838/libgcc-s-so-1-must-be-installed-for-pthread-cancel-to-work
import ctypes
libgcc_s = ctypes.CDLL('libgcc_s.so.1')

@pytest.fixture(scope="session")
def release_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return Environment(branch=BRANCH, conf_file="conf/release.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def test_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return Environment(branch=BRANCH, conf_file="conf/test.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def report_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return Environment(branch=BRANCH, conf_file="conf/report.conf", repo_dir=repo_dir, build_dir=build_dir)
