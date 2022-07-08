#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from contextlib import contextmanager
from selftest.util import findFiles
from selftest.output import FileOutput
from selftest.output import XmlOutput
from selftest.input import Conf
import json
import os
import re
import shutil
import xml.etree.ElementTree as ET


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
        with open(os.path.join(self.build_dir, path), "r") as f:
            return json.load(f)

    def readAsXml(self, path):
        tree = ET.parse(os.path.join(self.build_dir, path))
        root = tree.getroot()
        return  XmlOutput(root)

    def readAsHtml(self, path):
        with open(os.path.join(self.build_dir, path), "r") as f:
            xmltext = f.read()

            # To avoid failing when parsing html
            xmltext = xmltext.replace("&nbsp;%"," ")
            xmltext = re.sub("<![^>\n]*>", "", xmltext)
            xmltext = re.sub("=([0-9]+)", r'="\1"',xmltext)
            xmltext = re.sub("<meta[^>\n]*>", "", xmltext)
            xmltext = re.sub("<link[^>\n]*>", "", xmltext)
            xmltext = re.sub("<img[^>\n]*>", "", xmltext)
            xmltext = re.sub("<br>", "", xmltext)

        root = ET.fromstring(xmltext)
        return  XmlOutput(root)

    def remove(self, path):
        f = os.path.join(self.build_dir, path)
        if os.path.isfile(f):
            os.remove(f)
        if os.path.isdir(f):
            shutil.rmtree(f)
