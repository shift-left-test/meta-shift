#!/usr/bin/python

import pytest
import unittest
import yocto


class YoctoTest(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch="morty", conf="with-test.conf")
        self.recipes = self.build.shell.execute("bitbake -s").stdout
        self.image = self.build.parse("core-image-minimal")
        self.sdk = self.build.parse("core-image-minimal -c populate_sdk")

    def test_populate_image(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

    def test_populate_sdk(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c populate_sdk").stderr.empty()

    def test_cppcheck_native(self):
        assert self.recipes.contains("cppcheck-native")
        assert self.build.shell.execute("bitbake cppcheck-native").stderr.empty()
        project = self.build.parse("cppcheck-native")
        assert project.packages.contains("libpcre-native")

    def test_cppcheck_nativesdk(self):
        assert self.recipes.contains("nativesdk-cppcheck")
        assert self.sdk.packages.contains("nativesdk-cppcheck")
        assert self.build.shell.execute("bitbake nativesdk-cppcheck").stderr.empty()
        project = self.build.parse("nativesdk-cppcheck")
        assert project.packages.contains("nativesdk-libpcre")

    def test_cpplint_native(self):
        assert self.recipes.contains("cpplint-native")
        assert self.build.shell.execute("bitbake cpplint-native").stderr.empty()

    def test_cpplint_nativesdk(self):
        assert self.recipes.contains("nativesdk-cpplint")
        assert self.sdk.packages.contains("nativesdk-cpplint")
        assert self.build.shell.execute("bitbake nativesdk-cpplint").stderr.empty()

    def test_gcovr_native(self):
        assert self.recipes.contains("gcovr-native")
        assert self.build.shell.execute("bitbake gcovr-native").stderr.empty()
        project = self.build.parse("gcovr-native")
        assert project.packages.contains("python-jinja2-native")
        assert project.packages.contains("python-lxml-native")

    def test_gcovr_nativesdk(self):
        assert self.recipes.contains("nativesdk-gcovr")
        assert self.sdk.packages.contains("nativesdk-gcovr")
        assert self.build.shell.execute("bitbake nativesdk-gcovr").stderr.empty()
        project = self.build.parse("nativesdk-gcovr")
        assert project.packages.contains("nativesdk-python-jinja2")
        assert project.packages.contains("nativesdk-python-lxml")

    def test_googletest(self):
        assert self.recipes.containsAny("gtest", "googletest")
        assert self.image.packages.containsAny("gtest", "googletest")
        assert self.sdk.packages.containsAny("gtest", "googletest")

    def test_doxygen_native(self):
        assert self.recipes.contains("doxygen-native")
        assert self.build.shell.execute("bitbake doxygen-native").stderr.empty()
        project = self.build.parse("doxygen-native")
        assert project.packages.contains("flex-native")
        assert project.packages.contains("bison-native")

    def test_doxygen_nativesdk(self):
        assert self.recipes.contains("nativesdk-doxygen")
        assert self.sdk.packages.contains("nativesdk-doxygen")
        assert self.build.shell.execute("bitbake nativesdk-doxygen").stderr.empty()

    def test_cmakeutils_native(self):
        assert self.recipes.contains("cmake-native")
        assert self.build.shell.execute("bitbake cmake-native").stderr.empty()
        environ = self.build.shell.execute("bitbake -e cmake-native -c install").stdout
        assert environ.contains("CMakeUtils.cmake")
        assert environ.contains("FindGMock.cmake")

    def test_cmakeutils_nativesdk(self):
        assert self.recipes.contains("nativesdk-cmake")
        assert self.build.shell.execute("bitbake nativesdk-cmake").stderr.empty()
        environ = self.build.shell.execute("bitbake -e nativesdk-cmake -c install").stdout
        assert environ.contains("CMAKE_CROSSCOMPILING_EMULATOR")
        assert environ.contains("crosscompiling_emulator.cmake")
        assert environ.contains("CMakeUtils.cmake")
        assert environ.contains("FindGMock.cmake")

    def test_cpp_project(self):
        assert self.image.packages.contains("cpp-project")
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
        command = "bitbake cpp-project -c test -v"
        expected = "50% tests passed, 2 tests failed out of 4"
        # assert that the task should not be skipped when calling multiple times
        for _ in xrange(3):
            assert self.build.shell.execute(command).stdout.contains(expected)

    def test_do_coverage(self):
        command = "bitbake cpp-project -c coverage -v"
        expected = "GCC Code Coverage Report"
        # assert that the task should not be skipped when calling multiple times
        for _ in xrange(3):
            assert self.build.shell.execute(command).stdout.contains(expected)

    def test_do_testall(self):
        command = "bitbake core-image-minimal -c testall -v"
        expected = "50% tests passed, 2 tests failed out of 4"
        # assert that the task should not be skipped when calling multiple times
        for _ in xrange(3):
            assert self.build.shell.execute(command).stdout.contains(expected)

    def test_do_coverageall(self):
        command = "bitbake core-image-minimal -c coverageall -v"
        expected = "GCC Code Coverage Report"
        # assert that the task should not be skipped when calling multiple times
        for _ in xrange(3):
            assert self.build.shell.execute(command).stdout.contains(expected)


if __name__ == "__main__":
    pytest.main(["-x", "-v", __file__])
