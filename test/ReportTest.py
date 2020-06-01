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
        assert self.build.files.read("report/test_result/cmake-project-1.0.0-r0/OperatorTest.xml").contains('classname="cmake-project.PlusTest"')
        assert self.build.files.read("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml").contains('classname="sqlite3wrapper.DatabaseTest"')
        assert self.build.files.read("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml").contains('classname="stringutils.StringTest"')
        assert self.build.files.read("report/test_coverage/cmake-project-1.0.0-r0/coverage.xml").contains('name="cmake-project.minus.src"')
        assert self.build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").contains('name="sqlite3wrapper.include.SQLite3Wrapper"')
        assert self.build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").contains('name="stringutils.include.util"')
        assert self.build.files.read("report/test_coverage/qmake5-project-1.0.0-r0/coverage.xml").contains('name="qmake5-project.plus.src"')
        assert self.build.files.read("report/test_coverage/autotools-project-1.0.0-r0/coverage.xml").contains('name="autotools-project.plus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake core-image-minimal -c checkcodeall").stderr.empty()

        # check cppcheck report
        assert self.build.files.read("report/test_check/cmake-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/stringutils-0.0.1-r0/cppcheck_report.xml").contains('cppcheck version="')

        # check cpplint report
        assert self.build.files.read("report/test_check/cmake-project-1.0.0-r0/cpplint_report.txt")
        assert self.build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cpplint_report.txt")
        assert self.build.files.read("report/test_check/stringutils-0.0.1-r0/cpplint_report.txt")


class cmake_project(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake cmake-project -c coverageall").stderr.empty()
        assert self.build.files.read("report/test_result/cmake-project-1.0.0-r0/OperatorTest.xml").contains('classname="cmake-project.PlusTest"')
        assert self.build.files.read("report/test_coverage/cmake-project-1.0.0-r0/coverage.xml").contains('name="cmake-project.minus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake cmake-project -c checkcodeall").stderr.empty()
        assert self.build.files.read("report/test_check/cmake-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/cmake-project-1.0.0-r0/cpplint_report.txt")


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


class qmake5_project5(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake qmake5-project -c coverageall").stderr.empty()
        assert self.build.files.exists("report/test_result/qmake5-project-1.0.0-r0/tests/minus_test/test_result.xml")
        assert self.build.files.exists("report/test_result/qmake5-project-1.0.0-r0/tests/plus_test/test_result.xml")
        assert self.build.files.read("report/test_coverage/qmake5-project-1.0.0-r0/coverage.xml").contains('name="qmake5-project.plus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake qmake5-project -c checkcodeall").stderr.empty()
        assert self.build.files.read("report/test_check/qmake5-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/qmake5-project-1.0.0-r0/cpplint_report.txt")


class autotools_project(unittest.TestCase):
    def setUp(self):
        self.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.REPORT)

    def test_do_coverageall(self):
        assert self.build.shell.execute("bitbake autotools-project -c coverageall").stderr.empty()
        assert self.build.files.exists("report/test_result/autotools-project-1.0.0-r0/operatorTest.xml")
        assert self.build.files.read("report/test_coverage/autotools-project-1.0.0-r0/coverage.xml").contains('name="autotools-project.plus.src"')

    def test_do_checkcodeall(self):
        assert self.build.shell.execute("bitbake autotools-project -c checkcodeall").stderr.empty()
        assert self.build.files.read("report/test_check/autotools-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
        assert self.build.files.read("report/test_check/autotools-project-1.0.0-r0/cpplint_report.txt")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
