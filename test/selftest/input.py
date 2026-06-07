#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


class Conf(object):
    def __init__(self, path):
        self.path = path

    def set(self, key, value):
        # set() appends one line per call to a fresh tempfile; values are wrapped
        # in double quotes, so a value containing one would corrupt the conf.
        assert '"' not in str(value), "Conf value must not contain a double quote: {!r}".format(value)
        with open(self.path, "a+") as f:
            f.write('%s = "%s"\n' % (key, value))
