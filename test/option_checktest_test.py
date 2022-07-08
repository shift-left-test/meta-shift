#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import pytest


def test_do_checktest_seed_option(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_SEED", "1234")
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")

        o = report_build.shell.execute("bitbake cmake-project -c checktest")
        assert o.stdout.contains("cmake-project/1.0.0-r0/git/minus/src/minus.cpp,minus,30,12,30,13,*")
        assert o.stdout.contains("cmake-project/1.0.0-r0/git/program/main.cpp,main,37,39,37,40,*")

        o = report_build.shell.execute("bitbake cmake-project -c checktestall")
        assert o.stdout.contains("cmake-project/1.0.0-r0/git/minus/src/minus.cpp,minus,30,12,30,13,*")
        assert o.stdout.contains("cmake-project/1.0.0-r0/git/program/main.cpp,main,37,39,37,40,*")


def test_do_checktest_verbose_option(report_build):
    with report_build.files.conf() as conf:
        conf.set("SHIFT_CHECKTEST_VERBOSE", "1")
        o = report_build.shell.execute("bitbake autotools-project -c checktest")
        assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest: CommandMutate [INFO] mutant:")
        assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest: CommandEvaluate [INFO] mutant:")
        assert o.stdout.contains("autotools-project-1.0.0-r0 do_checktest: CommandReport [INFO] evaluation-file")
