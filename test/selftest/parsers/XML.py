#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import xml.etree.ElementTree as ET


class XmlOutput(object):
    """The xml output holder class

    This class provides xml output comparison helper functions.
    """

    def __init__(self, root):
        """ Default constructor

        Args:
          root (Element): root Element of xml.etree.ElementTree
        """
        self.root = root

    def containsElement(self, element_name):
        """Assert that the root contains the element with the given name

        Args:
          element_name (str): element name to examine

        Returns:
          True if the root contains element that meets the condition, False otherwise
        """
        find = False
        for e in self.root.iter(element_name):
            find = True
            break

        return find

    def containsElementWithAttrib(self, element_name, attributes):
        """Assert that the root contains the element with the given attributes

        Args:
          element_name (str): element name to examine
          attributes (dict): name, value pair to examine

        Returns:
          True if the root contains element that meets the condition, False otherwise
        """
        find = False
        for e in self.root.iter(element_name):
            match = True

            for key in attributes:
                if key in e.attrib:
                    if e.attrib[key] != attributes[key]:
                        match = False
                        break
                else:
                    match = False
                    break

            if match:
                find = True
                break

        return find

    def containsElementWithText(self, element_name, text):
        """Assert that the root contains the element with the given text

        Args:
          element_name (str): element name to examine
          text (str): element's text to examine

        Returns:
          True if the root contains element that meets the condition, False otherwise
        """
        find = False
        for e in self.root.iter(element_name):
            if text == e.text:
                find = True
                break

        return find


def parse(path):
    with open(path, "r") as f:
        tree = ET.parse(path)
        root = tree.getroot()
        return XmlOutput(root)


def parseString(string):
    root = ET.fromstring(string)
    return XmlOutput(root)
