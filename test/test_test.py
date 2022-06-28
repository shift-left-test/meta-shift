#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_core_image_minimal_do_report(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c report")
    assert o.stderr.contains("ERROR: Task do_report does not exist for target core-image-minimal")


def test_core_image_minimal_do_test(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target core-image-minimal")


def test_core_image_minimal_do_testall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c testall")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Started")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Succeeded")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")


def test_core_image_minimal_do_coverage(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target core-image-minimal")


def test_core_image_minimal_do_coverageall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c coverageall")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Succeeded")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report")


def test_core_image_minimal_do_checkcode(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkcodeall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkcodeall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")

    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_core_image_minimal_do_checkcache(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkcache")
    assert o.stderr.contains("ERROR: Task do_checkcache does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkcacheall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkcacheall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcache: Source Availability")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Source Availability")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcache: Source Availability")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcache: Source Availability")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcache: Source Availability")


def test_core_image_minimal_do_checkrecipe(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkrecipe")
    assert o.stderr.contains("ERROR: Task do_checkrecipe does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkrecipeall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkrecipeall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")


def test_cmake_project_do_build(test_build):
    assert test_build.shell.execute("bitbake cmake-project").stderr.empty()

    project = test_build.parse("cmake-project")
    assert project.packages.contains("cmake-native")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")
    assert project.packages.contains("oelint-adv-native")


def test_qmake_project_do_build(test_build):
    assert test_build.shell.execute("bitbake qmake-project").stderr.empty()

    project = test_build.parse("qmake-project")
    assert project.packages.contains("qtbase")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")
    assert project.packages.contains("oelint-adv-native")


def test_autotools_project_do_build(test_build):
    assert test_build.shell.execute("bitbake autotools-project").stderr.empty()

    project = test_build.parse("autotools-project")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")
    assert project.packages.contains("oelint-adv-native")


def test_cmake_project_for_static_analysis_do_compile(test_build):
    o = test_build.shell.execute("bitbake cmake-project-for-static-analysis -c compile")
    assert o.stdout.contains("Missing space before {  [whitespace/braces]")  # by cpplint
    assert o.returncode != 0
