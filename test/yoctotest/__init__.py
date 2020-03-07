#!/usr/bin/python

import os
import shutil
import subprocess
import tempfile


class Output(object):
    """The console output holder class.

    This class provides various output comparison helper functions.
    """

    def __init__(self, output):
        """Default constructor

        Args:
          output (str): a console output string
        """
        self.output = output

    def empty(self):
        """Assert that the output is empty

        Returns:
          True if the output is empty, False otherwise
        """
        return not self.output.strip()

    def contains(self, keyword):
        """Assert that the output contains the given keyword

        Args:
         keyword (str): text to examine

        Returns:
          True if the output contains the text, False otherwise
        """
        return keyword in self.output

    def containsAll(self, *keywords):
        for keyword in keywords:
            if not self.contains(keyword):
                return False
        return True

    def containsAny(self, *keywords):
        for keyword in keywords:
            if keyword in self.output:
                return True
        return False

    def __str__(self):
        """Print the console output string
        """
        return self.output


class YoctoBuildInfo(object):
    def __init__(self, workspace):
        self.workspace = workspace

    def readFile(self, path):
        with open(os.path.join(self.workspace, path), "r") as f:
            return f.read()

    def packages(self):
        return Output(self.readFile(os.path.join(self.workspace, "build/pn-buildlist")))

    def tasks(self):
        return Output(self.readFile(os.path.join(self.workspace, "build/task-depends.dot")))

    
class Phase(object):
    def __init__(self, outputs):
        """Default constructor

        Args:
          outputs (tuple): stderr and stdout
        """
        self.stdout = Output(outputs[0])
        self.stderr = Output(outputs[1])
   
    
class YoctoShell(object):
    COMMAND_WRAPPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "command-wrapper.sh")
    
    def __init__(self, workspace):
        self.workspace = workspace

    def run(self, command):
        proc = subprocess.Popen("{0} -w {1} -c \"{2}\"".format(self.COMMAND_WRAPPER, self.workspace, command), shell = True)
        return proc.wait()

    def execute(self, command):
        proc = subprocess.Popen("{0} -w {1} -c \"{2}\"".format(self.COMMAND_WRAPPER, self.workspace, command),
                                shell = True,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)
        return Phase(proc.communicate())

    
class YoctoTestEnvironment(object):
    PREPARE_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prepare-workspace.sh")

    def __init__(self, branch = "zeus"):
        self.workspace = os.path.join(*[tempfile.gettempdir(), "meta-testing", branch.lower().strip()])
        self.branch = branch.lower()

        if os.path.exists(self.workspace):
            print("Remove the existing workspace: %s" % self.workspace)
            shutil.rmtree(self.workspace)

        subprocess.Popen("{0} -w {1} -b {2}".format(self.PREPARE_SCRIPT, self.workspace, self.branch), shell = True).wait()

    def shell(self):
        return YoctoShell(self.workspace)


    def parse(self, target):
        YoctoShell(self.workspace).run("bitbake {0} -g".format(target))
        return YoctoBuildInfo(self.workspace)
