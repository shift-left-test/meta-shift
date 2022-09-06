#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_cmake_project_filter(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_FILTER", "PlusTest.*-*Fail:*AlsoFail")
        stdout = test_build.shell.execute("bitbake cmake-project -c test").stdout
        assert not stdout.containsAny(
            "PlusTest.testShouldFail",
            "MinusTest.testShouldReturnExpectedValue",
            "MinusTest.testShouldAlsoFail")


def test_qmake_project_filter(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_FILTER", "PlusTest.*-*Fail:*AlsoFail")
        stdout = test_build.shell.execute("bitbake qmake-project -c test").stdout
        assert not stdout.containsAny(
            "PlusTest.testShouldFail",
            "MinusTest.testShouldReturnExpectedValue",
            "MinusTest.testShouldAlsoFail")


def test_autotools_project_filter(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_FILTER", "PlusTest.*-*Fail:*AlsoFail")
        stdout = test_build.shell.execute("bitbake autotools-project -c test").stdout
        assert not stdout.containsAny(
            "PlusTest.testShouldFail",
            "MinusTest.testShouldReturnExpectedValue",
            "MinusTest.testShouldAlsoFail")


def test_do_test_shuffle_on(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SHUFFLE", "1")
        first = test_build.shell.execute("bitbake sqlite3wrapper -c test").stdout
        second = test_build.shell.execute("bitbake sqlite3wrapper -c test").stdout
        assert first != second


def test_do_test_suppress_failures_off(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_SUPPRESS_FAILURES", "0")
        o = test_build.shell.execute("bitbake cmake-project -c test")
        assert o.returncode != 0
