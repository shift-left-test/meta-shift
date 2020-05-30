#!/usr/bin/python

import atexit
import os
import getpass
import logging
import subprocess
import shutil
import tempfile
import unittest


logging.basicConfig(level=logging.INFO, format="'%(asctime)s - %(message)s'")
logger = logging.getLogger(__name__)

TempDirectories = []

@atexit.register
def removeTempDirectories():
    for tempdir in TempDirectories:
        logger.info("Remove the temp build directory: {0}".format(tempdir))
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)


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

    def __repr__(self):
        """Output string
        """
        return "'{0}'".format(self.output)

    def __str__(self):
        """Output string
        """
        return self.__repr__()


class FileOutput(Output):
    def __init__(self, filename):
        self.filename = filename
        with open(os.path.join(filename), "r") as f:
            super(FileOutput, self).__init__(f.read())

    def __repr__(self):
        return "{0}: {1}".format(self.filename, super(FileOutput, self).__repr__())


class Files(object):
    def __init__(self, builddir):
        self.builddir = builddir

    def __repr__(self):
        return "Files: ['builddir': {0}]".format(self.builddir)

    def exists(self, path):
        return os.path.exists(os.path.join(self.builddir, path))

    def read(self, path):
        f = os.path.join(self.builddir, path)
        assert os.path.exists(f)
        return FileOutput(f)

    def rmdir(self, path):
        f = os.path.join(self.builddir, path)
        if os.path.exists(f):
            shutil.rmtree(f)

class Outputs(object):
    def __init__(self, kwargs = {}):
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
    def __init__(self, script, builddir):
        self.script = script
        self.builddir = builddir

    def __repr__(self):
        return "Shell: ['script': {0}, 'builddir': {1}]".format(self.script, self.builddir)

    def cmd(self, command):
        return 'bash -c "source {0} {1} && {2}"'.format(self.script, self.builddir, command)

    def run(self, command):
        subprocess.call(self.cmd(command), shell=True)

    def execute(self, command, env=None):
        proc = subprocess.Popen(self.cmd(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        streams = proc.communicate()
        return Outputs({ "stdout": Output(streams[0]), "stderr": Output(streams[1]), "returncode": proc.returncode })


class BuildInfo(object):
    def __init__(self, builddir):
        def readFile(path):
            with open(path, "r") as f:
                return f.read()

        self.builddir = builddir
        self.packages = FileOutput(os.path.join(builddir, "pn-buildlist"))
        self.tasks = FileOutput(os.path.join(builddir, "task-depends.dot"))

        @property
        def packages(self):
            return self.packages

        @property
        def tasks(self):
            return self.tasks


class BuildEnvironment(object):
    def __init__(self, branch, conf):
        self.repodir = os.path.join(tempfile.gettempdir(), "meta-shift-repos-%s" % getpass.getuser())
        self.branch = branch
        self.conf = os.path.join(*[os.path.dirname(__file__), conf])
        self.builddir = tempfile.mkdtemp()
        TempDirectories.append(self.builddir)

        mini_mcf = os.path.join(os.path.dirname(__file__), "mini-mcf.py")
        cmd = "{} -r {} -b {} -c {} -d {}".format(mini_mcf, self.repodir, self.branch, self.conf, self.builddir)
        subprocess.call(cmd, shell=True)

    def __repr__(self):
        return "BuildEnvironment: ['repodir': {0}, 'branch': {1}, 'conf': {2}, 'builddir': {3}]".format(self.repodir, self.branch, self.conf, self.builddir)

    @property
    def shell(self):
        f = os.path.join(self.repodir, "poky/oe-init-build-env")
        assert os.path.exists(f)
        return Shell(f, self.builddir)

    @property
    def files(self):
        return Files(self.builddir)

    def parse(self, recipe):
        self.shell.run("bitbake {0} -g".format(recipe))
        return BuildInfo(self.builddir)
