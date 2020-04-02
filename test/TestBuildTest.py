#!/usr/bin/python

import pytest
import unittest
import yocto


class TestBuildTest(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch="morty", conf="test.conf")

    def test_populate_image(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()
        assert self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/image-info.txt").contains("cpp-project")
        assert self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/installed-packages.txt").contains("cpp-project-1.0.0-r0.aarch64.rpm")
        assert self.build.files.read("buildhistory/packages/aarch64-poky-linux/gtest/latest").contains("PACKAGES = gtest-dbg gtest-staticdev gtest-dev gtest-doc gtest-locale gtest-bin gtest")
        assert self.build.files.read("buildhistory/packages/aarch64-poky-linux/gmock/latest").contains("PACKAGES = gmock-dbg gmock-staticdev gmock-dev gmock-doc gmock-locale gmock-bin gmock")

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/files-in-image.txt")
        assert files.contains("./opt/tests/cpp-project-1.0.0-r0/OperatorTest")
        assert files.contains("./usr/bin/program")
        assert files.contains("./usr/lib/libplus.so.1")
        assert files.contains("./usr/lib/libplus.so.1.0.0")

    def test_cpp_project(self):
        assert self.build.shell.execute("bitbake cpp-project").stderr.empty()

        project = self.build.parse("cpp-project")
        assert project.packages.containsAny("gtest", "googletest")
        assert project.packages.contains("cppcheck-native")
        assert project.packages.contains("cpplint-native")
        assert project.packages.contains("gcovr-native")
        assert project.packages.contains("qemu-native")
        assert project.packages.contains("doxygen-native")
        assert project.packages.contains("cmake-native")

        pkgs = self.build.shell.execute("oe-pkgdata-util list-pkg-files cpp-project").stdout
        assert pkgs.contains("/usr/bin/program")
        assert pkgs.contains("/usr/lib/libplus.so.1")
        assert pkgs.contains("/usr/lib/libplus.so.1.0.0")
        assert pkgs.contains("/opt/tests/cpp-project-1.0.0-r0/OperatorTest")

    def test_do_test(self):
        command = "bitbake cpp-project -c test"
        expected = "50% tests passed, 2 tests failed out of 4"
        assert self.build.shell.execute(command).stdout.contains(expected)
        xml = "report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml"
        assert self.build.files.exists(xml)
        assert self.build.files.read(xml).contains('classname="cpp-project.PlusTest"')
        # assert that the task should not be skipped when calling multiple times
        assert self.build.shell.execute(command).stdout.contains(expected)

    def test_do_coverage(self):
        command = "bitbake cpp-project -c coverage"
        expected = "GCC Code Coverage Report"
        assert self.build.shell.execute(command).stdout.contains(expected)
        xml = "report/test_coverage/cpp-project-1.0.0-r0/coverage.xml"
        assert self.build.files.exists(xml)
        assert self.build.files.read(xml).contains('<package name="cpp-project.git.minus.src"')
        # assert that the task should not be skipped when calling multiple times
        assert self.build.shell.execute(command).stdout.contains(expected)

    def test_do_testall(self):
        command = "bitbake core-image-minimal -c testall"
        expected = "50% tests passed, 2 tests failed out of 4"
        assert self.build.shell.execute(command).stdout.contains(expected)
        assert self.build.files.exists("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml")
        assert self.build.files.exists("report/test_result/sample-project-1.0.0-r0/SampleTest.xml")
        # assert that the task should not be skipped when calling multiple times
        assert self.build.shell.execute(command).stdout.contains(expected)

    def test_do_coverageall(self):
        command = "bitbake core-image-minimal -c coverageall"
        expected = "GCC Code Coverage Report"
        assert self.build.shell.execute(command).stdout.contains(expected)
        assert self.build.files.exists("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml")
        assert self.build.files.exists("report/test_coverage/sample-project-1.0.0-r0/coverage.xml")
        # assert that the task should not be skipped when calling multiple times
        assert self.build.shell.execute(command).stdout.contains(expected)


if __name__ == "__main__":
    pytest.main(["-x", "-v", __file__])
