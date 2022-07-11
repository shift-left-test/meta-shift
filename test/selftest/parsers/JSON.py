#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import json


def parse(path):
    with open(path, "r") as f:
        return json.load(f)
