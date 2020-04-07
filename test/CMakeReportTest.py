#!/usr/bin/python

import pytest
import unittest
import yocto

BRANCH = "morty"
REPORT_CONFIG = "cmake/report.conf"
NO_REPORT_CONFIG = "cmake/testable.conf"


class TestReport(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=REPORT_CONFIG)

    def test_core_image_minimal_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert self.build.files.read("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml").contains('classname="cpp-project.PlusTest"')
        assert self.build.files.read("report/test_result/sample-project-1.0.0-r0/SampleTest.xml").contains('classname="sample-project.SqrtTest"')
        assert self.build.files.read("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml").contains('classname="sqlite3wrapper.DatabaseTest"')
        assert self.build.files.read("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml").contains('classname="stringutils.StringTest"')
        assert self.build.files.read("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml").contains('<package name="cpp-project.git.minus.src"')
        assert self.build.files.read("report/test_coverage/sample-project-1.0.0-r0/coverage.xml").contains('<package name="sample-project.git.abs.src"')
        assert self.build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").contains('<package name="sqlite3wrapper.git.include.SQLite3Wrapper"')
        assert self.build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").contains('<package name="stringutils.git.include.util"')

    def test_cpp_project_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project -c coverageall")
        assert self.build.files.read("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml").contains('classname="cpp-project.PlusTest"')
        assert self.build.files.read("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml").contains('<package name="cpp-project.git.minus.src"')

    def test_sqlite3logger_do_coverageall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverageall")
        assert self.build.files.read("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml").contains('classname="sqlite3wrapper.DatabaseTest"')
        assert self.build.files.read("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml").contains('classname="stringutils.StringTest"')
        assert self.build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").contains('<package name="sqlite3wrapper.git.include.SQLite3Wrapper"')
        assert self.build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").contains('<package name="stringutils.git.include.util"')


class NoTestReport(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=BRANCH, conf=NO_REPORT_CONFIG)

    def test_core_image_minimal_do_coverageall(self):
        o = self.build.shell.execute("bitbake core-image-minimal -c coverageall")
        assert not self.build.files.exists("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml")
        assert not self.build.files.exists("report/test_result/sample-project-1.0.0-r0/SampleTest.xml")
        assert not self.build.files.exists("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml")
        assert not self.build.files.exists("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml")
        assert not self.build.files.exists("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml")
        assert not self.build.files.exists("report/test_coverage/sample-project-1.0.0-r0/coverage.xml")
        assert not self.build.files.exists("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml")
        assert not self.build.files.exists("report/test_coverage/stringutils-0.0.1-r0/coverage.xml")

    def test_cpp_project_do_coverageall(self):
        o = self.build.shell.execute("bitbake cpp-project -c coverageall")
        assert not self.build.files.exists("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml")
        assert not self.build.files.exists("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml")

    def test_sqlite3logger_do_coverageall(self):
        o = self.build.shell.execute("bitbake sqlite3logger -c coverageall")
        assert not self.build.files.exists("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml")
        assert not self.build.files.exists("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml")
        assert not self.build.files.exists("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml")
        assert not self.build.files.exists("report/test_coverage/stringutils-0.0.1-r0/coverage.xml")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
