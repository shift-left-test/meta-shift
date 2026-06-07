#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.output import Output
from selftest.output import Outputs
import logging
import subprocess


logger = logging.getLogger(__name__)

MAX_RETRIES = 3
# qemu-user occasionally races on pthread_cancel during target test runs; retry
# only this specific, transient failure.
LIBGCC_RACE_MARKER = "libgcc_s.so.1 must be installed for pthread_cancel to work"


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
        outputs = None
        for attempt in range(1, MAX_RETRIES + 1):
            proc = subprocess.Popen(self.cmd(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            streams = proc.communicate()
            outputs = Outputs({
                "stdout": Output(streams[0].decode("utf-8")),
                "stderr": Output(streams[1].decode("utf-8")),
                "returncode": proc.returncode})
            # Retry only the known qemu-user libgcc_s race, and only when the
            # command actually failed -- a successful run whose output merely
            # mentions the string must not be needlessly re-executed.
            if not (proc.returncode != 0 and outputs.stderr.contains(LIBGCC_RACE_MARKER)):
                break
            logger.warning("Retry %d/%d after libgcc_s pthread_cancel race: %s", attempt, MAX_RETRIES, command)
        return outputs
