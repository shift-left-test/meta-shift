#!/usr/bin/python

import constants
import pytest
import unittest
import yocto


class TestLayersWithRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.RELEASE)

    def test_mutually_exclusive_options(self):
        assert not self.build.shell.execute("bitbake-layers test-layers --show --add").stderr.empty()
        assert not self.build.shell.execute("bitbake-layers test-layers --show --remove").stderr.empty()
        assert not self.build.shell.execute("bitbake-layers test-layers --add --remove").stderr.empty()

    def test_default_action(self):
        o = self.build.shell.execute("bitbake-layers test-layers")
        assert o.stdout.contains("meta-sample-test")

    def test_show(self):
        o = self.build.shell.execute("bitbake-layers test-layers --show")
        assert o.stdout.contains("meta-sample-test")

    def test_show_with_basepath(self):
        o = self.build.shell.execute("bitbake-layers test-layers --show --basepath /dev/null")
        assert not o.stdout.contains("meta-sample-test")

    def test_add_remove(self):
        assert not self.build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
        self.build.shell.execute("bitbake-layers test-layers --add")
        assert self.build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
        self.build.shell.execute("bitbake-layers test-layers --remove")
        assert not self.build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")


class TestRecipesWithTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_show_recipes(self):
        o = self.build.shell.execute("bitbake-layers test-recipes")
        assert o.stdout.containsAll("autotools-project              1.0.0                meta-sample",
                                    "cmake-project                  1.0.0                meta-sample",
                                    "humidifier-project             1.0.0                meta-sample",
                                    "qmake5-project                 1.0.0                meta-sample",
                                    "sqlite3wrapper                 0.1.0                meta-sample",
                                    "stringutils                    0.0.1                meta-sample")

    def test_show_recipes_with_pnspec(self):
        o = self.build.shell.execute("bitbake-layers test-recipes *-project")
        assert o.stdout.containsAll("autotools-project              1.0.0                meta-sample",
                                    "cmake-project                  1.0.0                meta-sample",
                                    "humidifier-project             1.0.0                meta-sample",
                                    "qmake5-project                 1.0.0                meta-sample")
        assert not o.stdout.containsAll("sqlite3wrapper                 0.1.0                meta-sample",
                                        "stringutils                    0.0.1                meta-sample")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
