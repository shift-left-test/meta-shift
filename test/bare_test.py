#!/usr/bin/python

import os
import pytest


def test_core_image_minimal(bare_build):
    assert bare_build.shell.execute("bitbake core-image-minimal").stderr.empty()

def test_cmakeutils(bare_build):
    assert bare_build.shell.execute("bitbake cmake").stderr.empty()


def test_cmakeutils_native(bare_build):
    assert bare_build.shell.execute("bitbake cmake-native").stderr.empty()
    environ = bare_build.shell.execute("bitbake -e cmake-native -c install").stdout
    assert environ.contains("CMakeUtils.cmake")
    assert environ.contains("FindGMock.cmake")


def test_cmakeutils_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-cmake").stderr.empty()
    f = "tmp/work/x86_64-nativesdk-pokysdk-linux/nativesdk-cmake/3.4.3-r0/sysroot-destdir/" \
        "opt/poky/{SDK_VERSION}/sysroots/x86_64-pokysdk-linux/usr/share/cmake/OEToolchainConfig.cmake.d/crosscompiling_emulator.cmake"
    assert bare_build.files.read(f).containsAll('SET(CMAKE_CROSSCOMPILING_EMULATOR "qemu-{QEMU_ARCH};',
                                                ';-L;$ENV{{SDKTARGETSYSROOT}};-E;LD_LIBRARY_PATH=$ENV{{SDKTARGETSYSROOT}}/usr/lib:$ENV{{SDKTARGETSYSROOT}}/lib:$LD_LIBRARY_PATH")')


def test_compiledb(bare_build):
    assert bare_build.shell.execute("bitbake compiledb").stderr.empty()


def test_compiledb_native(bare_build):
    assert bare_build.shell.execute("bitbake compiledb-native").stderr.empty()


def test_compiledb_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-compiledb").stderr.empty()


def test_cppcheck(bare_build):
    assert bare_build.shell.execute("bitbake cppcheck").stderr.empty()


def test_cppcheck_native(bare_build):
    assert bare_build.shell.execute("bitbake cppcheck-native").stderr.empty()


def test_cppcheck_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-cppcheck").stderr.empty()


def test_cpplint(bare_build):
    assert bare_build.shell.execute("bitbake cpplint").stderr.empty()


def test_cpplint_native(bare_build):
    assert bare_build.shell.execute("bitbake cpplint-native").stderr.empty()


def test_cpplint_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-cpplint").stderr.empty()


def test_fff(bare_build):
    assert bare_build.shell.execute("bitbake fff").stderr.empty()


def test_fff_native(bare_build):
    assert bare_build.shell.execute("bitbake fff-native").stderr.empty()


def test_fff_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-fff").stderr.empty()


def test_gcovr(bare_build):
    assert bare_build.shell.execute("bitbake gcovr").stderr.empty()


def test_gcovr_native(bare_build):
    assert bare_build.shell.execute("bitbake gcovr-native").stderr.empty()


def test_gcovr_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-gcovr").stderr.empty()


def test_googletest(bare_build):
    assert bare_build.shell.execute("bitbake gtest").stderr.empty()
    assert bare_build.shell.execute("bitbake gmock").stderr.empty()


def test_googletest_native(bare_build):
    assert bare_build.shell.execute("bitbake gtest-native").stderr.empty()
    assert bare_build.shell.execute("bitbake gmock-native").stderr.empty()


def test_googletest_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-gtest").stderr.empty()
    assert bare_build.shell.execute("bitbake nativesdk-gmock").stderr.empty()


def test_lcov(bare_build):
    assert bare_build.shell.execute("bitbake lcov").stderr.empty()


def test_lcov_native(bare_build):
    assert bare_build.shell.execute("bitbake lcov-native").stderr.empty()


def test_lcov_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-lcov").stderr.empty()


def test_python_bashlex(bare_build):
    assert bare_build.shell.execute("bitbake python-bashlex").stderr.empty()


def test_python_bashlex_native(bare_build):
    assert bare_build.shell.execute("bitbake python-bashlex-native").stderr.empty()


def test_python_bashlex_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-python-bashlex").stderr.empty()


def test_python_click(bare_build):
    assert bare_build.shell.execute("bitbake python-click").stderr.empty()


def test_python_click_native(bare_build):
    assert bare_build.shell.execute("bitbake python-click-native").stderr.empty()


def test_python_click_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-python-click").stderr.empty()


def test_python_enum34(bare_build):
    assert bare_build.shell.execute("bitbake python-enum34").stderr.empty()


def test_python_enum34_native(bare_build):
    assert bare_build.shell.execute("bitbake python-enum34-native").stderr.empty()


def test_python_enum34_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-python-enum34").stderr.empty()


def test_python_lcov_cobertura(bare_build):
    assert bare_build.shell.execute("bitbake python-lcov-cobertura").stderr.empty()


def test_python_lcov_cobertura_native(bare_build):
    assert bare_build.shell.execute("bitbake python-lcov-cobertura-native").stderr.empty()


def test_python_lcov_cobertura_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-python-lcov-cobertura").stderr.empty()


def test_python_shutilwhich(bare_build):
    assert bare_build.shell.execute("bitbake python-shutilwhich").stderr.empty()


def test_python_shutilwhich_native(bare_build):
    assert bare_build.shell.execute("bitbake python-shutilwhich-native").stderr.empty()


def test_python_shutilwhich_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-python-shutilwhich").stderr.empty()


def test_qemu(bare_build):
    assert bare_build.shell.execute("bitbake qemu").stderr.empty()


def test_qemu_native(bare_build):
    assert bare_build.shell.execute("bitbake qemu-native").stderr.empty()


def test_qemu_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-qemu").stderr.empty()


def test_sage(bare_build):
    assert bare_build.shell.execute("bitbake sage").stderr.empty()


def test_sage_native(bare_build):
    assert bare_build.shell.execute("bitbake sage-native").stderr.empty()


def test_sage_nativesdk(bare_build):
    assert bare_build.shell.execute("bitbake nativesdk-sage").stderr.empty()
