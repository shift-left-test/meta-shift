# MIT License
#
# Copyright (c) 2020 LG Electronics, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import bb.utils
import fnmatch
import logging
import os
import re
import sys

logger = logging.getLogger('bitbake-layers')

tinfoil = None


def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


def is_testable(recipefile):
    return any("shifttest" == os.path.splitext(os.path.basename(inherit_class))[0] for
               inherit_class in tinfoil.cooker_data.inherits.get(recipefile, []))


def do_test_recipes(args):
    bbpath = str(tinfoil.config_data.getVar("BBPATH", True))

    classfile = "classes/shifttest.bbclass"
    if not bb.utils.which(bbpath, classfile, history=False):
        logger.error("Unable to locate %s in BBPATH", classfile)
        sys.exit(1)

    pkg_pn = tinfoil.cooker.recipecaches[''].pkg_pn
    (latest_versions, preferred_versions) = tinfoil.find_providers()

    print("{} {} {}".format("recipe".ljust(30), "version".ljust(20), "layer".ljust(20)))
    print("=" * 74)

    for p in sorted(pkg_pn):
        pref = preferred_versions[p]
        realfn = bb.cache.virtualfn2realfn(pref[1])
        preffile = realfn[0]
        layerdir = bb.utils.get_file_layer(preffile, tinfoil.config_data)

        if args.pnspec:
            if not fnmatch.fnmatch(p, args.pnspec):
                continue

        if not is_testable(preffile):
            continue

        print("{} {} {}".format(p.ljust(30), pref[0][1].ljust(20), layerdir.ljust(20)))


def register_commands(subparsers):
    parser = subparsers.add_parser("test-recipes",
                                   help="List testable recipes, showing the layer they are provided by",
                                   description="Lists the name and version of recipes in each layer. "
                                   "Optionally you may specify pnspec to match a specified recipe name (supports wildcards).")
    parser.add_argument("pnspec",
                        nargs="?",
                        help="optional recipe name specification (wildcards allowed, enclose in quotes to avoid shell expansion)")
    parser.set_defaults(func=do_test_recipes, parserecipes=True)
