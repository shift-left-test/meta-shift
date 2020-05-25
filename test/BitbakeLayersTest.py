#!/usr/bin/python

import pytest
import unittest
import yocto
from configure import config


class BitbakeLayersWithRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=config["branch"], conf=config["release"])

    def test_show_test_layers(self):
        o = self.build.shell.execute("bitbake-layers test-layers --show")
        assert o["stdout"].contains("meta-sample-test")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
