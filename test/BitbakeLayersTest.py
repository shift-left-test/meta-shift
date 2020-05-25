#!/usr/bin/python

import pytest
import unittest
import yocto
from configure import config


class TestLayersWithRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=config["branch"], conf=config["release"])

    def test_mutually_exclusive_options(self):
        assert not self.build.shell.execute("bitbake-layers test-layers --show --add").stderr.empty()
        assert not self.build.shell.execute("bitbake-layers test-layers --show --remove").stderr.empty()
        assert not self.build.shell.execute("bitbake-layers test-layers --add --remove").stderr.empty()

    def test_default_action(self):
        o = self.build.shell.execute("bitbake-layers test-layers")
        assert o["stdout"].contains("meta-sample-test")

    def test_show(self):
        o = self.build.shell.execute("bitbake-layers test-layers --show")
        assert o["stdout"].contains("meta-sample-test")

    def test_show_with_basepath(self):
        o = self.build.shell.execute("bitbake-layers test-layers --show --basepath /dev/null")
        assert not o["stdout"].contains("meta-sample-test")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
