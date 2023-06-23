#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.output import Output
from selftest.output import Outputs
import subprocess


class Shell(object):
    def __init__(self, script, build_dir):
        self.script = script
        self.build_dir = build_dir

    def __repr__(self):
        return "Shell: ['script': {0}, 'build_dir': {1}]".format(self.script, self.build_dir)

    def cmd(self, command):
        c = 'bash -c "source {0} {1} && {2}"'.format(self.script, self.build_dir, command)
        return c

    def run(self, command):
        subprocess.call(self.cmd(command), shell=True)

    def execute(self, command):
        retry = 0
        while retry < 3:
            retry += 1
            proc = subprocess.Popen(self.cmd(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            streams = proc.communicate()
            outputs = Outputs({
                "stdout": Output(streams[0].decode("utf-8")),
                "stderr": Output(streams[1].decode("utf-8")),
                "returncode": proc.returncode})
            # Trying executing the given command several times to avoid weird errors
            if not outputs.stderr.contains("libgcc_s.so.1 must be installed for pthread_cancel to work"):
                break
        return outputs
