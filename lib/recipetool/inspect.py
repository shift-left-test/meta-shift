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
import bb
import json

logger = logging.getLogger('recipetool')

tinfoil = None


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

    def dump(self, output=sys.stdout):
        for line in self.result:
            output.write(line)


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

    def dump(self, output=sys.stdout):
        output.write(json.dumps(self.result, indent=2))
        output.write("\n")


def inspect(args):
    def is_testable(recipefile):
        return any("shifttest" == os.path.splitext(os.path.basename(inherit_class))[0] for
                   inherit_class in tinfoil.cooker_data.inherits.get(recipefile, []))

    if args.output:
        reporter = ReporterJson()
    else:
        reporter = Reporter()

    pn = args.recipename
    recipefile = tinfoil.cooker.findBestProvider(pn)[3]

    if recipefile is None:
        sys.stderr.write("Failed to find the recipe file for '{}'\n".format(pn))
        return

    appendfiles = tinfoil.cooker.collection.get_file_appends(recipefile)
    recipedata = tinfoil.parse_recipe_file(recipefile)
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
    reporter.add_value("Recipe", recipefile.split(":")[-1])  # To remove extra prefixes (e.g. virtual, nativesdk)
    reporter.add_value("Appends", appendfiles)
    reporter.add_value("SRC_URI", recipedata.getVar("SRC_URI", True).split())
    reporter.add_value("Work", recipedata.getVar("WORKDIR", True))
    reporter.add_value("Source", recipedata.getVar("S", True))
    reporter.add_value("Build", recipedata.getVar("B", True))
    reporter.add_value("Temp", recipedata.getVar("T", True))

    inherits = {}
    recipe_inherits = tinfoil.cooker_data.inherits.get(recipefile, [])
    for inherit_class in recipe_inherits:
        classname = os.path.splitext(os.path.basename(inherit_class))[0]
        inherits[classname] = inherit_class

    from collections import OrderedDict
    inherits = OrderedDict(sorted(inherits.items(), key=lambda t:t[0]))

    if args.recursive:
        dependedby_queue = [recipename]
        dependedby_set = set()
        pkg_fn_items = dict(tinfoil.cooker_data.pkg_fn)

        while len(dependedby_queue) > 0:
            p = dependedby_queue.pop()
            rf = tinfoil.cooker.findBestProvider(p)[3]
            if rf:
                rd = tinfoil.parse_recipe_file(rf)
                prvds = rd.getVar("PROVIDES", True).split()
                added_fn = []

                for fn, pn in pkg_fn_items.items():
                    if p == pn:
                        continue

                    if any((prov in tinfoil.cooker_data.deps[fn]) for prov in prvds):
                        if pn not in dependedby_set:
                            dependedby_set.add(pn)
                            dependedby_queue.append(pn)
                            added_fn.append(fn)

                for fn in added_fn:
                    del pkg_fn_items[fn]

        rec_dependedby = list(dependedby_set)

    dependedby = set()
    provides = sorted(recipedata.getVar("PROVIDES", True).split())
    for fn, pn in tinfoil.cooker_data.pkg_fn.items():
        if recipename == pn:
            continue
        if any((prov in tinfoil.cooker_data.deps[fn]) for prov in provides):
            dependedby.add(pn)
    dependedby = list(dependedby)

    if args.recursive:
        depends_queue = [recipename]
        depends_set = set()
        for k,v in tinfoil.cooker_data.rundeps[recipefile].items():
            depends_queue += v

        while len(depends_queue) > 0:
            p = depends_queue.pop()
            rf = tinfoil.cooker.findBestProvider(p)[3]
            if rf:
                for d in tinfoil.cooker_data.deps[rf]:
                    if d not in depends_set:
                        depends_set.add(d)
                        depends_queue.append(d)

                for k,v in tinfoil.cooker_data.rundeps[rf].items():
                    for d in v:
                      if d not in depends_set:
                          depends_queue.append(d)
                          if tinfoil.cooker.findBestProvider(d)[3]:
                              depends_set.add(d)

        rec_depends_real = set()
        for p in depends_set:
            rf = tinfoil.cooker.findBestProvider(p)[3]
            if rf and rf in tinfoil.cooker_data.pkg_fn:
                rec_depends_real.add(tinfoil.cooker_data.pkg_fn[rf])
            else:
                rec_depends_real.add(p)
        rec_depends_real = list(rec_depends_real)

    depends = tinfoil.cooker_data.deps[recipefile]
    depends_real = []
    for p in depends:
        rf = tinfoil.cooker.findBestProvider(p)[3]
        if rf and rf in tinfoil.cooker_data.pkg_fn:
            depends_real.append(tinfoil.cooker_data.pkg_fn[rf])
        else:
            depends_real.append(p)

    rdepends = tinfoil.cooker_data.rundeps[recipefile]
    rdepends = dict((k,sorted(v)) for k,v in rdepends.items())
    rdepends = OrderedDict(sorted(rdepends.items(), key=lambda t:t[0]))

    reporter.section("Dependencies")
    reporter.add_value("Inherits", inherits)
    reporter.add_value("Depends", sorted(depends_real))
    if args.recursive:
        reporter.add_value("Recursive Depends", sorted(rec_depends_real))
    reporter.add_value("Depended By", sorted(dependedby))
    if args.recursive:
        reporter.add_value("Recursive Depended By", sorted(rec_dependedby))
    reporter.add_value("RDepends", rdepends)
    reporter.add_value("Provides", provides)
    reporter.add_value("Packages", sorted(recipedata.getVar("PACKAGES", True).split()))

    output = open(args.output, "w") if args.output else sys.stdout
    reporter.dump(output)
    if args.output:
        output.close()


def register_commands(subparsers):
    parser = subparsers.add_parser("inspect",
                                   help="Inspect the specified recipe information",
                                   description="Inspect the specified recipe's detailed information, including file-path, version, meta-layer, append-file, dependencies, inherits, etc.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Show the list of Depends and Depends by recursively")
    parser.add_argument("-o", "--output", help="save the output to a file")
    parser.add_argument("recipename", help="Recipe name to inspect")
    parser.set_defaults(func=inspect, parserecipes=True)

