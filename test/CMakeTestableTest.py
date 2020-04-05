#!/usr/bin/python

import pytest
import unittest
import yocto

BRANCH = "morty"
CONFIG = "cmake/testable.conf"


class core_image_minimal(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_populate(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/image-info.txt")
        assert files.containsAll("sample-project", "cpp-project", "sqlite3logger")

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/installed-packages.txt")
        assert files.containsAll("sample-project-1.0.0-r0.aarch64.rpm",
                                 "cpp-project-1.0.0-r0.aarch64.rpm",
                                 "sqlite3logger-1.0.0-r0.aarch64.rpm",
                                 "libsqlite3wrapper0-0.1.0-r0.aarch64.rpm")

        assert self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gtest/latest")
        assert self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gmock/latest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target core-image-minimal")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c testall")
        assert o["stdout"].containsAll("cpp-project-1.0.0-r0 do_test: Running tests...",
                                       "sample-project-1.0.0-r0 do_test: Running tests...",
                                       "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                       "stringutils-0.0.1-r0 do_test: Running tests...")


    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target core-image-minimal")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert o["stdout"].containsAll("cpp-project-1.0.0-r0 do_test: Running tests...",
                                       "cpp-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "sample-project-1.0.0-r0 do_test: Running tests...",
                                       "sample-project-1.0.0-r0 do_coverage: GCC Code Coverage Report",
                                       "sqlite3wrapper-0.1.0-r0 do_test: Running tests...",
                                       "sqlite3wrapper-0.1.0-r0 do_coverage: GCC Code Coverage Report",
                                       "stringutils-0.0.1-r0 do_test: Running tests...",
                                       "stringutils-0.0.1-r0 do_coverage: GCC Code Coverage Report")

    def test_do_doc(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c doc")
        assert o["stderr"].contains("ERROR: Task do_doc does not exist for target core-image-minimal")

    def test_do_docall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c docall")
        assert o["stdout"].containsAll("NOTE: recipe core-image-minimal-1.0-r0: task do_docall: Started",
                                       "cpp-project-1.0.0-r0 do_doc: [100%] Generating API documentation with Doxygen",
                                       "sample-project-1.0.0-r0 do_doc: [100%] Generating API documentation with Doxygen",
                                       "sqlite3wrapper-0.1.0-r0 do_doc: [100%] Generating API documentation with Doxygen",
                                       "NOTE: recipe core-image-minimal-1.0-r0: task do_docall: Succeeded")


class cpp_project(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_populate(self):
        assert self.build.shell.execute("bitbake cpp-project").stderr.empty()

        project = self.build.parse("cpp-project")
        assert project.packages.contains("cmake-native")
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("cppcheck-native")
        assert project.packages.contains("cpplint-native")
        assert project.packages.contains("gcovr-native")
        assert project.packages.contains("qemu-native")
        assert project.packages.contains("doxygen-native")

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

    def test_do_doc(self):
        o = self.build.shell.execute("bitbake cpp-project -c doc")
        assert o["stdout"].contains("cpp-project-1.0.0-r0 do_doc: [100%] Generating API documentation with Doxygen")

    def test_do_docall(self):
        o = self.build.shell.execute("bitbake cpp-project -c docall")
        assert o["stdout"].containsAll("NOTE: recipe cpp-project-1.0.0-r0: task do_docall: Started",
                                       "cpp-project-1.0.0-r0 do_doc: [100%] Generating API documentation with Doxygen",
                                       "NOTE: recipe cpp-project-1.0.0-r0: task do_docall: Succeeded")


class sqlite3logger(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_populate(self):
        assert self.build.shell.execute("bitbake sqlite3logger").stderr.empty()

        project = self.build.parse("sqlite3logger")
        assert project.packages.contains("cmake-native")
        assert project.packages.contains("stringutils")
        assert project.packages.contains("sqlite3wrapper")

        # List of indirect dependent packages
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("cppcheck-native")
        assert project.packages.contains("cpplint-native")
        assert project.packages.contains("gcovr-native")
        assert project.packages.contains("qemu-native")
        assert project.packages.contains("doxygen-native")

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

    def test_do_doc(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c doc")
        assert o["stderr"].contains("ERROR: Task do_doc does not exist for target sqlite3logger")

    def test_do_docall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c docall")
        assert o["stdout"].containsAll("NOTE: recipe sqlite3logger-1.0.0-r0: task do_docall: Started",
                                       "sqlite3wrapper-0.1.0-r0 do_doc: [100%] Generating API documentation with Doxygen",
                                       "NOTE: recipe sqlite3logger-1.0.0-r0: task do_docall: Succeeded")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
