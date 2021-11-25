"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

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
    (latest_versions, preferred_versions, required) = tinfoil.find_providers()

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

        # Ignore untestable recipes
        if p.startswith("nativesdk-") or p.endswith("-native"):
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
