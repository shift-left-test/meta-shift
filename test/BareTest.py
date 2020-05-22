#!/usr/bin/python

import pytest
import unittest
import yocto

BRANCH = "morty"
CONFIG = "bare.conf"


class core_image_minimal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

    def test_do_populate_sdk(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c populate_sdk").stderr.empty()

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/host/installed-packages.txt")
        assert pkgs.contains("nativesdk-cmake-3.6.1-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-cppcheck-2.0-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-cpplint-1.4.5-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-gcovr-4.2-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-lcov-1.11-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-qemu-2.7.0-r1.x86_64_nativesdk.rpm")

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/target/installed-packages.txt")
        assert pkgs.contains("gtest-1.7.0-r0.aarch64.rpm")

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/files-in-sdk.txt")
        assert pkgs.contains("./opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake-3.6/Modules/CMakeUtils.cmake")
        assert pkgs.contains("./opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake-3.6/Modules/FindGMock.cmake")
        assert pkgs.contains("./opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake")

    def test_cmakeutils_native(self):
        assert self.build.shell.execute("bitbake cmake-native").stderr.empty()
        environ = self.build.shell.execute("bitbake -e cmake-native -c install").stdout
        assert environ.contains("CMakeUtils.cmake")
        assert environ.contains("FindGMock.cmake")

    def test_cmakeutils_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cmake").stderr.empty()
        f = "tmp/sysroots/x86_64-nativesdk-pokysdk-linux/opt/poky/2.2.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake"
        assert self.build.files.read(f).contains('SET(CMAKE_CROSSCOMPILING_EMULATOR "qemu-aarch64;-L;$ENV{SDKTARGETSYSROOT}")')

    def test_compiledb_native(self):
        assert self.build.shell.execute("bitbake compiledb-native").stderr.empty()

    def test_compiledb_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-compiledb").stderr.empty()

    def test_cppcheck_native(self):
        assert self.build.shell.execute("bitbake cppcheck-native").stderr.empty()

    def test_cppcheck_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cppcheck").stderr.empty()

    def test_cpplint_native(self):
        assert self.build.shell.execute("bitbake cpplint-native").stderr.empty()

    def test_cpplint_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cpplint").stderr.empty()

    def test_fff(self):
        assert self.build.shell.execute("bitbake fff").stderr.empty()
        files = self.build.shell.execute("oe-pkgdata-util list-pkg-files -p fff").stdout
        assert files.contains("/usr/include/fff/fff.h")

    def test_gcovr_native(self):
        assert self.build.shell.execute("bitbake gcovr-native").stderr.empty()

    def test_gcovr_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-gcovr").stderr.empty()

    def test_googletest(self):
        assert self.build.shell.execute("bitbake gtest").stderr.empty()
        assert self.build.shell.execute("bitbake gmock").stderr.empty()

    def test_lcov_native(self):
        assert self.build.shell.execute("bitbake lcov-native").stderr.empty()

    def test_lcov_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-lcov").stderr.empty()

    def test_python_bashlex_native(self):
        assert self.build.shell.execute("bitbake python-bashlex-native").stderr.empty()

    def test_python_bashlex_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-bashlex").stderr.empty()

    def test_python_click_native(self):
        assert self.build.shell.execute("bitbake python-click-native").stderr.empty()

    def test_python_click_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-click").stderr.empty()

    def test_python_enum34_native(self):
        assert self.build.shell.execute("bitbake python-enum34-native").stderr.empty()

    def test_python_enum34_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-enum34").stderr.empty()

    def test_python_lcov_cobertura_native(self):
        assert self.build.shell.execute("bitbake python-lcov-cobertura-native").stderr.empty()

    def test_python_lcov_cobertura_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-lcov-cobertura").stderr.empty()

    def test_python_shutilwhich_native(self):
        assert self.build.shell.execute("bitbake python-shutilwhich-native").stderr.empty()

    def test_python_shutilwhich_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-shutilwhich").stderr.empty()

    def test_qemu_native(self):
        assert self.build.shell.execute("bitbake qemu-native").stderr.empty()

    def test_qemu_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-qemu").stderr.empty()

    def test_sage_native(self):
        assert self.build.shell.execute("bitbake sage-native").stderr.empty()

    def test_sage_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-sage").stderr.empty()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
