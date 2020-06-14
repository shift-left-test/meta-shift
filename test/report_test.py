#!/usr/bin/python

import pytest


def test_core_image_minimal_do_coverageall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake core-image-minimal -c coverageall").stderr.empty()

    assert report_build.files.read("report/test_result/cmake-project-1.0.0-r0/OperatorTest.xml").contains('classname="cmake-project.PlusTest"')
    assert report_build.files.read("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml").contains('classname="sqlite3wrapper.DatabaseTest"')
    assert report_build.files.read("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml").contains('classname="stringutils.StringTest"')
    assert report_build.files.read("report/test_result/humidifier-project-1.0.0-r0/unittest.xml").contains('classname="humidifier-project.HumidifierTest"')

    assert report_build.files.read("report/test_coverage/cmake-project-1.0.0-r0/coverage.xml").contains('name="cmake-project.minus.src"')
    assert report_build.files.read("report/test_coverage/cmake-project-1.0.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')
    assert report_build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").contains('name="sqlite3wrapper.include.SQLite3Wrapper"')
    assert report_build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Column::getName() const" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Statement::check(int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Database::check(int)" signature="">')
    assert report_build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").contains('name="stringutils.include.util"')
    assert report_build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="bool util::string::contains&lt;char&gt;(char const*, char const*)" signature="">')
    assert report_build.files.read("report/test_coverage/qmake5-project-1.0.0-r0/coverage.xml").contains('name="qmake5-project.plus.src"')
    assert report_build.files.read("report/test_coverage/qmake5-project-1.0.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')
    assert report_build.files.read("report/test_coverage/autotools-project-1.0.0-r0/coverage.xml").contains('name="autotools-project.plus.src"')
    assert report_build.files.read("report/test_coverage/autotools-project-1.0.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')
    assert report_build.files.read("report/test_coverage/humidifier-project-1.0.0-r0/coverage.xml").contains('name="humidifier-project.humidifier.src"')
    assert report_build.files.read("report/test_coverage/humidifier-project-1.0.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="Humidifier::Humidifier(HumiditySensor const&amp;)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="Humidifier::setPreferredHumidity(int)" signature="">')


def test_core_image_minimal_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake core-image-minimal -c checkcodeall").stderr.empty()

    # check cppcheck report
    assert report_build.files.read("report/test_check/cmake-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
    assert report_build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cppcheck_report.xml").contains('cppcheck version=')
    assert report_build.files.read("report/test_check/stringutils-0.0.1-r0/cppcheck_report.xml").contains('cppcheck version="')

    # check cpplint report
    assert report_build.files.read("report/test_check/cmake-project-1.0.0-r0/cpplint_report.txt")
    assert report_build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cpplint_report.txt")
    assert report_build.files.read("report/test_check/stringutils-0.0.1-r0/cpplint_report.txt")


def test_cmake_project_do_coverageall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c coverageall").stderr.empty()
    assert report_build.files.read("report/test_result/cmake-project-1.0.0-r0/OperatorTest.xml").contains('classname="cmake-project.PlusTest"')
    assert report_build.files.read("report/test_coverage/cmake-project-1.0.0-r0/coverage.xml").contains('name="cmake-project.minus.src"')
    assert report_build.files.read("report/test_coverage/cmake-project-1.0.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_cmake_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake cmake-project -c checkcodeall").stderr.empty()
    assert report_build.files.read("report/test_check/cmake-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
    assert report_build.files.read("report/test_check/cmake-project-1.0.0-r0/cpplint_report.txt")


def test_qmake5_project_do_coverageall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake qmake5-project -c coverageall").stderr.empty()
    assert report_build.files.exists("report/test_result/qmake5-project-1.0.0-r0/tests/minus_test/test_result.xml")
    assert report_build.files.exists("report/test_result/qmake5-project-1.0.0-r0/tests/plus_test/test_result.xml")
    assert report_build.files.read("report/test_coverage/qmake5-project-1.0.0-r0/coverage.xml").contains('name="qmake5-project.plus.src"')
    assert report_build.files.read("report/test_coverage/qmake5-project-1.0.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_qmake5_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake qmake5-project -c checkcodeall").stderr.empty()
    assert report_build.files.read("report/test_check/qmake5-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
    assert report_build.files.read("report/test_check/qmake5-project-1.0.0-r0/cpplint_report.txt")


def test_autotools_project_do_coverageall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake autotools-project -c coverageall").stderr.empty()
    assert report_build.files.exists("report/test_result/autotools-project-1.0.0-r0/operatorTest.xml")
    assert report_build.files.read("report/test_coverage/autotools-project-1.0.0-r0/coverage.xml").contains('name="autotools-project.plus.src"')
    assert report_build.files.read("report/test_coverage/autotools-project-1.0.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::plus(int, int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="arithmetic::minus(int, int)" signature="">')


def test_autotools_project_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake autotools-project -c checkcodeall").stderr.empty()
    assert report_build.files.read("report/test_check/autotools-project-1.0.0-r0/cppcheck_report.xml").contains('cppcheck version=')
    assert report_build.files.read("report/test_check/autotools-project-1.0.0-r0/cpplint_report.txt")


def test_sqlite3logger_do_coverageall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake sqlite3logger -c coverageall").stderr.empty()
    assert report_build.files.read("report/test_result/sqlite3wrapper-0.1.0-r0/SQLite3WrapperTest.exe.xml").contains('classname="sqlite3wrapper.DatabaseTest"')
    assert report_build.files.read("report/test_result/stringutils-0.0.1-r0/unittest.bin.xml").contains('classname="stringutils.StringTest"')
    assert report_build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").contains('name="sqlite3wrapper.include.SQLite3Wrapper"')
    assert report_build.files.read("report/test_coverage/sqlite3wrapper-0.1.0-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Column::getName() const" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Statement::check(int)" signature="">',
        '<method branch-rate="1.0" line-rate="1.0" name="SQLite3Wrapper::Database::check(int)" signature="">')
    assert report_build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").contains('name="stringutils.include.util"')
    assert report_build.files.read("report/test_coverage/stringutils-0.0.1-r0/coverage.xml").containsAll(
        '<method branch-rate="1.0" line-rate="1.0" name="bool util::string::contains&lt;char&gt;(char const*, char const*)" signature="">')


def test_sqlite3logger_do_checkcodeall(report_build):
    report_build.files.remove("report")
    assert report_build.shell.execute("bitbake sqlite3logger -c checkcodeall").stderr.empty()
    assert report_build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cppcheck_report.xml").contains('cppcheck version=')
    assert report_build.files.read("report/test_check/stringutils-0.0.1-r0/cppcheck_report.xml").contains('cppcheck version=')
    assert report_build.files.read("report/test_check/sqlite3wrapper-0.1.0-r0/cpplint_report.txt")
    assert report_build.files.read("report/test_check/stringutils-0.0.1-r0/cpplint_report.txt")
