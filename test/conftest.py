#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import getpass
import os
import pytest
import re
import shutil
import subprocess
import time


def findFiles(*paths):
    import glob
    found = glob.glob(os.path.join(*paths))
    assert len(found) > 0
    return found


class Output(object):
    """The output holder class

    This class provides variout output comparison helper functions.
    """

    def __init__(self, output):
        """ Default constructor

        Args:
          output (str): an output string
        """
        self.output = output.strip()

    def empty(self):
        """Assert that the output is empty

        Returns:
          True if the output is empty, False otherwise
        """
        return not self.output

    def contains(self, keyword):
        """Assert that the output contains the given keyword

        Args:
          keyword (str): keyword to examine

        Returns:
          True if the output contains the keyword, False otherwise
        """
        return keyword in self.output

    def containsAll(self, *keywords):
        """Assert that the output contains all the given keywords

        Args:
          keywords (str): keywords to examine

        Returns:
          True if the output contains all the keywords, False otherwise
        """
        for keyword in keywords:
            if not self.contains(keyword):
                return False
        return True

    def containsAny(self, *keywords):
        """Assert that the output contains any of the given keywords

        Args:
          keywords (str): keywords to examine

        Returns:
          True if the output contains any of the keywords, False otherwise
        """
        for keyword in keywords:
            if self.contains(keyword):
                return True
        return False

    def matches(self, regexp):
        """Assert that the output contains text which the patten matches

        Args:
          regexp (str): search pattern

        Returns:
          True if the output contains matching text, False otherwise
        """
        matcher = re.compile(regexp, re.MULTILINE)
        return bool(matcher.search(self.output))


    def matchesAll(self, *regexps):
        """Assert that the output contains text which the patterns match

        Args:
          regexp (str): search patterns

        Returns:
          True if the output contains matching text, False otherwise
        """
        for regexp in regexps:
            if not self.matches(regexp):
                return False
        return True

    def __repr__(self):
        """Output string
        """
        return "'{0}'".format(self.output)

    def __str__(self):
        """Output string
        """
        return self.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class FileOutput(Output):
    def __init__(self, filename):
        self.filename = filename
        with open(os.path.join(filename), "r") as f:
            super(FileOutput, self).__init__(f.read())

    def __repr__(self):
        return "{0}: {1}".format(self.filename, super(FileOutput, self).__repr__())


class Files(object):
    def __init__(self, build_dir):
        self.build_dir = build_dir

    def __repr__(self):
        return "Files: ['build_dir': {0}]".format(self.build_dir)

    def exists(self, path):
        return os.path.exists(os.path.join(self.build_dir, path))

    def read(self, path):
        return FileOutput(findFiles(self.build_dir, path)[0])

    def remove(self, path):
        f = os.path.join(self.build_dir, path)
        if os.path.isfile(f):
            os.remove(f)
        if os.path.isdir(f):
            shutil.rmtree(f)


class Outputs(object):
    def __init__(self, kwargs={}):
        self.outputs = {}
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __setitem__(self, key, value):
        self.outputs[key] = value
        setattr(self, key, self.outputs[key])

    def __getitem__(self, key):
        return self.outputs[key]

    def __delitem__(self, key):
        self.outputs.pop(key)
        delattr(self, key)

    def keys(self):
        return self.outputs.keys()

    def __repr__(self):
        data = ", ".join("'{0}': {1}".format(key, value) for (key, value) in self.outputs.items())
        return "{0}: {{{1}}}".format(type(self).__name__, data)

    def __str__(self):
        return self.__repr__()


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
        proc = subprocess.Popen(self.cmd(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        streams = proc.communicate()
        return Outputs({
            "stdout": Output(streams[0].decode("utf-8")),
            "stderr": Output(streams[1].decode("utf-8")),
            "returncode": proc.returncode})


class BuildEnvironment(object):
    def __init__(self, conf_file, repo_dir, build_dir):
        self.repo_dir = repo_dir
        self.branch = "honister"
        self.conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), conf_file)
        self.build_dir = build_dir
        self.initWorkspace()

    def initWorkspace(self):
        mini_mcf = os.path.join(os.path.dirname(__file__), "mini-mcf.py")
        cmd = "{} -r {} -b {} -c {} -d {}".format(mini_mcf, self.repo_dir, self.branch, self.conf_file, self.build_dir)
        subprocess.call(cmd, shell=True)

    @property
    def shell(self):
        def wait_until(condition, timeout, period=1):
            until = time.time() + timeout
            while time.time() < until:
                if condition:
                    return True
                time.sleep(period)
            return False

        f = os.path.join(self.repo_dir, "poky", "oe-init-build-env")
        assert os.path.exists(f)
        assert wait_until(not os.path.exists(os.path.join(self.build_dir, "hashserve.lock")), 10)
        return Shell(f, self.build_dir)

    @property
    def files(self):
        return Files(self.build_dir)


@pytest.fixture(scope="session")
def bare_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/bare.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def release_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/release.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def test_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/test.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def test_qt6_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/test_qt6.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def report_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/report.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def report_qt6_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/report_qt6.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def test_clang_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/test_clang.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def test_clang_qt6_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/test_clang_qt6.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def report_clang_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/report_clang.conf", repo_dir=repo_dir, build_dir=build_dir)


@pytest.fixture(scope="session")
def report_clang_qt6_build(request, tmpdir_factory):
    repo_dir = str(tmpdir_factory.mktemp("repo"))
    build_dir = str(tmpdir_factory.mktemp("build"))

    def cleanup():
        shutil.rmtree(repo_dir)
        shutil.rmtree(build_dir)

    request.addfinalizer(cleanup)
    return BuildEnvironment(conf_file="conf/report_clang_qt6.conf", repo_dir=repo_dir, build_dir=build_dir)
