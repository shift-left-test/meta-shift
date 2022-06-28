#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


@pytest.fixture(scope="module")
def stdout(test_build):
    return test_build.shell.execute("bitbake core-image-minimal -c reportall").stdout


def test_do_reportall_warning(stdout):
    assert stdout.contains("SHIFT_REPORT_DIR is not set. No reports will be generated.")


def test_core_image_minimal_do_testall(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")


def test_core_image_minimal_do_coverageall(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert stdout.contains("qmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert stdout.contains("autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report")


def test_core_image_minimal_do_checkcodeall(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_core_image_minimal_do_checkcacheall(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Source Availability")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkcache: Source Availability")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_checkcache: Source Availability")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcache: Shared State Availability")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcache: Source Availability")


def test_core_image_minimal_do_checkrecipeall(stdout):
    assert stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert stdout.contains("qmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert stdout.contains("autotools-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert stdout.contains("humidifier-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")


def test_cmake_project_do_build(test_build):
    stdout = test_build.shell.execute("bitbake cmake-project -e | grep ^DEPENDS=").stdout
    assert stdout.contains("cmake-native")
    assert stdout.containsAny("gtest", "googletest")
    assert stdout.contains("cppcheck-native")
    assert stdout.contains("cpplint-native")
    assert stdout.contains("lcov-native")
    assert stdout.contains("python3-lcov-cobertura-native")
    assert stdout.contains("qemu-native")
    assert stdout.contains("sage-native")
    assert stdout.contains("oelint-adv-native")


def test_qmake_project_do_build(test_build):
    stdout = test_build.shell.execute("bitbake qmake-project -e | grep ^DEPENDS=").stdout
    assert stdout.contains("qtbase")
    assert stdout.containsAny("gtest", "googletest")
    assert stdout.contains("cppcheck-native")
    assert stdout.contains("cpplint-native")
    assert stdout.contains("lcov-native")
    assert stdout.contains("python3-lcov-cobertura-native")
    assert stdout.contains("qemu-native")
    assert stdout.contains("sage-native")
    assert stdout.contains("oelint-adv-native")


def test_autotools_project_do_build(test_build):
    stdout = test_build.shell.execute("bitbake autotools-project -e | grep ^DEPENDS=").stdout
    assert stdout.containsAny("gtest", "googletest")
    assert stdout.contains("cppcheck-native")
    assert stdout.contains("cpplint-native")
    assert stdout.contains("lcov-native")
    assert stdout.contains("python3-lcov-cobertura-native")
    assert stdout.contains("qemu-native")
    assert stdout.contains("sage-native")
    assert stdout.contains("oelint-adv-native")


def test_cmake_project_for_static_analysis_do_compile(test_build):
    o = test_build.shell.execute("bitbake cmake-project-for-static-analysis -c compile")
    assert o.stdout.contains("Missing space before {  [whitespace/braces]")  # by cpplint
    assert o.returncode != 0
