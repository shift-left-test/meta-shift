#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from contextlib import contextmanager
from selftest.input import Conf
from selftest.output import FileOutput
from selftest.parsers import HTML
from selftest.parsers import JSON
from selftest.parsers import XML
from selftest.util import findFiles
import os
import shutil


class Files(object):
    def __init__(self, build_dir):
        self.build_dir = build_dir

    def __repr__(self):
        return "Files: ['build_dir': {0}]".format(self.build_dir)

    def exists(self, path):
        return os.path.exists(os.path.join(self.build_dir, path))

    @contextmanager
    def conf(self):
        with self.tempfile("extra.conf") as f:
            yield Conf(f)

    @contextmanager
    def tempfile(self, filename=None):
        if not filename:
            filename = randomString(7)
        self.remove(filename)
        yield os.path.join(self.build_dir, filename)
        self.remove(filename)

    def read(self, path):
        return FileOutput(findFiles(self.build_dir, path)[0])

    def readAsJson(self, path):
        return JSON.parse(os.path.join(self.build_dir, path))

    def readAsXml(self, path):
        return XML.parse(os.path.join(self.build_dir, path))

    def readAsHtml(self, path):
        return HTML.parse(os.path.join(self.build_dir, path))

    def remove(self, path):
        f = os.path.join(self.build_dir, path)
        if os.path.isfile(f):
            os.remove(f)
        if os.path.isdir(f):
            shutil.rmtree(f)
