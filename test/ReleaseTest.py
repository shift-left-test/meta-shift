#!/usr/bin/python

import pytest
import unittest
import yocto

BRANCH = "morty"
CONFIG = "release.conf"


class core_image_minimal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/installed-packages.txt")
        assert files.containsAll("sample-project-1.0.0-r0.aarch64.rpm",
                                 "cpp-project-1.0.0-r0.aarch64.rpm",
                                 "cpp-project-qt5-1.0.0-r0.aarch64.rpm",
                                 "cpp-project-autotools-1.0.0-r0.aarch64.rpm",
                                 "sqlite3logger-1.0.0-r0.aarch64.rpm",
                                 "libsqlite3wrapper0-0.1.0-r0.aarch64.rpm")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target core-image-minimal")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c testall")
        assert o["stdout"].contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Started\n" \
                                    "NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target core-image-minimal")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert o["stdout"].contains("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Started\n" \
                                    "NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Succeeded\n")


class cpp_project(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake cpp-project").stderr.empty()

        project = self.build.parse("cpp-project")
        assert project.packages.contains("cmake-native")
        assert not project.packages.containsAny("gtest", "googletest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cpp-project -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target cpp-project")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cpp-project -c testall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-1.0.0-r0: task do_testall: Started\n" \
                                    "NOTE: recipe cpp-project-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cpp-project -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target cpp-project")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project -c coverageall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-1.0.0-r0: task do_coverageall: Started\n" \
                                    "NOTE: recipe cpp-project-1.0.0-r0: task do_coverageall: Succeeded")


class sqlite3logger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake sqlite3logger").stderr.empty()

        project = self.build.parse("sqlite3logger")
        assert project.packages.contains("cmake-native")
        assert project.packages.contains("stringutils")
        assert project.packages.contains("sqlite3wrapper")
        assert not project.packages.containsAny("gtest", "googletest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target sqlite3logger")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c testall")
        assert o["stdout"].contains("NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Started\n" \
                                    "NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target sqlite3logger")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverageall")
        assert o["stdout"].contains("NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Started\n" \
                                    "NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Succeeded")


class cpp_project_qt5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake cpp-project-qt5").stderr.empty()

        project = self.build.parse("cpp-project-qt5")
        assert project.packages.contains("qtbase")
        assert not project.packages.contains("lcov-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target cpp-project-qt5")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c testall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_testall: Started\n" \
                                    "NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target cpp-project-qt5")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverageall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_coverageall: Started\n" \
                                    "NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_coverageall: Succeeded")


class cpp_project_autotools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake cpp-project-autotools").stderr.empty()

        project = self.build.parse("cpp-project-autotools")
        assert not project.packages.contains("lcov-native")
        assert not project.packages.containsAny("gtest", "googletest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target cpp-project-autotools")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c testall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_testall: Started\n" \
                                    "NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target cpp-project-autotools")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c coverageall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_coverageall: Started\n" \
                                    "NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_coverageall: Succeeded")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
