#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import re


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

    def matchesAny(self, *regexps):
        """Assert that the output contains text which the patterns match

        Args:
          regexp (str): search patterns

        Returns:
          True if the output contains matching text, False otherwise
        """
        for regexp in regexps:
            if self.matches(regexp):
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

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


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


class FileOutput(Output):
    def __init__(self, filename):
        self.filename = filename
        with open(os.path.join(filename), "r") as f:
            super(FileOutput, self).__init__(f.read())

    def __repr__(self):
        return "{0}: {1}".format(self.filename, super(FileOutput, self).__repr__())
