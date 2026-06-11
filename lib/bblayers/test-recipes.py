"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import bb.utils
import fnmatch
import logging
import os
import sys

logger = logging.getLogger('bitbake-layers')

tinfoil = None


def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


def is_testable(recipefile):
    return any("shifttest" == os.path.splitext(os.path.basename(inherit_class))[0] for
               inherit_class in tinfoil.cooker_data.inherits.get(recipefile, []))


def image_recipe_closure(image):
    """Collect the PNs reachable from the image via build and runtime deps.

    Mirrors do_testall's recrdeptask traversal (DEPENDS + RDEPENDS) so the
    listing matches what 'bitbake <image> -c testall' would actually run.
    """
    cooker_data = tinfoil.cooker_data
    if not tinfoil.cooker.findBestProvider(image)[3]:
        logger.error("Unable to find a recipe providing image '%s'", image)
        sys.exit(1)

    pns = set()
    visited = set()
    queue = [image]
    while queue:
        p = queue.pop()
        if p in visited:
            continue
        visited.add(p)
        fn = tinfoil.cooker.findBestProvider(p)[3]
        if not fn:
            continue
        pn = cooker_data.pkg_fn.get(fn)
        if pn:
            pns.add(pn)
        queue.extend(cooker_data.deps.get(fn, []))
        for rdeps in cooker_data.rundeps.get(fn, {}).values():
            queue.extend(rdeps)
    return pns


def do_test_recipes(args):
    bbpath = str(tinfoil.config_data.getVar("BBPATH", True))

    classfile = "classes/shifttest.bbclass"
    if not bb.utils.which(bbpath, classfile, history=False):
        logger.error("Unable to locate %s in BBPATH", classfile)
        sys.exit(1)

    image_recipes = image_recipe_closure(args.image) if args.image else None

    pkg_pn = tinfoil.cooker.recipecaches[''].pkg_pn
    (latest_versions, preferred_versions, required) = tinfoil.find_providers()

    print("{} {} {}".format("recipe".ljust(30), "version".ljust(20), "layer".ljust(20)))
    print("=" * 74)

    for p in sorted(pkg_pn):
        if image_recipes is not None and p not in image_recipes:
            continue

        if args.pnspec:
            if not fnmatch.fnmatch(p, args.pnspec):
                continue

        pref = preferred_versions[p]
        realfn = bb.cache.virtualfn2realfn(pref[1])
        preffile = realfn[0]
        layerdir = bb.utils.get_file_layer(preffile, tinfoil.config_data)

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
                                   "Optionally restrict the listing to an image's build graph with --image, "
                                   "and/or match recipe names with pnspec (supports wildcards).")
    parser.add_argument("--image",
                        help="restrict the listing to recipes in the given image's build graph")
    parser.add_argument("pnspec",
                        nargs="?",
                        help="optional recipe name specification (wildcards allowed, enclose in quotes to avoid shell expansion)")
    parser.set_defaults(func=do_test_recipes, parserecipes=True)
