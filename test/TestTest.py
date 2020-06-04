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
        assert files.containsAll("cmake-project-1.0.0-r0.aarch64.rpm",
                                 "qmake5-project-1.0.0-r0.aarch64.rpm",
                                 "autotools-project-1.0.0-r0.aarch64.rpm",
                                 "sqlite3logger-1.0.0-r0.aarch64.rpm",
                                 "libsqlite3wrapper0-0.1.0-r0.aarch64.rpm")

        assert self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gtest/latest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c test")
        assert o.stderr.contains("ERROR: Task do_test does not exist for target core-image-minimal")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c testall")
        assert o.stdout.containsAll("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Started",
                                    "cmake-project-1.0.0-r0 do_test: Running tests...",
                                    "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                    "stringutils-0.0.1-r0 do_test: Running tests...",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                    "autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                    "NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverage")
        assert o.stderr.contains("ERROR: Task do_coverage does not exist for target core-image-minimal")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert o.stdout.containsAll("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Started",
                                    "cmake-project-1.0.0-r0 do_test: Running tests...",
                                    "cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                    "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                    "sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report",
                                    "stringutils-0.0.1-r0 do_test: Running tests...",
                                    "stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                    "qmake5-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                    "autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                    "autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                    "NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c checkcode")
        assert o.stderr.contains("ERROR: Task do_checkcode does not exist for target core-image-minimal")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c checkcodeall")
        assert o.stdout.containsAll("qmake5-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "qmake5-project-1.0.0-r0 do_checkcode: * cpplint is running...",
                                    "cmake-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "cmake-project-1.0.0-r0 do_checkcode: * cpplint is running...",
                                    "sqlite3wrapper-0.1.0-r0 do_checkcode: * cppcheck is running...",
                                    "sqlite3wrapper-0.1.0-r0 do_checkcode: * cpplint is running...",
                                    "autotools-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "autotools-project-1.0.0-r0 do_checkcode: * cpplint is running...")


class cmake_project(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake cmake-project").stderr.empty()

        project = self.build.parse("cmake-project")
        assert project.packages.contains("cmake-native")
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("cppcheck-native")
        assert project.packages.contains("cpplint-native")
        assert project.packages.contains("lcov-native")
        assert project.packages.contains("python-lcov-cobertura-native")
        assert project.packages.contains("qemu-native")
        assert project.packages.contains("sage-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cmake-project -c test")
        assert o.stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cmake-project -c testall")
        assert o.stdout.containsAll("NOTE: recipe cmake-project-1.0.0-r0: task do_testall: Started",
                                    "cmake-project-1.0.0-r0 do_test: Running tests...",
                                    "NOTE: recipe cmake-project-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cmake-project -c coverage")
        assert o.stdout.containsAll("cmake-project-1.0.0-r0 do_test: Running tests...",
                                    "cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cmake-project -c coverageall")
        assert o.stdout.containsAll("NOTE: recipe cmake-project-1.0.0-r0: task do_coverageall: Started",
                                    "cmake-project-1.0.0-r0 do_test: Running tests...",
                                    "cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                    "NOTE: recipe cmake-project-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake cmake-project -c checkcode")
        assert o.stdout.containsAll("cmake-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "cmake-project-1.0.0-r0 do_checkcode: * cpplint is running...")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake cmake-project -c checkcodeall")
        assert o.stdout.containsAll("cmake-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "cmake-project-1.0.0-r0 do_checkcode: * cpplint is running...")


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
        assert o.stderr.contains("ERROR: Task do_test does not exist for target sqlite3logger")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c testall")
        assert o.stdout.containsAll("NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Started",
                                    "stringutils-0.0.1-r0 do_test: Running tests...",
                                    "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                    "NOTE: recipe sqlite3logger-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverage")
        assert o.stderr.contains("ERROR: Task do_coverage does not exist for target sqlite3logger")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverageall")
        assert o.stdout.containsAll("NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Started",
                                    "stringutils-0.0.1-r0 do_test: Running tests...",
                                    "stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report",
                                    "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                    "sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report",
                                    "NOTE: recipe sqlite3logger-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c checkcode")
        assert o.stderr.containsAll("ERROR: Task do_checkcode does not exist for target sqlite3logger")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c checkcodeall")
        assert o.stdout.containsAll("stringutils-0.0.1-r0 do_checkcode: * cppcheck is running...",
                                    "stringutils-0.0.1-r0 do_checkcode: * cpplint is running...",
                                    "sqlite3wrapper-0.1.0-r0 do_checkcode: * cppcheck is running...",
                                    "sqlite3wrapper-0.1.0-r0 do_checkcode: * cpplint is running...")


class qmake5_project5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_build(self):
        assert self.build.shell.execute("bitbake qmake5-project").stderr.empty()

        project = self.build.parse("qmake5-project")
        assert project.packages.contains("qtbase")
        assert project.packages.contains("lcov-native")
        assert project.packages.contains("python-lcov-cobertura-native")
        assert project.packages.contains("qemu-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake qmake5-project -c test")
        assert o.stdout.containsAll("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake qmake5-project -c testall")
        assert o.stdout.containsAll("NOTE: recipe qmake5-project-1.0.0-r0: task do_testall: Started",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                    "NOTE: recipe qmake5-project-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake qmake5-project -c coverage")
        assert o.stdout.containsAll("qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                    "qmake5-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake qmake5-project -c coverageall")
        assert o.stdout.containsAll("NOTE: recipe qmake5-project-1.0.0-r0: task do_coverageall: Started",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of PlusTest *********",
                                    "qmake5-project-1.0.0-r0 do_test: ********* Start testing of MinusTest *********",
                                    "qmake5-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                    "NOTE: recipe qmake5-project-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake qmake5-project -c checkcode")
        assert o.stdout.containsAll("qmake5-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "qmake5-project-1.0.0-r0 do_checkcode: * cpplint is running...")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake qmake5-project -c checkcodeall")
        assert o.stdout.containsAll("qmake5-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "qmake5-project-1.0.0-r0 do_checkcode: * cpplint is running...")


class autotools_project(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake autotools-project").stderr.empty()

        project = self.build.parse("autotools-project")
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("lcov-native")
        assert project.packages.contains("python-lcov-cobertura-native")
        assert project.packages.contains("qemu-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake autotools-project -c test")
        assert o.stdout.contains("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake autotools-project -c testall")
        assert o.stdout.containsAll("NOTE: recipe autotools-project-1.0.0-r0: task do_testall: Started",
                                    "autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                    "NOTE: recipe autotools-project-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake autotools-project -c coverage")
        assert o.stdout.containsAll("autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                    "autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake autotools-project -c coverageall")
        assert o.stdout.containsAll("NOTE: recipe autotools-project-1.0.0-r0: task do_coverageall: Started",
                                    "autotools-project-1.0.0-r0 do_test:    program 1.0: test/test-suite.log",
                                    "autotools-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                    "NOTE: recipe autotools-project-1.0.0-r0: task do_coverageall: Succeeded")

    def test_do_checkcode(self):
        o = self.build.shell.execute("bitbake autotools-project -c checkcode")
        assert o.stdout.containsAll("autotools-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "autotools-project-1.0.0-r0 do_checkcode: * cpplint is running...")

    def test_do_checkcodeall(self):
        o = self.build.shell.execute("bitbake autotools-project -c checkcodeall")
        assert o.stdout.containsAll("autotools-project-1.0.0-r0 do_checkcode: * cppcheck is running...",
                                    "autotools-project-1.0.0-r0 do_checkcode: * cpplint is running...")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
