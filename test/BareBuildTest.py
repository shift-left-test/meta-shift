#!/usr/bin/python

import pytest
import unittest
import yocto


class BareBuildTest(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch="morty", conf="bare.conf")

    def test_populate_image(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()
        assert not self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/image-info.txt").contains("cpp-project")
        assert not self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/installed-packages.txt").contains("cpp-project-1.0.0-r0.aarch64.rpm")
        assert not self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gtest/latest")
        assert not self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gmock/latest")

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/files-in-image.txt")
        assert not files.contains("./opt/tests/cpp-project-1.0.0-r0/OperatorTest")
        assert not files.contains("./usr/bin/program")
        assert not files.contains("./usr/lib/libplus.so.1")
        assert not files.contains("./usr/lib/libplus.so.1.0.0")

    def test_populate_sdk(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c populate_sdk").stderr.empty()

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/host/installed-packages.txt")
        assert pkgs.contains("nativesdk-cmake-3.6.1-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-cppcheck-1.90-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-cpplint-1.4.5-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-doxygen-1.8.17-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-gcovr-4.2-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-qemu-2.7.0-r1.x86_64_nativesdk.rpm")

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/target/installed-packages.txt")
        assert pkgs.contains("gtest-1.7.0-r0.aarch64.rpm")

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/files-in-sdk.txt")
        assert pkgs.contains("./opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake-3.6/Modules/CMakeUtils.cmake")
        assert pkgs.contains("./opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake-3.6/Modules/FindGMock.cmake")
        assert pkgs.contains("./opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake")

    def test_cppcheck_native(self):
        assert self.build.shell.execute("bitbake cppcheck-native").stderr.empty()

    def test_cppcheck_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cppcheck").stderr.empty()

    def test_cpplint_native(self):
        assert self.build.shell.execute("bitbake cpplint-native").stderr.empty()

    def test_cpplint_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cpplint").stderr.empty()

    def test_gcovr_native(self):
        assert self.build.shell.execute("bitbake gcovr-native").stderr.empty()

    def test_gcovr_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-gcovr").stderr.empty()

    def test_googletest(self):
        assert self.build.shell.execute("bitbake gtest").stderr.empty()
        assert self.build.shell.execute("bitbake gmock").stderr.empty()

    def test_qemu_native(self):
        assert self.build.shell.execute("bitbake qemu-native").stderr.empty()

    def test_qemu_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-qemu").stderr.empty()

    def test_doxygen_native(self):
        assert self.build.shell.execute("bitbake doxygen-native").stderr.empty()

    def test_doxygen_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-doxygen").stderr.empty()

    def test_cmakeutils_native(self):
        assert self.build.shell.execute("bitbake cmake-native").stderr.empty()
        environ = self.build.shell.execute("bitbake -e cmake-native -c install").stdout
        assert environ.contains("CMakeUtils.cmake")
        assert environ.contains("FindGMock.cmake")

    def test_cmakeutils_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cmake").stderr.empty()
        f = "tmp/sysroots/x86_64-nativesdk-pokysdk-linux/opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake"
        assert self.build.files.read(f).contains('SET(CMAKE_CROSSCOMPILING_EMULATOR "qemu-aarch64;-L;$ENV{SDKTARGETSYSROOT}")')

    def test_cpp_project(self):
        assert not self.build.shell.execute("bitbake cpp-project").stderr.empty()

    def test_do_test(self):
        command = "bitbake cpp-project -c test"
        expected = "50% tests passed, 2 tests failed out of 4"
        assert not self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml")

    def test_do_coverage(self):
        command = "bitbake cpp-project -c coverage"
        expected = "GCC Code Coverage Report"
        assert not self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml")

    def test_do_testall(self):
        command = "bitbake core-image-minimal -c testall"
        expected = "50% tests passed, 2 tests failed out of 4"
        assert not self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml")
        assert not self.build.files.exists("report/test_result/sample-project-1.0.0-r0/SampleTest.xml")

    def test_do_coverageall(self):
        command = "bitbake core-image-minimal -c coverageall"
        expected = "GCC Code Coverage Report"
        assert not self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml")
        assert not self.build.files.exists("report/test_coverage/sample-project-1.0.0-r0/coverage.xml")


if __name__ == "__main__":
    pytest.main(["-x", "-v", __file__])
