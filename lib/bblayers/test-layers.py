# MIT License
#
# Copyright (c) 2020 Sung Gon Kim
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
import logging
import os
import re
import sys

logger = logging.getLogger('bitbake-layers')

tinfoil = None


def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


def find_top_directory():
    """
    Find the parent directory of the poky meta-layer

    :return: the base path
    """
    return os.path.dirname(tinfoil.config_data.getVar("COREBASE", True))


def is_test_configured(layerconf):
    """
    Check if the given layer is test-configured

    :param layerconf: path to the layer.conf
    :return: True if the layer is test-configured, False otherwise
    """
    regexp = re.compile("^LAYERDEPENDS_(?:.*)\"(?:.*)meta-shift(?:.*)\"", re.MULTILINE)
    with open(layerconf, "r") as f:
        return regexp.search(f.read())


def get_layername(layerconf):
    """
    Extract the layer name from layer.conf

    :param layerconf: path to the layer.conf
    :return: layername
    """
    regexp = re.compile("^(?:BBFILE_COLLECTIONS)(?:.+)(?:\")(.+)(?:\")", re.MULTILINE)
    with open(layerconf, "r") as f:
        return regexp.search(f.read()).groups()[0]


def find_layers_from(basepath):
    """
    Find the test-configured layers from the given base directory

    :param basepath: base path to look up
    :return: test-configure layers
    """
    layers = []
    for root, dirs, files in os.walk(basepath):
        for d in dirs:
            if d.startswith("."):
                continue

            layerconf = os.path.join(root, d, "conf", "layer.conf")
            if not os.path.exists(layerconf):
                continue

            if not is_test_configured(layerconf):
                continue

            name = get_layername(layerconf)
            path = os.path.abspath(os.path.join(root, d))
            layers.append((name, path))

    return sorted(layers, key=lambda x: x[0])


def show(layers):
    """
    Show the test-configure layers

    :param layers: meta-layers
    """
    print("{} {}".format("layer".ljust(20), "path".ljust(40)))
    print("=" * 74)
    for layername, layerdir in layers:
        print("{} {}".format(layername.ljust(20), layerdir.ljust(40)))


def add(layers):
    layernames = []
    for layername, layerdir in layers:
        """Add a layer to bblayers.conf."""
        if layername in layernames:
            sys.stderr.write("Warning: Layer %s in %s is ignored. Another layer with same name is already in BBLAYERS.\n" % (layername, layerdir))
            continue
        else:
            layernames.append(layername)

        bblayers_conf = os.path.join('conf', 'bblayers.conf')
        if not os.path.exists(bblayers_conf):
            sys.stderr.write("Unable to find bblayers.conf\n")
            return

        notadded, _ = bb.utils.edit_bblayers_conf(bblayers_conf, layerdir, None)
        if notadded:
            sys.stderr.write("Specified layer %s is already in BBLAYERS\n" % layerdir)
            continue

        sys.stdout.write("Added: %s\n" % layerdir)


def remove(layers):
    for _, layerdir in layers:
        """Remove a layer from bblayers.conf."""
        bblayers_conf = os.path.join('conf', 'bblayers.conf')
        if not os.path.exists(bblayers_conf):
            sys.stderr.write("Unable to find bblayers.conf\n")
            return

        (_, notremoved) = bb.utils.edit_bblayers_conf(bblayers_conf, None, layerdir)
        if notremoved:
            sys.stderr.write("No layers matching %s found in BBLAYERS\n" % layerdir)
            continue

        sys.stdout.write("Removed: %s\n" % layerdir)


def process(args):
    """
    Process the sub-command

    :param args: arguments
    """
    basepath = args.basepath if args.basepath else find_top_directory()
    layers = find_layers_from(basepath)

    if args.add:
        add(layers)
    elif args.remove:
        remove(layers)
    else:
        show(layers)


def register_commands(subparsers):
    parser = subparsers.add_parser("test-layers",
                                   help="Show, add or remove test-configured layers.",
                                   description="Show, add or remove test-configured layers.")
    parser.add_argument("--basepath", help="base path to search test-configured layers")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--show", action="store_true", help="show test-configured layers")
    group.add_argument("--add", action="store_true", help="add test-configured layers to bblayers.conf")
    group.add_argument("--remove", action="store_true", help="remove test-configured layers from bblayers.conf")
    parser.set_defaults(func=process, parserecipes=False)
