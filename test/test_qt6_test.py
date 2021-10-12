#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 LG Electronics, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import pytest


def test_core_image_minimal_do_test(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target core-image-minimal")


def test_core_image_minimal_do_testall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c testall")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Started")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Succeeded")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_test: Running tests...")


def test_core_image_minimal_do_coverage(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target core-image-minimal")


def test_core_image_minimal_do_coverageall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c coverageall")
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
    assert o.stdout.contains("stringutils-0.0.1-r0 do_test: Running tests...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report")


def test_core_image_minimal_do_checkcode(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkcodeall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c checkcodeall")
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

    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_core_image_minimal_do_checkcache(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c checkcache")
    assert o.stderr.contains("ERROR: Task do_checkcache does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkcacheall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c checkcacheall")
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
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcache: Source Availability")


def test_core_image_minimal_do_checkrecipe(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c checkrecipe")
    assert o.stderr.contains("ERROR: Task do_checkrecipe does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkrecipeall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake core-image-minimal -c checkrecipeall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkrecipe: INFO:oelint-adv:Done.")


def test_qmake_project_do_build(test_qt6_build):
    assert test_qt6_build.shell.execute("bitbake qmake-project").stderr.empty()

    project = test_qt6_build.parse("qmake-project")
    assert project.packages.contains("qtbase")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python3-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")
    assert project.packages.contains("oelint-adv-native")


def test_qmake_project_do_test(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c test")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")


def test_qmake_project_do_testall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c testall")
    assert o.stdout.contains("NOTE: recipe qmake-project-1.0.0-r0: task do_testall: Started")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("NOTE: recipe qmake-project-1.0.0-r0: task do_testall: Succeeded")


def test_qmake_project_do_coverage(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c coverage")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_qmake_project_do_coverageall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c coverageall")
    assert o.stdout.contains("NOTE: recipe qmake-project-1.0.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("NOTE: recipe qmake-project-1.0.0-r0: task do_coverageall: Succeeded")


def test_qmake_project_do_checkcode(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkcode")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_qmake_project_do_checkcodeall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkcodeall")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* metrix++ is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* duplo is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_qmake_project_do_checkcache(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkcache")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Source Availability")


def test_qmake_project_do_checkcacheall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkcacheall")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Shared State Availability")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkcache: Source Availability")


def test_qmake_project_do_checkrecipe(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkrecipe")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")


def test_qmake_project_do_checkrecipeall(test_qt6_build):
    o = test_qt6_build.shell.execute("bitbake qmake-project -c checkrecipeall")
    assert o.stdout.contains("qmake-project-1.0.0-r0 do_checkrecipe: INFO:oelint-adv:Done.")
