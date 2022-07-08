#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from contextlib import contextmanager
from selftest.files import Files
from selftest.shell import Shell
from selftest.util import wait_until
import os
import random
import subprocess


class Environment(object):
    def __init__(self, branch, conf_file, repo_dir, build_dir):
        self.repo_dir = repo_dir
        self.branch = branch
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.conf_file = os.path.join(self.base_dir, conf_file)
        self.build_dir = build_dir
        self.initWorkspace()

    def initWorkspace(self):
        mini_mcf = os.path.join(self.base_dir, "mini-mcf.py")
        cmd = "{} -r {} -b {} -c {} -d {}".format(mini_mcf, self.repo_dir, self.branch, self.conf_file, self.build_dir)
        subprocess.call(cmd, shell=True)

    @property
    def shell(self):
        f = os.path.join(self.repo_dir, "poky", "oe-init-build-env")
        assert os.path.exists(f)
        assert wait_until(not os.path.exists(os.path.join(self.build_dir, "hashserve.lock")), 10)
        return Shell(f, self.build_dir)

    @property
    def files(self):
        return Files(self.build_dir)

    @contextmanager
    def externalsrc(self, recipe):
        try:
            self.shell.run("devtool modify " + recipe)
            yield
        finally:
            self.shell.run("devtool reset " + recipe)
            self.shell.run("bitbake-layers remove-layer workspace")
            self.files.remove("workspace")
