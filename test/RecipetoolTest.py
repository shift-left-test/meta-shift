#!/usr/bin/python

import pytest
import unittest
import yocto
from configure import config


class Inspect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=config["branch"], conf=config["bare"])

    def test_default_format(self):
        o = self.build.shell.execute("recipetool inspect cpplint")
        assert o["stdout"].containsAll("General Information",
                                       "-------------------",
                                       "Name: cpplint",
                                       "Summary: CPPLint - a static code analyzer for C/C++",
                                       "Description: A Static code analyzer for C/C++ written in python",
                                       "Author: Google Inc.",
                                       "Homepage: https://github.com/cpplint/cpplint",
                                       "Bugtracker: https://github.com/cpplint/cpplint/issues",
                                       "Section: devel/python",
                                       "License: BSD-3-Clause",
                                       "Version: 1.4.5",
                                       "Revision: r0",
                                       "Layer: meta-shift",
                                       "Testable: False")

    def test_json_format(self):
        o = self.build.shell.execute("recipetool inspect cpplint --json")
        assert o["stdout"].containsAll('"General Information": {',
                                       '"Author": "Google Inc."',
                                       '"Homepage": "https://github.com/cpplint/cpplint"',
                                       '"Layer": "meta-shift"',
                                       '"Bugtracker": "https://github.com/cpplint/cpplint/issues"',
                                       '"Summary": "CPPLint - a static code analyzer for C/C++"',
                                       '"Name": "cpplint"',
                                       '"Version": "1.4.5"',
                                       '"Section": "devel/python"',
                                       '"Revision": "r0"',
                                       '"Testable": false',
                                       '"License": "BSD-3-Clause"',
                                       '"Description": "A Static code analyzer for C/C++ written in python"')


class InspectWithRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=config["branch"], conf=config["release"])

    def test_cpp_project(self):
        o = self.build.shell.execute("recipetool inspect cpp-project")
        assert o["stdout"].containsAll("Name: cpp-project",
                                       "Layer: meta-sample",
                                       "Testable: False")


class InspectWithTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=config["branch"], conf=config["test"])

    def test_cpp_project(self):
        o = self.build.shell.execute("recipetool inspect cpp-project")
        assert o["stdout"].containsAll("Name: cpp-project",
                                       "Layer: meta-sample",
                                       "Testable: True")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
