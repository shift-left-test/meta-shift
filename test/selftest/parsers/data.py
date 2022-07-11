#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


class multidict(dict):
    def __setitem__(self, key, value):
        try:
            self[key].append(value)
        except KeyError:
            super(multidict, self).__setitem__(key, value)
        except AttributeError:
            super(multidict, self).__setitem__(key, [self[key], value])
