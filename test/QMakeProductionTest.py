#!/usr/bin/python

import pytest
import unittest
import yocto

BRANCH = "morty"
CONFIG = "qmake/production.conf"


class core_image_minimal(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_populate(self):
        assert self.build.shell.execute("bitbake core-image-minimal").stderr.empty()

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/image-info.txt")
        assert files.containsAll("cpp-project-qt5")

        files = self.build.files.read("buildhistory/images/qemuarm64/glibc/core-image-minimal/installed-packages.txt")
        assert files.containsAll("cpp-project-qt5-1.0.0-r0.aarch64.rpm")

        assert not self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gtest/latest")
        assert not self.build.files.exists("buildhistory/packages/aarch64-poky-linux/gmock/latest")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target core-image-minimal")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c testall")
        assert o["stdout"].contains("NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Started\n" \
                                    "NOTE: recipe core-image-minimal-1.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target core-image-minimal")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert o["stdout"].contains("NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Started\n" \
                                    "NOTE: recipe core-image-minimal-1.0-r0: task do_coverageall: Succeeded\n")

    def test_do_doc(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c doc")
        assert o["stderr"].contains("ERROR: Task do_doc does not exist for target core-image-minimal")

    def test_do_docall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c docall")
        assert o["stdout"].contains("NOTE: recipe core-image-minimal-1.0-r0: task do_docall: Started\n" \
                                    "NOTE: recipe core-image-minimal-1.0-r0: task do_docall: Succeeded\n")


class cpp_project_qt5(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=CONFIG)

    def test_populate(self):
        assert self.build.shell.execute("bitbake cpp-project-qt5").stderr.empty()

        project = self.build.parse("cpp-project-qt5")
        assert project.packages.contains("qtbase")
        assert not project.packages.contains("gcovr-native")
        assert not project.packages.contains("doxygen-native")

    def test_do_test(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c test")
        assert o["stderr"].contains("ERROR: Task do_test does not exist for target cpp-project-qt5")

    def test_do_testall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c testall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_testall: Started\n" \
                                    "NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_testall: Succeeded")

    def test_do_coverage(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverage")
        assert o["stderr"].contains("ERROR: Task do_coverage does not exist for target cpp-project-qt5")

    def test_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverageall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_coverageall: Started\n" \
                                    "NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_coverageall: Succeeded")

    @unittest.skip("WIP")
    def test_do_doc(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c doc")
        assert o["stderr"].contains("ERROR: Task do_doc does not exist for target cpp-project-qt5")

    @unittest.skip("WIP")
    def test_do_docall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c docall")
        assert o["stdout"].contains("NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_docall: Started\n" \
                                    "NOTE: recipe cpp-project-qt5-1.0.0-r0: task do_docall: Succeeded")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
