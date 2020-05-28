#!/usr/bin/python

import constants
import pytest
import unittest
import yocto


class core_image_minimal(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c coverageall").stderr.empty()
        assert self.build.files.read("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml").contains('classname="cpp-project.PlusTest"')
        assert self.build.files.read("report/test_result/sample-project-1.0.0-r0/SampleTest.xml").contains('classname="sample-project.SqrtTest"')
        assert self.build.files.read("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml").contains('classname="sqlite3wrapper.DatabaseTest"')
        assert self.build.files.read("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml").contains('classname="stringutils.StringTest"')
        assert self.build.files.read("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml").contains('name="cpp-project.minus.src"')
        assert self.build.files.read("report/test_coverage/sample-project-1.0.0-r0/coverage.xml").contains('name="sample-project.abs.src"')
        assert self.build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").contains('name="sqlite3wrapper.include.SQLite3Wrapper"')
        assert self.build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").contains('name="stringutils.include.util"')
        assert self.build.files.read("report/test_coverage/cpp-project-qt5-1.0.0-r0/coverage.xml").contains('name="cpp-project-qt5.plus.src"')
        assert self.build.files.read("report/test_coverage/cpp-project-autotools-1.0.0-r0/coverage.xml").contains('name="cpp-project-autotools.plus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c checkcodeall").stderr.empty()

        # check cppcheck report
        assert self.build.files.read("report/test_check/cpp-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/sample-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/stringutils-0.0.1-r0/cppcheck_report.xml").contains('cppcheck version="')

        #check cpplint report
        assert self.build.files.read("report/test_check/cpp-project-1.0.0-r0/cpplint_report.txt")
        assert self.build.files.read("report/test_check/sample-project-1.0.0-r0/cpplint_report.txt")
        assert self.build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cpplint_report.txt")
        assert self.build.files.read("report/test_check/stringutils-0.0.1-r0/cpplint_report.txt")


class cpp_project(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake cpp-project -c coverageall").stderr.empty()
        assert self.build.files.read("report/test_result/cpp-project-1.0.0-r0/OperatorTest.xml").contains('classname="cpp-project.PlusTest"')
        assert self.build.files.read("report/test_coverage/cpp-project-1.0.0-r0/coverage.xml").contains('name="cpp-project.minus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake cpp-project -c checkcodeall").stderr.empty()
        assert self.build.files.read("report/test_check/cpp-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/cpp-project-1.0.0-r0/cpplint_report.txt")


class sqlite3logger(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake sqlite3logger -c coverageall").stderr.empty()
        assert self.build.files.read("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml").contains('classname="sqlite3wrapper.DatabaseTest"')
        assert self.build.files.read("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml").contains('classname="stringutils.StringTest"')
        assert self.build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").contains('name="sqlite3wrapper.include.SQLite3Wrapper"')
        assert self.build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").contains('name="stringutils.include.util"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake sqlite3logger -c checkcodeall").stderr.empty()
        assert self.build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/stringutils-0.0.1-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cpplint_report.txt")
        assert self.build.files.read("report/test_check/stringutils-0.0.1-r0/cpplint_report.txt")


class cpp_project_qt5(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake cpp-project-qt5 -c coverageall").stderr.empty()
        assert self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/minus_test/test_result.xml")
        assert self.build.files.exists("report/test_result/cpp-project-qt5-1.0.0-r0/tests/plus_test/test_result.xml")
        assert self.build.files.read("report/test_coverage/cpp-project-qt5-1.0.0-r0/coverage.xml").contains('name="cpp-project-qt5.plus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake cpp-project-qt5 -c checkcodeall").stderr.empty()
        assert self.build.files.read("report/test_check/cpp-project-qt5-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/cpp-project-qt5-1.0.0-r0/cpplint_report.txt")


class cpp_project_autotools(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake cpp-project-autotools -c coverageall").stderr.empty()
        assert self.build.files.exists("report/test_result/cpp-project-autotools-1.0.0-r0/operatorTest.xml")
        assert self.build.files.read("report/test_coverage/cpp-project-autotools-1.0.0-r0/coverage.xml").contains('name="cpp-project-autotools.plus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake cpp-project-autotools -c checkcodeall").stderr.empty()
        assert self.build.files.read("report/test_check/cpp-project-autotools-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/cpp-project-autotools-1.0.0-r0/cpplint_report.txt")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
