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
# THE SOFTWARE

import bb
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from devtool import setup_tinfoil, DevtoolError


logger = logging.getLogger("devtool")
logger.setLevel(logging.WARNING)


class Task(object):
    """Task representation class
    """
    def __init__(self, tid, pn, task):
        self.tid = tid
        self.pn = pn
        self.task = task[:-9] if task.endswith("_setscene") else task

    def isSetsceneTask(self):
        return self.tid.endswith("_setscene")

    def __str__(self):
        return "%s:%s" % (self.pn, self.task)

    def __repr__(self):
        return self.__str__()


def get_tasks(args, basepath):
    """Return the relevant taks of the given recipe
    """
    def execute(cmd, env=None):
        try:
            output = subprocess.check_output(cmd,
                                             stderr=subprocess.STDOUT,
                                             env=env,
                                             shell=True)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            logger.error("bitbake failed: \n%s" % e.output.decode("utf-8"))
            sys.exit(e.returncode)

    try:
        tmpdir = tempfile.mkdtemp(prefix="devtool-cache-")

        env = os.environ.copy()
        env["BB_ENV_EXTRAWHITE"] = env.get("BB_ENV_EXTRAWHITE", "") + " TMPDIR_forcevariable"
        env["TMPDIR_forcevariable"] = tmpdir

        output = execute("bitbake %s -n" % args.recipe, env=env)

        tids = []
        matcher = re.compile("NOTE: Running(?: setscene)? task [0-9]+ of [0-9]+ \(([^)]+)\)")
        for line in output.splitlines():
            matched = matcher.match(line)
            if matched:
                tids.append(matched.group(1))
    finally:
        shutil.rmtree(tmpdir)

    try:
        tinfoil = setup_tinfoil(config_only=False, basepath=basepath)
        tasks = []
        for tid in tids:
            (mc, fn, taskname) = bb.runqueue.split_tid(tid)
            tasks.append(Task(tid, tinfoil.cooker.recipecaches[mc].pkg_fn[fn], taskname))

        tasks.sort(key=lambda x: (x.pn, x.task))
        return tasks

    finally:
        tinfoil.shutdown()


def print_variables(args, title, found, missed):
    wanted = len(found) + len(missed)

    print(title)
    print("-" * len(title))
    print("Wanted : %d (%d%%)" % (wanted, wanted / wanted * 100))
    print("Found  : %d (%d%%)" % (len(found), len(found) / wanted * 100))
    if args.found:
        for task in found:
            print("    %s" % task)
    print("Missed : %d (%d%%)" % (len(missed), len(missed) / wanted * 100))
    if args.missed:
        for task in missed:
            print("    %s" % task)
    print()


def cache(args, config, basepath, workspace):
    """Show the shared state cache status of the recipe
    """
    print("INFO: This might take a few minutes to complete...")
    try:
        tasks = get_tasks(args, basepath)
        print_variables(args, "Local Cache Statistics",
                        [x for x in tasks if x.isSetsceneTask()],
                        [x for x in tasks if not x.isSetsceneTask()])
        return 0
    except Exception as e:
        logger.error(str(e))
        return 2


def register_commands(subparsers, context):
    parser = subparsers.add_parser("cache",
                                   help="Show the shared state cache status of the recipe",
                                   description="Show the shared state cache status of the recipe",
                                   group="info")
    parser.add_argument("recipe", help="recipe to examine")
    parser.add_argument("-f", "--found", action="store_true", help="Show the list of cached tasks")
    parser.add_argument("-m", "--missed", action="store_true", help="Show the list of missed tasks")
    parser.set_defaults(func=cache, no_workspace=True)
