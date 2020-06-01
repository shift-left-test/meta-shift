#!/usr/bin/python

import constants
import pytest
import unittest
import yocto


class core_image_minimal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.RELEASE)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/installed-packages.txt")
        assert files.containsAll("cmake-project-1.0.0-r0.aarch64.rpm",
                                 "qmake5-project-1.0.0-r0.aarch64.rpm",
                                 "autotools-project-1.0.0-r0.aarch64.rpm",
                                 "sqlite3logger-1.0.0-r0.aarch64.rpm",
                                 "libsqlite3wrapper0-0.1.0-r0.aarch64.rpm")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c checkcode")
        assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c checkcodeall")
        assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c test")
        assert o.stderr.contains("ERROR: Task do_test does not exist for target core-image-minimal")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c testall")
        assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_testall: No recipes found to run 'do_test' task.")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverage")
        assert o.stderr.contains("ERROR: Task do_coverage does not exist for target core-image-minimal")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert o.stdout.contains("WARNING: core-image-minimal-1.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")


class cmake_project(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.RELEASE)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake cmake-project").stderr.empty()

        project = self.build.parse("cmake-project")
        assert project.packages.contains("cmake-native")
        assert not project.packages.containsAny("gtest", "googletest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cmake-project -c test")
        assert o.stderr.contains("ERROR: Task do_test does not exist for target cmake-project")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cmake-project -c testall")
        assert o.stdout.contains("WARNING: cmake-project-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cmake-project -c coverage")
        assert o.stderr.contains("ERROR: Task do_coverage does not exist for target cmake-project")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cmake-project -c coverageall")
        assert o.stdout.contains("WARNING: cmake-project-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake cmake-project -c checkcode")
        assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target cmake-project")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake cmake-project -c checkcodeall")
        assert o.stdout.contains("WARNING: cmake-project-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


class sqlite3logger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.RELEASE)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake sqlite3logger").stderr.empty()

        project = self.build.parse("sqlite3logger")
        assert project.packages.contains("cmake-native")
        assert project.packages.contains("stringutils")
        assert project.packages.contains("sqlite3wrapper")
        assert not project.packages.containsAny("gtest", "googletest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c test")
        assert o.stderr.contains("ERROR: Task do_test does not exist for target sqlite3logger")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c testall")
        assert o.stdout.contains("WARNING: sqlite3logger-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverage")
        assert o.stderr.contains("ERROR: Task do_coverage does not exist for target sqlite3logger")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverageall")
        assert o.stdout.contains("WARNING: sqlite3logger-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c checkcode")
        assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target sqlite3logger")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c checkcodeall")
        assert o.stdout.contains("WARNING: sqlite3logger-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


class qmake5_project5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.RELEASE)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake qmake5-project").stderr.empty()

        project = self.build.parse("qmake5-project")
        assert project.packages.contains("qtbase")
        assert not project.packages.contains("lcov-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake qmake5-project -c test")
        assert o.stderr.contains("ERROR: Task do_test does not exist for target qmake5-project")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake qmake5-project -c testall")
        assert o.stdout.contains("WARNING: qmake5-project-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake qmake5-project -c coverage")
        assert o.stderr.contains("ERROR: Task do_coverage does not exist for target qmake5-project")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake qmake5-project -c coverageall")
        assert o.stdout.contains("WARNING: qmake5-project-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake qmake5-project -c checkcode")
        assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target qmake5-project")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake qmake5-project -c checkcodeall")
        assert o.stdout.contains("WARNING: qmake5-project-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


class autotools_project(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.RELEASE)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake autotools-project").stderr.empty()

        project = self.build.parse("autotools-project")
        assert not project.packages.contains("lcov-native")
        assert not project.packages.containsAny("gtest", "googletest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake autotools-project -c test")
        assert o.stderr.contains("ERROR: Task do_test does not exist for target autotools-project")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake autotools-project -c testall")
        assert o.stdout.contains("WARNING: autotools-project-1.0.0-r0 do_testall: No recipes found to run 'do_test' task.")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake autotools-project -c coverage")
        assert o.stderr.contains("ERROR: Task do_coverage does not exist for target autotools-project")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake autotools-project -c coverageall")
        assert o.stdout.contains("WARNING: autotools-project-1.0.0-r0 do_coverageall: No recipes found to run 'do_coverage' task.")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake autotools-project -c checkcode")
        assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target autotools-project")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake autotools-project -c checkcodeall")
        assert o.stdout.contains("WARNING: autotools-project-1.0.0-r0 do_checkcodeall: No recipes found to run 'do_checkcode' task.")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
