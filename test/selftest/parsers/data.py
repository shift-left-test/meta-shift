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


def asList(node):
    """Normalize a parsed report node to a list.

    The XML/HTML parsers yield a single value for a lone element and a list
    when the tag repeats, so callers that iterate must coerce uniformly.
    A missing node (None) becomes an empty list.
    """
    if node is None:
        return []
    return node if isinstance(node, list) else [node]
