#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from html.parser import HTMLParser
from selftest.parsers.data import multidict


class HTMLReportParser(HTMLParser):
    def __init__(self, data):
        super(HTMLReportParser, self).__init__()
        self.data = data
        self.tags = []

    def add(self, value):
        self.data["/".join(self.tags)] = value

    def handle_starttag(self, tag, attrs):
        # Ignore HTML void elements
        # https://www.w3.org/TR/2011/WD-html-markup-20110113/syntax.html#syntax-elements
        if tag in ["area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"]:
            return
        self.tags.append(tag)
        if attrs:
            self.add(dict(attrs))

    def handle_endtag(self, tag):
        if self.tags[-1] == tag:
            self.tags.pop()

    def handle_data(self, data):
        if data.strip():
            self.add(data.strip())


def parse(path):
    with open(path, "r") as f:
        data = multidict()
        parser = HTMLReportParser(data)
        parser.feed(f.read())
        return data
