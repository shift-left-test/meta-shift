#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.parsers.data import asList
from cpptest_base import (
    assert_arithmetic_coverage,
    assert_checktest_summary,
    assert_coverage_branch_in_xml,
    assert_coverage_branch_text,
    assert_coverage_excludes,
    assert_coverage_extra_options,
    assert_test_filter,
    assert_test_shuffle,
    assert_test_suppress_failures,
    assert_verify_without_report_dir,
)


RECIPE = "cmake-project"


def test_do_checktest(stdout, report):
    assert_checktest_summary(stdout, report, RECIPE)


def test_do_checktest_excludes(report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_PATTERNS", "!plus/plus.cpp")
        report.shell.execute("bitbake cmake-project -c checktest")
        with report.files.readAsXml("report/cmake-project-1.0.0-r0/checktest/mutations.xml") as data:
            paths = asList(data["mutations/mutation/sourceFilePath"])
            assert "plus/plus.cpp" not in paths


def test_do_checktest_extensions(report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")
        conf.set("SHIFT_CHECKTEST_EXTENSIONS", ".unknown")

        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert not o.stdout.contains("AOR : plus/plus.cpp (30:12-30:13 -> *)")


def test_do_checktest_generator(report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_GENERATOR", "uniform")
        first = report.shell.execute("bitbake cmake-project -c checktest").stdout

    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_GENERATOR", "weighted")
        second = report.shell.execute("bitbake cmake-project -c checktest").stdout

    assert first != second


def test_do_checktest_seed(report):
    def collect_mutation_ids():
        with report.files.readAsXml("report/cmake-project-1.0.0-r0/checktest/mutations.xml") as data:
            paths = asList(data["mutations/mutation/sourceFilePath"])
            lines = asList(data["mutations/mutation/lineNumber"])
            mutators = asList(data["mutations/mutation/mutator"])
            return sorted(zip(paths, lines, mutators))

    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        report.shell.execute("bitbake cmake-project -c checktest")
        first = collect_mutation_ids()
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        report.shell.execute("bitbake cmake-project -c checktest")
        second = collect_mutation_ids()
    assert first == second


def test_do_checktest_verbose(report):
    with report.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")

        o = report.shell.execute("bitbake cmake-project -c checktest")
        assert o.stdout.contains("(seed: 1234)")


def test_do_coverage(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    assert stdout.contains("cmake-project-1.0.0-r0 do_coverage: GCC Code Coverage Report")
    assert_arithmetic_coverage(report, RECIPE)


def test_do_coverage_branch(stdout, report):
    assert_coverage_branch_in_xml(report, RECIPE)


def test_do_coverage_branch_text(report):
    assert_coverage_branch_text(report, RECIPE)


def test_do_coverage_excludes(stdout, report):
    assert_coverage_excludes(report, RECIPE)


def test_do_coverage_extra_options(report):
    assert_coverage_extra_options(report, RECIPE)


def test_do_verify(test_build):
    assert_verify_without_report_dir(test_build, RECIPE)


def test_do_test(stdout, report):
    assert stdout.contains("cmake-project-1.0.0-r0 do_test: Running tests...")
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/test/OperatorTest_1.xml") as data:
        data = data["testsuites/testsuite"]
        assert data["name"] == "PlusTest" and data["tests"] == "1" and data["failures"] == "1"
    with report.files.readAsXml("report/cmake-project-1.0.0-r0/test/OperatorTest_3.xml") as data:
        data = data["testsuites/testsuite"]
        assert data["name"] == "MinusTest" and data["tests"] == "1" and data["failures"] == "1"


def test_do_test_filter(test_build):
    assert_test_filter(test_build, RECIPE)


def test_do_test_shuffle(test_build):
    assert_test_shuffle(test_build, RECIPE)


def test_do_test_parallel(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_PARALLEL_JOBS", "2")
        conf.set("BB_VERBOSE_LOGS", "1")
        o = test_build.shell.execute("bitbake cmake-project -c test")
        assert o.stdout.contains("--parallel 2") or o.stderr.contains("--parallel 2")


def test_do_test_qemu_set_env(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_QEMU_SET_ENV", "LD_PRELOAD=/nonexistent_preload.so")
        o = test_build.shell.execute("bitbake cmake-project -c test")
        # qemu forwards LD_PRELOAD into the guest, whose loader reports the
        # missing object -- proof the var reached the guest, not the host.
        assert o.stdout.contains("nonexistent_preload.so") or o.stderr.contains("nonexistent_preload.so")


def test_do_test_suppress_failures(test_build):
    assert_test_suppress_failures(test_build, RECIPE)


def test_do_test_stop_on_failure(test_build):
    with test_build.files.conf() as conf:
        conf.set("SHIFT_TEST_STOP_ON_FAILURE", "1")
        conf.set("BB_VERBOSE_LOGS", "1")
        o = test_build.shell.execute("bitbake cmake-project -c test")
        assert o.stdout.contains("--stop-on-failure") or o.stderr.contains("--stop-on-failure")
