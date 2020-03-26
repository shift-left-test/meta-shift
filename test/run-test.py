#!/usr/bin/python

import pytest
import yoctotest


class YoctoProject(dict):
    def __init__(self, codename):
        self["env"] = yoctotest.YoctoTestEnvironment(codename)
        self["recipes"] = self["env"].shell().execute("bitbake -s").stdout
        self["image"] = self["env"].parse("core-image-minimal")
        self["sdk"] = self["env"].parse("core-image-minimal -c populate_sdk")


@pytest.fixture(scope="module", params=["morty"])
def yocto(request):
    return YoctoProject(request.param)


def test_cpp_project(yocto):
    assert yocto["image"].packages().contains("cpp-project")
    assert yocto["env"].shell().execute("bitbake cpp-project").stderr.empty()

    project = yocto["env"].parse("cpp-project")
    assert project.packages().containsAny("gtest", "googletest")
    assert project.packages().contains("cppcheck-native")
    assert project.packages().contains("cpplint-native")
    assert project.packages().contains("gcovr-native")
    assert project.packages().contains("qemu-native")
    assert project.packages().contains("doxygen-native")
    assert project.packages().contains("cmake-native")

    pkgs = yocto["env"].shell().execute("oe-pkgdata-util list-pkg-files cpp-project").stdout
    assert pkgs.contains("/opt/tests/cpp-project-1.0.0-r0/OperatorTest")
    assert pkgs.contains("/usr/bin/program")
    assert pkgs.contains("/usr/lib/libplus.so.1")
    assert pkgs.contains("/usr/lib/libplus.so.1.0.0")

def test_populate_image(yocto):
    assert yocto["env"].shell().execute("bitbake core-image-minimal").stderr.empty()

def test_populate_sdk(yocto):
    assert yocto["env"].shell().execute("bitbake core-image-minimal -c populate_sdk").stderr.empty()

def test_do_test(yocto):
    command = "bitbake cpp-project -c test -v"
    expected = "50% tests passed, 2 tests failed out of 4"
    assert yocto["env"].shell().execute(command).stdout.contains(expected)
    assert yocto["env"].shell().execute(command).stdout.contains(expected)

def test_do_coverage(yocto):
    command = "bitbake cpp-project -c coverage -v"
    expected = "GCC Code Coverage Report"
    assert yocto["env"].shell().execute(command).stdout.contains(expected)
    assert yocto["env"].shell().execute(command).stdout.contains(expected)

def test_do_testall(yocto):
    command = "bitbake core-image-minimal -c testall -v"
    expected = "50% tests passed, 2 tests failed out of 4"
    assert yocto["env"].shell().execute(command).stdout.contains(expected)
    assert yocto["env"].shell().execute(command).stdout.contains(expected)

def test_cppcheck_native(yocto):
    assert yocto["recipes"].contains("cppcheck-native")
    assert yocto["env"].shell().execute("bitbake cppcheck-native").stderr.empty()
    project = yocto["env"].parse("cppcheck-native")
    assert project.packages().contains("libpcre-native")

def test_cppcheck_nativesdk(yocto):
    assert yocto["recipes"].contains("nativesdk-cppcheck")
    assert yocto["sdk"].packages().contains("nativesdk-cppcheck")
    assert yocto["env"].shell().execute("bitbake nativesdk-cppcheck").stderr.empty()
    project = yocto["env"].parse("nativesdk-cppcheck")
    assert project.packages().contains("nativesdk-libpcre")

def test_cpplint_native(yocto):
    assert yocto["recipes"].contains("cpplint-native")
    assert yocto["env"].shell().execute("bitbake cpplint-native").stderr.empty()

def test_cpplint_nativesdk(yocto):
    assert yocto["recipes"].contains("nativesdk-cpplint")
    assert yocto["sdk"].packages().contains("nativesdk-cpplint")
    assert yocto["env"].shell().execute("bitbake nativesdk-cpplint").stderr.empty()

def test_gcovr_native(yocto):
    assert yocto["recipes"].contains("gcovr-native")
    assert yocto["env"].shell().execute("bitbake gcovr-native").stderr.empty()
    project = yocto["env"].parse("gcovr-native")
    assert project.packages().contains("python-jinja2-native")
    assert project.packages().contains("python-lxml-native")

def test_gcovr_nativesdk(yocto):
    assert yocto["recipes"].contains("nativesdk-gcovr")
    assert yocto["sdk"].packages().contains("nativesdk-gcovr")
    assert yocto["env"].shell().execute("bitbake nativesdk-gcovr").stderr.empty()
    project = yocto["env"].parse("nativesdk-gcovr")
    assert project.packages().contains("nativesdk-python-jinja2")
    assert project.packages().contains("nativesdk-python-lxml")

def test_googletest(yocto):
    assert yocto["recipes"].containsAny("gtest", "googletest")
    assert yocto["image"].packages().containsAny("gtest", "googletest")
    assert yocto["sdk"].packages().containsAny("gtest", "googletest")

def test_doxygen_native(yocto):
    assert yocto["recipes"].contains("doxygen-native")
    assert yocto["env"].shell().execute("bitbake doxygen-native").stderr.empty()
    project = yocto["env"].parse("doxygen-native")
    assert project.packages().contains("flex-native")
    assert project.packages().contains("bison-native")

def test_doxygen_nativesdk(yocto):
    assert yocto["recipes"].contains("nativesdk-doxygen")
    assert yocto["sdk"].packages().contains("nativesdk-doxygen")
    assert yocto["env"].shell().execute("bitbake nativesdk-doxygen").stderr.empty()

def test_cmakeutils_native(yocto):
    assert yocto["recipes"].contains("cmake-native")
    assert yocto["env"].shell().execute("bitbake cmake-native").stderr.empty()
    environ = yocto["env"].shell().execute("bitbake -e cmake-native -c install").stdout
    assert environ.contains("CMakeUtils.cmake")
    assert environ.contains("FindGMock.cmake")

def test_cmakeutils_nativesdk(yocto):
    assert yocto["recipes"].contains("nativesdk-cmake")
    assert yocto["env"].shell().execute("bitbake nativesdk-cmake").stderr.empty()
    environ = yocto["env"].shell().execute("bitbake -e nativesdk-cmake -c install").stdout
    assert environ.contains("CMAKE_CROSSCOMPILING_EMULATOR")
    assert environ.contains("crosscompiling_emulator.cmake")
    assert environ.contains("CMakeUtils.cmake")
    assert environ.contains("FindGMock.cmake")


if __name__ == "__main__":
    pytest.main(["-x", "-v", __file__])
