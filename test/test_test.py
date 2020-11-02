#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 Sung Gon Kim

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


def test_core_image_minimal_do_test(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target core-image-minimal")


def test_core_image_minimal_do_testall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c testall")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Started")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Succeeded")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_test: Running tests...")


def test_core_image_minimal_do_coverage(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target core-image-minimal")


def test_core_image_minimal_do_coverageall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c coverageall")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Succeeded")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_test: Running tests...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report")


def test_core_image_minimal_do_checkcode(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkcodeall(test_build):
    o = test_build.shell.execute("bitbake core-image-minimal -c checkcodeall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_cmake_project_do_build(test_build):
    assert test_build.shell.execute("bitbake cmake-project").stderr.empty()

    project = test_build.parse("cmake-project")
    assert project.packages.contains("cmake-native")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python3-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")


def test_cmake_project_do_test(test_build):
    o = test_build.shell.execute("bitbake cmake-project -c test")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")


def test_cmake_project_do_testall(test_build):
    o = test_build.shell.execute("bitbake cmake-project -c testall")
    assert o.stdout.contains("NOTE: recipe cmake-project-1.0.0-r0: task do_testall: Started")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("NOTE: recipe cmake-project-1.0.0-r0: task do_testall: Succeeded")


def test_cmake_project_do_coverage(test_build):
    o = test_build.shell.execute("bitbake cmake-project -c coverage")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_cmake_project_do_coverageall(test_build):
    o = test_build.shell.execute("bitbake cmake-project -c coverageall")
    assert o.stdout.contains("NOTE: recipe cmake-project-1.0.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("NOTE: recipe cmake-project-1.0.0-r0: task do_coverageall: Succeeded")


def test_cmake_project_do_checkcode(test_build):
    o = test_build.shell.execute("bitbake cmake-project -c checkcode")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_cmake_project_do_checkcodeall(test_build):
    o = test_build.shell.execute("bitbake cmake-project -c checkcodeall")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("cmake-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_qmake5_project_do_build(test_build):
    assert test_build.shell.execute("bitbake qmake5-project").stderr.empty()

    project = test_build.parse("qmake5-project")
    assert project.packages.contains("qtbase")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python3-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")


def test_qmake5_project_do_test(test_build):
    o = test_build.shell.execute("bitbake qmake5-project -c test")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")


def test_qmake5_project_do_testall(test_build):
    o = test_build.shell.execute("bitbake qmake5-project -c testall")
    assert o.stdout.contains("NOTE: recipe qmake5-project-1.0.0-r0: task do_testall: Started")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("NOTE: recipe qmake5-project-1.0.0-r0: task do_testall: Succeeded")


def test_qmake5_project_do_coverage(test_build):
    o = test_build.shell.execute("bitbake qmake5-project -c coverage")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_qmake5_project_do_coverageall(test_build):
    o = test_build.shell.execute("bitbake qmake5-project -c coverageall")
    assert o.stdout.contains("NOTE: recipe qmake5-project-1.0.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("NOTE: recipe qmake5-project-1.0.0-r0: task do_coverageall: Succeeded")


def test_qmake5_project_do_checkcode(test_build):
    o = test_build.shell.execute("bitbake qmake5-project -c checkcode")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_qmake5_project_do_checkcodeall(test_build):
    o = test_build.shell.execute("bitbake qmake5-project -c checkcodeall")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("qmake5-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_autotools_project_do_build(test_build):
    assert test_build.shell.execute("bitbake autotools-project").stderr.empty()

    project = test_build.parse("autotools-project")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python3-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")


def test_autotools_project_do_test(test_build):
    o = test_build.shell.execute("bitbake autotools-project -c test")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")


def test_autotools_project_do_testall(test_build):
    o = test_build.shell.execute("bitbake autotools-project -c testall")
    assert o.stdout.contains("NOTE: recipe autotools-project-1.0.0-r0: task do_testall: Started")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("NOTE: recipe autotools-project-1.0.0-r0: task do_testall: Succeeded")


def test_autotools_project_do_coverage(test_build):
    o = test_build.shell.execute("bitbake autotools-project -c coverage")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_autotools_project_do_coverageall(test_build):
    o = test_build.shell.execute("bitbake autotools-project -c coverageall")
    assert o.stdout.contains("NOTE: recipe autotools-project-1.0.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("NOTE: recipe autotools-project-1.0.0-r0: task do_coverageall: Succeeded")


def test_autotools_project_do_checkcode(test_build):
    o = test_build.shell.execute("bitbake autotools-project -c checkcode")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_autotools_project_do_checkcodeall(test_build):
    o = test_build.shell.execute("bitbake autotools-project -c checkcodeall")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("autotools-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_humidifier_project_do_build(test_build):
    assert test_build.shell.execute("bitbake humidifier-project").stderr.empty()

    project = test_build.parse("cmake-project")
    assert project.packages.contains("cmake-native")
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python3-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")
    assert project.packages.contains("sage-native")


def test_humidifier_project_do_test(test_build):
    o = test_build.shell.execute("bitbake humidifier-project -c test")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")


def test_humidifier_project_do_testall(test_build):
    o = test_build.shell.execute("bitbake humidifier-project -c testall")
    assert o.stdout.contains("NOTE: recipe humidifier-project-1.0.0-r0: task do_testall: Started")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("NOTE: recipe humidifier-project-1.0.0-r0: task do_testall: Succeeded")


def test_humidifier_project_do_coverage(test_build):
    o = test_build.shell.execute("bitbake humidifier-project -c coverage")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")


def test_humidifier_project_do_coverageall(test_build):
    o = test_build.shell.execute("bitbake humidifier-project -c coverageall")
    assert o.stdout.contains("NOTE: recipe humidifier-project-1.0.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_test: Running tests...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("NOTE: recipe humidifier-project-1.0.0-r0: task do_coverageall: Succeeded")


def test_humidifier_project_do_checkcode(test_build):
    o = test_build.shell.execute("bitbake humidifier-project -c checkcode")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_humidifier_project_do_checkcodeall(test_build):
    o = test_build.shell.execute("bitbake humidifier-project -c checkcodeall")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("humidifier-project-1.0.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")


def test_sqlite3logger_do_build(test_build):
    assert test_build.shell.execute("bitbake sqlite3logger").stderr.empty()

    project = test_build.parse("sqlite3logger")
    assert project.packages.contains("cmake-native")
    assert project.packages.contains("stringutils")
    assert project.packages.contains("sqlite3wrapper")

    # List of indirectly dependent packages
    assert project.packages.containsAny("gtest", "googletest")
    assert project.packages.contains("cppcheck-native")
    assert project.packages.contains("cpplint-native")
    assert project.packages.contains("lcov-native")
    assert project.packages.contains("python3-lcov-cobertura-native")
    assert project.packages.contains("qemu-native")


def test_sqlite3logger_do_test(test_build):
    o = test_build.shell.execute("bitbake sqlite3logger -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target sqlite3logger")


def test_sqlite3logger_do_testall(test_build):
    o = test_build.shell.execute("bitbake sqlite3logger -c testall")
    assert o.stdout.contains("NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Started")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_test: Running tests...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")
    assert o.stdout.contains("NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Succeeded")


def test_sqlite3logger_do_coverage(test_build):
    o = test_build.shell.execute("bitbake sqlite3logger -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target sqlite3logger")


def test_sqlite3logger_do_coverageall(test_build):
    o = test_build.shell.execute("bitbake sqlite3logger -c coverageall")
    assert o.stdout.contains("NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Started")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_test: Running tests...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_test: Running tests...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report")
    assert o.stdout.contains("NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Succeeded")


def test_sqlite3logger_do_checkcode(test_build):
    o = test_build.shell.execute("bitbake sqlite3logger -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target sqlite3logger")


def test_sqlite3logger_do_checkcodeall(test_build):
    o = test_build.shell.execute("bitbake sqlite3logger -c checkcodeall")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("stringutils-0.0.1-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cppcheck is running...")
    assert o.stdout.contains("sqlite3wrapper-0.1.0-r0 do_checkcode: INFO:SAGE:* cpplint is running...")
