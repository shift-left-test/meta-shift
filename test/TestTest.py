#!/usr/bin/python

import constants
import pytest
import unittest
import yocto


class core_image_minimal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/installed-packages.txt")
        assert files.containsAll("sample-project-1.0.0-r0.aarch64.rpm",
                                 "cpp-project-1.0.0-r0.aarch64.rpm",
                                 "cpp-project-qt5-1.0.0-r0.aarch64.rpm",
                                 "cpp-project-autotools-1.0.0-r0.aarch64.rpm",
                                 "sqlite3logger-1.0.0-r0.aarch64.rpm",
                                 "libsqlite3wrapper0-0.1.0-r0.aarch64.rpm")

        assert self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gtest/latest")
        assert self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gmock/latest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target core-image-minimal")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c testall")
        assert o["stdout"].containsAll("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Started",
                                       "cpp-project-1.0.0-r0 do_test: Running tests...",
                                       "sample-project-1.0.0-r0 do_test: Running tests...",
                                       "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                       "stringutils-0.0.1-r0 do_test: Running tests...",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                       "cpp-project-autotools-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                       "NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target core-image-minimal")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert o["stdout"].containsAll("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Started",
                                       "cpp-project-1.0.0-r0 do_test: Running tests...",
                                       "cpp-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "sample-project-1.0.0-r0 do_test: Running tests...",
                                       "sample-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                       "sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report",
                                       "stringutils-0.0.1-r0 do_test: Running tests...",
                                       "stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "cpp-project-autotools-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                       "cpp-project-autotools-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c checkcode")
        assert o["stderr"].contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c checkcodeall")
        assert o["stdout"].containsAll("cpp-project-qt5-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-qt5-1.0.0-r0 do_checkcode: * cpplint is running...",
                                       "sample-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "sample-project-1.0.0-r0 do_checkcode: * cpplint is running...",
                                       "cpp-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-1.0.0-r0 do_checkcode: * cpplint is running...",
                                       "sqlite3wrapper-0.1.0-r0 do_checkcode: * cppcheck is running...",
                                       "sqlite3wrapper-0.1.0-r0 do_checkcode: * cpplint is running...",
                                       "cpp-project-autotools-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-autotools-1.0.0-r0 do_checkcode: * cpplint is running...")


class cpp_project(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake cpp-project").stderr.empty()

        project = self.build.parse("cpp-project")
        assert project.packages.contains("cmake-native")
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("cppcheck-native")
        assert project.packages.contains("cpplint-native")
        assert project.packages.contains("lcov-native")
        assert project.packages.contains("python-lcov-cobertura-native")
        assert project.packages.contains("qemu-native")
        assert project.packages.contains("sage-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cpp-project -c test")
        assert o["stdout"].contains("cpp-project-1.0.0-r0 do_test: Running tests...")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cpp-project -c testall")
        assert o["stdout"].containsAll("NOTE: recipe cpp-project-1.0.0-r0: task do_testall: Started",
                                       "cpp-project-1.0.0-r0 do_test: Running tests...",
                                       "NOTE: recipe cpp-project-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cpp-project -c coverage")
        assert o["stdout"].containsAll("cpp-project-1.0.0-r0 do_test: Running tests...",
                                       "cpp-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project -c coverageall")
        assert o["stdout"].containsAll("NOTE: recipe cpp-project-1.0.0-r0: task do_coverageall: Started",
                                       "cpp-project-1.0.0-r0 do_test: Running tests...",
                                       "cpp-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "NOTE: recipe cpp-project-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake cpp-project -c checkcode")
        assert o["stdout"].containsAll("cpp-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-1.0.0-r0 do_checkcode: * cpplint is running...")


    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake cpp-project -c checkcodeall")
        assert o["stdout"].containsAll("cpp-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-1.0.0-r0 do_checkcode: * cpplint is running...")


class sqlite3logger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake sqlite3logger").stderr.empty()

        project = self.build.parse("sqlite3logger")
        assert project.packages.contains("cmake-native")
        assert project.packages.contains("stringutils")
        assert project.packages.contains("sqlite3wrapper")

        # List of indirectly dependent packages
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("cppcheck-native")
        assert project.packages.contains("cpplint-native")
        assert project.packages.contains("lcov-native")
        assert project.packages.contains("python-lcov-cobertura-native")
        assert project.packages.contains("qemu-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target sqlite3logger")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c testall")
        assert o["stdout"].containsAll("NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Started",
                                       "stringutils-0.0.1-r0 do_test: Running tests...",
                                       "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                       "NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target sqlite3logger")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverageall")
        assert o["stdout"].containsAll("NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Started",
                                       "stringutils-0.0.1-r0 do_test: Running tests...",
                                       "stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report",
                                       "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                       "sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report",
                                       "NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c checkcode")
        assert o["stderr"].containsAll("ERROR: Task do_checkcode does not exist for target sqlite3logger")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c checkcodeall")
        assert o["stdout"].containsAll("stringutils-0.0.1-r0 do_checkcode: * cppcheck is running...",
                                       "stringutils-0.0.1-r0 do_checkcode: * cpplint is running...",
                                       "sqlite3wrapper-0.1.0-r0 do_checkcode: * cppcheck is running...",
                                       "sqlite3wrapper-0.1.0-r0 do_checkcode: * cpplint is running...")


class cpp_project_qt5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_build(self):
        assert self.build.shell.execute("bitbake cpp-project-qt5").stderr.empty()

        project = self.build.parse("cpp-project-qt5")
        assert project.packages.contains("qtbase")
        assert project.packages.contains("lcov-native")
        assert project.packages.contains("python-lcov-cobertura-native")
        assert project.packages.contains("qemu-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c test")
        assert o["stdout"].containsAll("cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c testall")
        assert o["stdout"].containsAll("NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_testall: Started",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                       "NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverage")
        assert o["stdout"].containsAll("cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_coverage: GCC Code Coverage Report")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverageall")
        assert o["stdout"].containsAll("NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_coverageall: Started",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                       "cpp-project-qt5-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c checkcode")
        assert o["stdout"].containsAll("cpp-project-qt5-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-qt5-1.0.0-r0 do_checkcode: * cpplint is running...")


    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c checkcodeall")
        assert o["stdout"].containsAll("cpp-project-qt5-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-qt5-1.0.0-r0 do_checkcode: * cpplint is running...")


class cpp_project_autotools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake cpp-project-autotools").stderr.empty()

        project = self.build.parse("cpp-project-autotools")
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("lcov-native")
        assert project.packages.contains("python-lcov-cobertura-native")
        assert project.packages.contains("qemu-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c test")
        assert o["stdout"].contains("cpp-project-autotools-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c testall")
        assert o["stdout"].containsAll("NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_testall: Started",
                                       "cpp-project-autotools-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                       "NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c coverage")
        assert o["stdout"].containsAll("cpp-project-autotools-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                       "cpp-project-autotools-1.0.0-r0 do_coverage: GCC Code Coverage Report")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c coverageall")
        assert o["stdout"].containsAll("NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_coverageall: Started",
                                       "cpp-project-autotools-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                       "cpp-project-autotools-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "NOTE: recipe cpp-project-autotools-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c checkcode")
        assert o["stdout"].containsAll("cpp-project-autotools-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-autotools-1.0.0-r0 do_checkcode: * cpplint is running...")


    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake cpp-project-autotools -c checkcodeall")
        assert o["stdout"].containsAll("cpp-project-autotools-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                       "cpp-project-autotools-1.0.0-r0 do_checkcode: * cpplint is running...")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
