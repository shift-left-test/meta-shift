#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.parsers.data import multidict
from xml.parsers import expat


class XMLReportParser(object):
    def __init__(self, data):
        self.data = data
        self.tags = []
        self.parser = expat.ParserCreate()
        self.parser.StartElementHandler = self.handle_starttag
        self.parser.EndElementHandler = self.handle_endtag
        self.parser.CharacterDataHandler = self.handle_data

    def add(self, value):
        self.data["/".join(self.tags)] = value

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if attrs:
            self.add(dict(attrs))

    def handle_endtag(self, tag):
        if self.tags[-1] == tag:
            self.tags.pop()

    def handle_data(self, data):
        if data.strip():
            self.add(data.strip())

    def feed(self, text):
        self.parser.Parse(text)


def parse(path):
    with open(path, "r") as f:
        data = multidict()
        parser = XMLReportParser(data)
        parser.feed(f.read())
        return data
