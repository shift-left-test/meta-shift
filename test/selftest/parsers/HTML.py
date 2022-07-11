#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from selftest.parsers import XML
import re


def parse(path):
    with open(path, "r") as f:
        xmltext = f.read()

        # To avoid failing when parsing html
        xmltext = xmltext.replace("&nbsp;%"," ")
        xmltext = re.sub("<![^>\n]*>", "", xmltext)
        xmltext = re.sub("=([0-9]+)", r'="\1"',xmltext)
        xmltext = re.sub("<meta[^>\n]*>", "", xmltext)
        xmltext = re.sub("<link[^>\n]*>", "", xmltext)
        xmltext = re.sub("<img[^>\n]*>", "", xmltext)
        xmltext = re.sub("<br>", "", xmltext)

        return XML.parseString(xmltext)
