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
# THE SOFTWARE

import os
import shutil
import logging
import tempfile
from devtool import setup_tinfoil, recipe_to_append, DevtoolError, parse_recipe
from lib.devtool.standard import modify, reset, get_default_srctree, _extract_source

logger = logging.getLogger("devtool")
logger.setLevel(logging.WARNING)


def clone(args, config, basepath, clone_workspace):
    """Modify the source for an existing recipe and change the source revision to fetch
    """
    srctree = None
    tinfoil = setup_tinfoil(basepath=basepath, tracking=True)
    if not tinfoil:
        # Error already shown
        return 1
    try:
        rd = parse_recipe(config, tinfoil, args.recipename, True)
        if not rd:
            raise DevtoolError("Failed to parse recipe")

        pn = rd.getVar('PN', True)
        recipefile = rd.getVar('FILE', True)

        if args.srctree:
            srctree = os.path.abspath(args.srctree)
        else:
            srctree = get_default_srctree(config, pn)

        tinfoil.config_data.setVar("SRCREV_pn-%s" % pn, args.srcrev)

        initial_rev = _extract_source(srctree, args.keep_temp, args.branch, False, rd, tinfoil)
        if not initial_rev:
            raise DevtoolError("Failed to extract source")
    except:
        if srctree and os.path.exists(srctree):
            shutil.rmtree(srctree)
        raise
    finally:
        while True:
            try:
                tinfoil.shutdown()
            except:
                tinfoil.wait_event(0.25)
            else:
                break

    args.no_extract = True
    ret = modify(args, config, basepath, clone_workspace)
    try:
        if ret != 0:
            raise DevtoolError("Failed to modify source")

        appendfile = recipe_to_append(recipefile, config, args.wildcard)
        if not os.path.exists(appendfile):
            raise DevtoolError("Failed to find bbappend file")
        try:
            with open(appendfile, 'a') as f:
                f.write('\nSRCREV = "%s"\n' % (args.srcrev))
        except:
            raise DevtoolError("Failed to add new source revision to bbappend file")
    except:
        bb.process.run('devtool reset %s --remove-work' % args.recipename)
        raise

    return ret


def register_commands(subparsers, context):
    defsrctree = get_default_srctree(context.config)

    parser_modify = subparsers.add_parser('clone', help='Modify the source for an existing recipe and change the source revision to fetch',
                                       description='Exactly same as devtool-modify, except that the source revision is changed',
                                       group='starting', order=89)
    parser_modify.add_argument('recipename', help='Name of existing recipe to edit (just name - no version, path or extension)')
    parser_modify.add_argument('srcrev', help='Source revision to fetch if fetching from an SCM such as git')
    parser_modify.add_argument('srctree', nargs='?', help='Path to external source tree. If not specified, a subdirectory of %s will be used.' % defsrctree)
    parser_modify.add_argument('--wildcard', '-w', action="store_true", help='Use wildcard for unversioned bbappend')
    group = parser_modify.add_mutually_exclusive_group()
    group.add_argument('--same-dir', '-s', help='Build in same directory as source', action="store_true")
    group.add_argument('--no-same-dir', help='Force build in a separate build directory', action="store_true")
    parser_modify.add_argument('--branch', '-b', default="devtool", help='Name for development branch to checkout (when not using -n/--no-extract) (default "%(default)s")')
    parser_modify.add_argument('--keep-temp', help='Keep temporary directory (for debugging)', action="store_true")
    parser_modify.set_defaults(func=clone)

