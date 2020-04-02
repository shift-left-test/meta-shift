#!/usr/bin/python

import pytest
import unittest
import yocto


class NoTestReportTest(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch="morty", conf="no-test-report.conf")

    def test_do_test(self):
        command = "bitbake cpp-project -c test"
        expected = "50% tests passed, 2 tests failed out of 4"
        assert self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml")

    def test_do_coverage(self):
        command = "bitbake cpp-project -c coverage"
        expected = "GCC Code Coverage Report"
        assert self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml")

    def test_do_testall(self):
        command = "bitbake core-image-minimal -c testall"
        expected = "50% tests passed, 2 tests failed out of 4"
        assert self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml")
        assert not self.build.files.exists("report/test_result/sample-project-1.0.0-r0/SampleTest.xml")

    def test_do_coverageall(self):
        command = "bitbake core-image-minimal -c coverageall"
        expected = "GCC Code Coverage Report"
        assert self.build.shell.execute(command).stdout.contains(expected)
        assert not self.build.files.exists("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml")
        assert not self.build.files.exists("report/test_coverage/sample-project-1.0.0-r0/coverage.xml")


if __name__ == "__main__":
    pytest.main(["-x", "-v", __file__])
