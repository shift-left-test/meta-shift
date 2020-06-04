#!/usr/bin/python

import constants
import os
import pytest
import unittest
import yocto


class core_image_minimal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.BARE)

    def test_do_build(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

    def test_do_populate_sdk(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c populate_sdk").stderr.empty()

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/host/installed-packages.txt")
        assert pkgs.contains("nativesdk-cmake-3.7.2-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-cppcheck-2.0-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-cpplint-1.4.5-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-gcovr-4.2-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-lcov-1.11-r0.x86_64_nativesdk.rpm")
        assert pkgs.contains("nativesdk-qemu-2.8.0-r0.x86_64_nativesdk.rpm")

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/target/installed-packages.txt")
        assert pkgs.contains("fff-1.0-r0.aarch64.rpm")
        assert pkgs.contains("gtest-1.8.0-r0.aarch64.rpm")

        pkgs = self.build.files.read("buildhistory/sdk/poky-glibc-x86_64-core-image-minimal-aarch64/core-image-minimal/files-in-sdk.txt")
        assert pkgs.contains("./opt/poky/2.3.4/sysroots/aarch64-poky-linux/usr/include/fff/fff.h")
        assert pkgs.contains("./opt/poky/2.3.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake-3.7/Modules/CMakeUtils.cmake")
        assert pkgs.contains("./opt/poky/2.3.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake-3.7/Modules/FindGMock.cmake")
        assert pkgs.contains("./opt/poky/2.3.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake")

    def test_cmake_project_build_on_sdk(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c populate_sdk").stderr.empty()
        installer = os.path.join(self.build.builddir, "tmp", "deploy", "sdk", "poky-glibc-x86_64-core-image-minimal-aarch64-toolchain-2.3.4.sh")
        assert os.path.exists(installer)

        project_dir = os.path.join(self.build.builddir, "project")
        self.build.shell.execute("git clone http://mod.lge.com/hub/yocto/sample/cmake-project.git {}".format(project_dir))

        sdk_dir = os.path.join(self.build.builddir, "sdk")
        command = "; ".join(["{0} -d {1} -y",
                             "source {1}/environment-setup-aarch64-poky-linux",
                             "cd {2}",
                             "cmake . -DENABLE_TEST=ON",
                             "make all test"])
        o = self.build.shell.execute(command.format(installer, sdk_dir, project_dir))
        assert o.returncode == 2, o.stderr  # Expect 2, since two tests fails

    def test_cmakeutils(self):
        assert self.build.shell.execute("bitbake cmake").stderr.empty()

    def test_cmakeutils_native(self):
        assert self.build.shell.execute("bitbake cmake-native").stderr.empty()
        environ = self.build.shell.execute("bitbake -e cmake-native -c install").stdout
        assert environ.contains("CMakeUtils.cmake")
        assert environ.contains("FindGMock.cmake")

    def test_cmakeutils_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cmake").stderr.empty()
        f = "tmp/work/x86_64-nativesdk-pokysdk-linux/nativesdk-cmake/3.7.2-r0/" \
            "sysroot-destdir/opt/poky/2.3.4/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake"
        assert self.build.files.read(f).contains('SET(CMAKE_CROSSCOMPILING_EMULATOR "qemu-aarch64;-L;$ENV{SDKTARGETSYSROOT}")')

    def test_compiledb(self):
        assert self.build.shell.execute("bitbake compiledb").stderr.empty()

    def test_compiledb_native(self):
        assert self.build.shell.execute("bitbake compiledb-native").stderr.empty()

    def test_compiledb_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-compiledb").stderr.empty()

    def test_cppcheck(self):
        assert self.build.shell.execute("bitbake cppcheck").stderr.empty()

    def test_cppcheck_native(self):
        assert self.build.shell.execute("bitbake cppcheck-native").stderr.empty()

    def test_cppcheck_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cppcheck").stderr.empty()

    def test_cpplint(self):
        assert self.build.shell.execute("bitbake cpplint").stderr.empty()

    def test_cpplint_native(self):
        assert self.build.shell.execute("bitbake cpplint-native").stderr.empty()

    def test_cpplint_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-cpplint").stderr.empty()

    def test_fff(self):
        assert self.build.shell.execute("bitbake fff").stderr.empty()

    def test_fff_native(self):
        assert self.build.shell.execute("bitbake fff-native").stderr.empty()

    def test_fff_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-fff").stderr.empty()

    def test_gcovr(self):
        assert self.build.shell.execute("bitbake gcovr").stderr.empty()

    def test_gcovr_native(self):
        assert self.build.shell.execute("bitbake gcovr-native").stderr.empty()

    def test_gcovr_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-gcovr").stderr.empty()

    def test_googletest(self):
        assert self.build.shell.execute("bitbake gtest").stderr.empty()
        assert self.build.shell.execute("bitbake gmock").stderr.empty()

    def test_googletest_native(self):
        assert self.build.shell.execute("bitbake gtest-native").stderr.empty()
        assert self.build.shell.execute("bitbake gmock-native").stderr.empty()

    def test_googletest_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-gtest").stderr.empty()
        assert self.build.shell.execute("bitbake nativesdk-gmock").stderr.empty()

    def test_lcov(self):
        assert self.build.shell.execute("bitbake lcov").stderr.empty()

    def test_lcov_native(self):
        assert self.build.shell.execute("bitbake lcov-native").stderr.empty()

    def test_lcov_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-lcov").stderr.empty()

    def test_python_bashlex(self):
        assert self.build.shell.execute("bitbake python-bashlex").stderr.empty()

    def test_python_bashlex_native(self):
        assert self.build.shell.execute("bitbake python-bashlex-native").stderr.empty()

    def test_python_bashlex_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-bashlex").stderr.empty()

    def test_python_click(self):
        assert self.build.shell.execute("bitbake python-click").stderr.empty()

    def test_python_click_native(self):
        assert self.build.shell.execute("bitbake python-click-native").stderr.empty()

    def test_python_click_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-click").stderr.empty()

    def test_python_enum34(self):
        assert self.build.shell.execute("bitbake python-enum34").stderr.empty()

    def test_python_enum34_native(self):
        assert self.build.shell.execute("bitbake python-enum34-native").stderr.empty()

    def test_python_enum34_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-enum34").stderr.empty()

    def test_python_lcov_cobertura(self):
        assert self.build.shell.execute("bitbake python-lcov-cobertura").stderr.empty()

    def test_python_lcov_cobertura_native(self):
        assert self.build.shell.execute("bitbake python-lcov-cobertura-native").stderr.empty()

    def test_python_lcov_cobertura_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-lcov-cobertura").stderr.empty()

    def test_python_shutilwhich(self):
        assert self.build.shell.execute("bitbake python-shutilwhich").stderr.empty()

    def test_python_shutilwhich_native(self):
        assert self.build.shell.execute("bitbake python-shutilwhich-native").stderr.empty()

    def test_python_shutilwhich_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-python-shutilwhich").stderr.empty()

    def test_qemu(self):
        assert self.build.shell.execute("bitbake qemu").stderr.empty()

    def test_qemu_native(self):
        assert self.build.shell.execute("bitbake qemu-native").stderr.empty()

    def test_qemu_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-qemu").stderr.empty()

    def test_sage(self):
        assert self.build.shell.execute("bitbake sage").stderr.empty()

    def test_sage_native(self):
        assert self.build.shell.execute("bitbake sage-native").stderr.empty()

    def test_sage_nativesdk(self):
        assert self.build.shell.execute("bitbake nativesdk-sage").stderr.empty()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
