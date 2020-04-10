#!/usr/bin/python

import pytest
import unittest
import yocto

BRANCH = "morty"
REPORT_CONFIG = "qmake/report.conf"
NO_REPORT_CONFIG = "qmake/testable.conf"


class TestReport(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=REPORT_CONFIG)

    def test_core_image_minimal_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/minus_test/test_result.xml")
        assert self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/plus_test/test_result.xml")

    def test_cpp_project_qt5_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverageall")
        assert self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/minus_test/test_result.xml")
        assert self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/plus_test/test_result.xml")
        assert self.build.files.exists("report/test_coverage/cpp-project-qt5-1.0.0-r0/coverage.xml")


class NoTestReport(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=NO_REPORT_CONFIG)

    def test_core_image_minimal_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert not self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/minus_test/test_result.xml")
        assert not self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/plus_test/test_result.xml")

    def test_cpp_project_qt5_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project-qt5 -c coverageall")
        assert not self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/minus_test/test_result.xml")
        assert not self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/plus_test/test_result.xml")
        assert not self.build.files.exists("report/test_coverage/cpp-project-qt5-1.0.0-r0/coverage.xml")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
