#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import os
import re


class Output(object):
    """Holds a command/file output and provides comparison helpers.

    Every helper returns a bool; tests wrap them in ``assert``.
    """

    def __init__(self, output):
        self.output = output.strip()

    def empty(self):
        """Return True if the output is empty."""
        return not self.output

    def contains(self, keyword):
        """Return True if the output contains the keyword."""
        return keyword in self.output

    def containsAll(self, *keywords):
        """Return True if the output contains every keyword."""
        return all(self.contains(keyword) for keyword in keywords)

    def containsAny(self, *keywords):
        """Return True if the output contains any of the keywords."""
        return any(self.contains(keyword) for keyword in keywords)

    def matches(self, regexp):
        """Return True if the output matches the pattern (multiline search)."""
        return bool(re.compile(regexp, re.MULTILINE).search(self.output))

    def matchesAll(self, *regexps):
        """Return True if the output matches every pattern."""
        return all(self.matches(regexp) for regexp in regexps)

    def matchesAny(self, *regexps):
        """Return True if the output matches any of the patterns."""
        return any(self.matches(regexp) for regexp in regexps)

    def __repr__(self):
        return "'{0}'".format(self.output)

    def __str__(self):
        return self.__repr__()


class Outputs(object):
    def __init__(self, items=None):
        self.outputs = {}
        for key, value in (items or {}).items():
            self[key] = value

    def __setitem__(self, key, value):
        self.outputs[key] = value
        setattr(self, key, value)

    def __getitem__(self, key):
        return self.outputs[key]

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
