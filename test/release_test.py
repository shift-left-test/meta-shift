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


def test_core_image_minimal_do_checkcode(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")


def test_core_image_minimal_do_checkcodeall(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c checkcodeall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


def test_core_image_minimal_do_test(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target core-image-minimal")


def test_core_image_minimal_do_testall(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c testall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_testall: No recipes found to run 'do_test' task.")


def test_core_image_minimal_do_coverage(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target core-image-minimal")


def test_core_image_minimal_do_coverageall(release_build):
    o = release_build.shell.execute("bitbake core-image-minimal -c coverageall")
    assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


def test_cmake_project_do_build(release_build):
    assert release_build.shell.execute("bitbake cmake-project").stderr.empty()

    project = release_build.parse("cmake-project")
    assert project.packages.contains("cmake-native")
    assert not project.packages.containsAny("gtest", "googletest")


def test_cmake_project_do_test(release_build):
    o = release_build.shell.execute("bitbake cmake-project -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target cmake-project")


def test_cmake_project_do_testall(release_build):
    o = release_build.shell.execute("bitbake cmake-project -c testall")
    assert o.stdout.contains("WARNING: cmake-project-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")


def test_cmake_project_do_coverage(release_build):
    o = release_build.shell.execute("bitbake cmake-project -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target cmake-project")


def test_cmake_project_do_coverageall(release_build):
    o = release_build.shell.execute("bitbake cmake-project -c coverageall")
    assert o.stdout.contains("WARNING: cmake-project-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


def test_cmake_project_do_checkcode(release_build):
    o = release_build.shell.execute("bitbake cmake-project -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target cmake-project")


def test_cmake_project_do_checkcodeall(release_build):
    o = release_build.shell.execute("bitbake cmake-project -c checkcodeall")
    assert o.stdout.contains("WARNING: cmake-project-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


def test_qmake5_project_do_build(release_build):
    assert release_build.shell.execute("bitbake qmake5-project").stderr.empty()

    project = release_build.parse("qmake5-project")
    assert project.packages.contains("qtbase")
    assert not project.packages.contains("lcov-native")


def test_qmake5_project_do_test(release_build):
    o = release_build.shell.execute("bitbake qmake5-project -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target qmake5-project")


def test_qmake5_project_do_testall(release_build):
    o = release_build.shell.execute("bitbake qmake5-project -c testall")
    assert o.stdout.contains("WARNING: qmake5-project-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")


def test_qmake5_project_do_coverage(release_build):
    o = release_build.shell.execute("bitbake qmake5-project -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target qmake5-project")


def test_qmake5_project_do_coverageall(release_build):
    o = release_build.shell.execute("bitbake qmake5-project -c coverageall")
    assert o.stdout.contains("WARNING: qmake5-project-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


def test_qmake5_project_do_checkcode(release_build):
    o = release_build.shell.execute("bitbake qmake5-project -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target qmake5-project")


def test_qmake5_project_do_checkcodeall(release_build):
    o = release_build.shell.execute("bitbake qmake5-project -c checkcodeall")
    assert o.stdout.contains("WARNING: qmake5-project-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


def test_autotools_project_do_build(release_build):
    assert release_build.shell.execute("bitbake autotools-project").stderr.empty()

    project = release_build.parse("autotools-project")
    assert not project.packages.contains("lcov-native")
    assert not project.packages.containsAny("gtest", "googletest")


def test_autotools_project_do_test(release_build):
    o = release_build.shell.execute("bitbake autotools-project -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target autotools-project")


def test_autotools_project_do_testall(release_build):
    o = release_build.shell.execute("bitbake autotools-project -c testall")
    assert o.stdout.contains("WARNING: autotools-project-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")


def test_autotools_project_do_coverage(release_build):
    o = release_build.shell.execute("bitbake autotools-project -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target autotools-project")


def test_autotools_project_do_coverageall(release_build):
    o = release_build.shell.execute("bitbake autotools-project -c coverageall")
    assert o.stdout.contains("WARNING: autotools-project-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


def test_autotools_project_do_checkcode(release_build):
    o = release_build.shell.execute("bitbake autotools-project -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target autotools-project")


def test_autotools_project_do_checkcodeall(release_build):
    o = release_build.shell.execute("bitbake autotools-project -c checkcodeall")
    assert o.stdout.contains("WARNING: autotools-project-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


def test_humidifier_project_do_build(release_build):
    assert release_build.shell.execute("bitbake humidifier-project").stderr.empty()


def test_humidifier_project_do_test(release_build):
    o = release_build.shell.execute("bitbake humidifier-project -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target humidifier-project")


def test_humidifier_project_do_testall(release_build):
    o = release_build.shell.execute("bitbake humidifier-project -c testall")
    assert o.stdout.contains("WARNING: humidifier-project-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")


def test_humidifier_project_do_coverage(release_build):
    o = release_build.shell.execute("bitbake humidifier-project -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target humidifier-project")


def test_humidifier_project_do_coverageall(release_build):
    o = release_build.shell.execute("bitbake humidifier-project -c coverageall")
    assert o.stdout.contains("WARNING: humidifier-project-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


def test_humidifier_project_do_checkcode(release_build):
    o = release_build.shell.execute("bitbake humidifier-project -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target humidifier-project")


def test_humidifier_project_do_checkcodeall(release_build):
    o = release_build.shell.execute("bitbake humidifier-project -c checkcodeall")
    assert o.stdout.contains("WARNING: humidifier-project-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


def test_sqlite3logger_do_build(release_build):
    assert release_build.shell.execute("bitbake sqlite3logger").stderr.empty()

    project = release_build.parse("sqlite3logger")
    assert project.packages.contains("cmake-native")
    assert project.packages.contains("stringutils")
    assert project.packages.contains("sqlite3wrapper")
    assert not project.packages.containsAny("gtest", "googletest")


def test_sqlite3logger_do_test(release_build):
    o = release_build.shell.execute("bitbake sqlite3logger -c test")
    assert o.stderr.contains("ERROR: Task do_test does not exist for target sqlite3logger")


def test_sqlite3logger_do_testall(release_build):
    o = release_build.shell.execute("bitbake sqlite3logger -c testall")
    assert o.stdout.contains("WARNING: sqlite3logger-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")


def test_sqlite3logger_do_coverage(release_build):
    o = release_build.shell.execute("bitbake sqlite3logger -c coverage")
    assert o.stderr.contains("ERROR: Task do_coverage does not exist for target sqlite3logger")


def test_sqlite3logger_do_coverageall(release_build):
    o = release_build.shell.execute("bitbake sqlite3logger -c coverageall")
    assert o.stdout.contains("WARNING: sqlite3logger-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


def test_sqlite3logger_do_checkcode(release_build):
    o = release_build.shell.execute("bitbake sqlite3logger -c checkcode")
    assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target sqlite3logger")


def test_sqlite3logger_do_checkcodeall(release_build):
    o = release_build.shell.execute("bitbake sqlite3logger -c checkcodeall")
    assert o.stdout.contains("WARNING: sqlite3logger-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")
