#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


class Conf(object):
    def __init__(self, path):
        self.path = path

    def set(self, key, value):
        with open(self.path, "a+") as f:
            f.write('%s = "%s"\n' % (key, value))
