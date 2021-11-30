"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import sys
import os
import argparse
import glob
import fnmatch
import re
import logging
import scriptutils
import oe.recipeutils
import bb
import json
import subprocess
from collections import OrderedDict

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from shift_oelint_adv.__main__ import run  # nopep8
from shift_oelint_adv.rule_file import set_messageformat  # nopep8
from shift_oelint_adv.rule_file import set_suppressions  # nopep8

logger = logging.getLogger('recipetool')

tinfoil = None


def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


def make_plain_report(issues):
    return "\n".join([x[1] for x in issues]) + "\n"


def make_json_report(issues):
    json_dict = dict()
    json_dict["issues"] = list()
    for issue in issues:
        item = dict()
        split_data = issue[1].split(":")

        item["file"] = split_data[0]
        item["line"] = int(split_data[1])
        item["severity"] = split_data[2]
        item["rule"] = split_data[3]
        item["description"] = split_data[4]
        json_dict["issues"].append(item)

    return json.dumps(json_dict, indent=2) + "\n"


def check(args, files):
    class ArgForRun:
        def __init__(self):
            self.addrules = ["jetm"]
            self.customrules = []
            self.files = files
            self.quiet = True
            self.fix = False
            self.nobackup = False

    set_suppressions([
        "oelint.var.suggestedvar.BBCLASSEXTEND",
        "oelint.var.suggestedvar.CVE_PRODUCT",
        "oelint.task.customorder"
    ])
    set_messageformat("{path}:{line}:{severity}:{id}:{msg}")

    issues = run(ArgForRun())

    if args.output:
        output = open(args.output, "w")
        output.write(make_json_report(issues))
        output.close()

    sys.stderr.write(make_plain_report(issues))


def checkrecipes(args):
    logger.info("Checking the specified recipes or files for the styling issues...")
    files = []
    for recipe in args.recipes:
        if os.path.isfile(recipe):
            if recipe.split(".")[-1] in ["bb", "bbappend", "inc"]:
                files.append(recipe)
            else:
                sys.stderr.write("Not a BitBake file: '{}'\n".format(recipe))
        else:
            recipefile = oe.recipeutils.pn_to_recipe(tinfoil.cooker, recipe)
            if recipefile:
                files.append(recipefile)
                files.extend(tinfoil.cooker.collection.get_file_appends(recipefile))
            else:
                sys.stderr.write("Failed to find the recipe file for '{}'\n".format(recipe))
    check(args, files)
    logger.info("Done.")


def register_command(subparsers):
    check_parser = subparsers.add_parser('check',
                                         help="Check specified recipes or files for the OpenEmbedded Style Guide issues.",
                                         description="Check specified recipes or files for the OpenEmbedded Style Guide issues.")
    check_parser.add_argument("-o", "--output", help="save the output to a file")
    check_parser.add_argument("recipes", metavar="RECIPE", nargs='+', help="recipe or file to parse")
    check_parser.set_defaults(func=checkrecipes, parserecipes=True)
