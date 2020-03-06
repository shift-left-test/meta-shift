#!/usr/bin/python

import os
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover(os.path.dirname(__file__), pattern="*Test.py")
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)
