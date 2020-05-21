# Recipe creation tool - recipe infomation retrieval plugin
#
# Copyright (C) 2020 Sung Gon Kim
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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

logger = logging.getLogger('recipetool')

tinfoil = None
plugins = None

def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


class Reporter:
    def __init__(self):
        self.result = []

    def section(self, section_name):
        self.result.append("\n%s\n%s\n" % (section_name, ('-' * len(section_name))))


    def add_value(self, key, value):
        if isinstance(value, dict):
            self.result.append("%s:\n" % key)
            for v_key in sorted(value.keys()):
                v_value = value[v_key]
                self.result.append("    %s: %s\n" % (v_key, v_value))
        elif isinstance(value, list):
            self.result.append("%s:\n" % key)
            for v_value in sorted(value):
                self.result.append("    %s\n" % v_value)
        else:
            self.result.append("%s: " % key)
            self.result.append("%s\n" % value)

    def dump(self):
        for line in self.result:
            sys.stdout.write(line)


class ReporterJson(Reporter):
    def __init__(self):
        self.result = {}
        self.current_section = None


    def section(self, section_name):
        self.current_section = {}
        self.result[section_name] = self.current_section


    def add_value(self, key, value):
        self.current_section[key] = value
        pass


    def dump(self):
        sys.stdout.write(json.dumps(self.result, indent=2))
        sys.stdout.write("\n")


def retrieve(args):
    def is_testable(recipefile):
        return any("shifttest" == os.path.splitext(os.path.basename(inherit_class))[0] for
                   inherit_class in tinfoil.cooker_data.inherits.get(recipefile, []))

    if args.json:
        reporter = ReporterJson()
    else:
        reporter = Reporter()

    pn = args.recipename
    recipefile = oe.recipeutils.pn_to_recipe(tinfoil.cooker, pn)

    if recipefile is None:
        print("Fail to find recipefile for '{}'".format(pn))
        return

    appendfiles = tinfoil.cooker.collection.get_file_appends(recipefile)
    recipedata = oe.recipeutils.parse_recipe(tinfoil.cooker, recipefile, appendfiles)
    recipename = tinfoil.cooker_data.pkg_fn[recipefile]

    reporter.section("General Information")
    reporter.add_value("Name", recipename)
    reporter.add_value("Summary", recipedata.getVar("SUMMARY", True))
    reporter.add_value("Description", recipedata.getVar("DESCRIPTION", True))
    reporter.add_value("Author", recipedata.getVar("AUTHOR", True))
    reporter.add_value("Homepage", recipedata.getVar("HOMEPAGE", True))
    reporter.add_value("Bugtracker", recipedata.getVar("BUGTRACKER", True))
    reporter.add_value("Section", recipedata.getVar("SECTION", True))
    reporter.add_value("License", recipedata.getVar("LICENSE", True))
    reporter.add_value("Version", recipedata.getVar("PV", True))
    reporter.add_value("Revision", recipedata.getVar("PR", True))
    reporter.add_value("Layer", bb.utils.get_file_layer(recipefile, tinfoil.config_data))
    reporter.add_value("Testable", is_testable(recipefile))

    reporter.section("Additional Information")
    reporter.add_value("BBFile", recipefile)
    reporter.add_value("Appends", appendfiles)
    reporter.add_value("SRC_URI", recipedata.getVar("SRC_URI", True).split())
    reporter.add_value("Work", recipedata.getVar("WORKDIR", True))
    reporter.add_value("Source", recipedata.getVar("S", True))
    reporter.add_value("Build", recipedata.getVar("B", True))

    reporter.section("Dependencies")
    inherits = {}
    recipe_inherits = tinfoil.cooker_data.inherits.get(recipefile, [])
    for inherit_class in recipe_inherits:
        classname = os.path.splitext(os.path.basename(inherit_class))[0]
        inherits[classname] = inherit_class
    provides = tinfoil.cooker_data.fn_provides[recipefile]
    dependedby = []

    for fn, pn in tinfoil.cooker_data.pkg_fn.items():
        if recipename == pn:
            continue

        if any((prov in tinfoil.cooker_data.deps[fn]) for prov in provides):
            dependedby.append(pn)

    reporter.add_value("Inherits", inherits)
    reporter.add_value("Depends", tinfoil.cooker_data.deps[recipefile])
    reporter.add_value("Depended By", dependedby)
    reporter.add_value("RDepends", tinfoil.cooker_data.rundeps[recipefile])
    reporter.add_value("Provides", provides)
    reporter.add_value("Packages", recipedata.getVar("PACKAGES", True).split())

    reporter.dump()


def register_commands(subparsers):
    parser_info = subparsers.add_parser('info',
                                          help='Retrieve recipe information',
                                          description='Retrieve recipe file-path, version, meta-layer, append-file, dependencies, inherits, etc.')
    parser_info.add_argument('-j', '--json', help='Dump as the json format', action='store_true')
    parser_info.add_argument('recipename', help='Recipe name to retrieve')
    parser_info.set_defaults(func=retrieve, parserecipes=True)
