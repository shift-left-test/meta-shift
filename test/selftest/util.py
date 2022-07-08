#-*- coding: utf-8 -*-

"""
Copyright (c) 2022 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import glob
import os
import random
import string
import time


def findFiles(*paths):
    found = glob.glob(os.path.join(*paths))
    assert len(found) > 0
    return found


def randomString(length=10):
    return "".join(random.sample(string.ascii_lowercase, length))


def wait_until(condition, timeout, period=1):
    until = time.time() + timeout
    while time.time() < until:
        if condition:
            return True
        time.sleep(period)
    return False
