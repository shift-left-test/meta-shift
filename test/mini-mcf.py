#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

from __future__ import print_function
import argparse
import collections
import getpass
import json
import logging
import os
import shutil
import subprocess
import tempfile


BRANCH = "nanbield"
REPO_DIR = os.path.join(tempfile.gettempdir(), "meta-shift-repos-%s" % getpass.getuser())
BUILD_DIR = "build"
META_SHIFT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


Repo = collections.namedtuple("Repo", ["name", "url", "location", "layer", "branch"])

REPOS = [
    Repo("poky", "https://git.yoctoproject.org/git/poky.git", "poky", "meta", None),
    Repo("meta-poky", "https://git.yoctoproject.org/git/poky.git", "poky", "meta-poky", None),
    Repo("meta-yocto-bsp", "https://git.yoctoproject.org/git/poky.git", "poky", "meta-yocto-bsp", None),
    Repo("meta-oe", "https://github.com/openembedded/meta-openembedded.git", "meta-openembedded", "meta-oe", None),
    Repo("meta-multimedia", "https://github.com/openembedded/meta-openembedded.git", "meta-openembedded", "meta-multimedia", None),
    Repo("meta-python", "https://github.com/openembedded/meta-openembedded.git", "meta-openembedded", "meta-python", None),
    Repo("meta-networking", "https://github.com/openembedded/meta-openembedded.git", "meta-openembedded", "meta-networking", None),
    Repo("meta-raspberrypi", "https://git.yoctoproject.org/git/meta-raspberrypi.git", "meta-raspberrypi", "", "master"),
    Repo("meta-qt5", "https://github.com/meta-qt5/meta-qt5.git", "meta-qt5", "", "master"),
    Repo("meta-qt6", "https://code.qt.io/yocto/meta-qt6.git", "meta-qt6", "", "6.5"),
    Repo("meta-clang", "https://github.com/kraj/meta-clang.git", "meta-clang", "", None),
    Repo("meta-shift", None, "meta-shift", "", None),
    Repo("meta-sample", "https://github.com/shift-left-test/meta-sample.git", "meta-sample", "", None),
    Repo("meta-sample-test", "https://github.com/shift-left-test/meta-sample-test.git", "meta-sample-test", "", None),
]


def parse_args():
    def exist_file(path):
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError("File not exist: {}".format(path))
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError("Not a file: {}".format(path))
        return path

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--branch", default=BRANCH, help="Name of the branch to checkout for the repositories (default: %(default)s)")
    parser.add_argument("-c", "--conf_file", type=exist_file, required=True, help="Configuration file path")
    parser.add_argument("-d", "--build_dir", type=str, default=BUILD_DIR, help="Path to populate the build directory (default: %(default)s)")
    parser.add_argument("-r", "--repo_dir", default=REPO_DIR, help="Path to download the repositories (default: %(default)s)")
    return parser.parse_args()


def execute(cmd):
    return subprocess.check_call(cmd, shell=True)


def download_repo(url, branch, path):
    logger.info(url)
    if os.path.exists(path):
        print("[INFO] Removing '%s'..." % path)
        shutil.rmtree(path)
    execute("git clone {0} -b {1} --depth 1 {2}".format(url, branch, path))


def download_repos(args):
    def getOrDefault(value, defaultValue):
        return value if value else defaultValue

    logger.info("Downloading the repositories to '{0}'...".format(args.repo_dir))
    done  = []
    for repo in REPOS:
        if repo.name == "meta-shift":
            continue
        p = os.path.join(args.repo_dir, repo.location)
        if not repo.url in done:
            download_repo(repo.url, getOrDefault(repo.branch, args.branch), p)
            done.append(repo.url)


def configure_template(conf_dir):
    logger.info("Creating 'templateconf.cfg'...")
    with open(os.path.join(conf_dir, "templateconf.cfg"), "w") as f:
        f.write("meta-poky/conf")


def configure_bblayers(conf_dir, conf_data, repo_dir):
    logger.info("Creating 'bblayers.conf'...")
    BBLAYERS_CONF = '''# POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
# changes incompatibly
POKY_BBLAYERS_CONF_VERSION = "2"

BBPATH = "${{TOPDIR}}"
BBFILES ?= ""

BBLAYERS ?= " \\
  {metalayers} \\
  "
'''
    bblayers_conf = os.path.join(conf_dir, "bblayers.conf")
    metalayers = []
    for repo in REPOS:
        if repo.name not in conf_data["includes"]:
            continue
        if repo.name == "meta-shift":
            layerdir = META_SHIFT_DIR
        else:
            layerdir = os.path.join(repo_dir, repo.location, repo.layer)
        metalayers.append(os.path.abspath(layerdir))

    with open(bblayers_conf, "w") as f:
        f.write(BBLAYERS_CONF.format(metalayers="  \\ \n  ".join(metalayers)))


def configure_local(conf_dir, conf_data):
    logger.info("Creating 'local.conf'...")
    LOCAL_CONF = '''
DISTRO = "sample"
PACKAGE_CLASSES = "package_ipk"
EXTRA_IMAGE_FEATURES = ""
USER_CLASSES = ""
PATCHRESOLVE = "noop"
BB_DISKMON_DIRS ??= "\\
    STOPTASKS,${TMPDIR},1G,100K \\
    STOPTASKS,${DL_DIR},1G,100K \\
    STOPTASKS,${SSTATE_DIR},1G,100K \\
    STOPTASKS,/tmp,100M,100K \\
    HALT,${TMPDIR},100M,1K \\
    HALT,${DL_DIR},100M,1K \\
    HALT,${SSTATE_DIR},100M,1K \\
    HALT,/tmp,10M,1K"
PACKAGECONFIG:append:pn-qemu-native = " sdl"
PACKAGECONFIG:append:pn-nativesdk-qemu = " sdl"
CONF_VERSION = "2"
INHIBIT_PACKAGE_DEBUG_SPLIT = "1"
'''
    local_conf = os.path.join(conf_dir, "local.conf")
    with open(local_conf, "w") as f:
        f.write(LOCAL_CONF)

        for key, value in conf_data["local.conf"].items():
            value = os.environ.get(key, value)
            f.write('{} ?= "{}"\n'.format(key, value))

        f.write("include /etc/meta-shift/global.conf\n")
        f.write("include ${TOPDIR}/extra.conf\n")


def configure(args):
    def read_json(filename):
        with open(filename, "r") as f:
            return json.load(f)

    conf_dir = os.path.join(args.build_dir, "conf")
    if not os.path.exists(conf_dir):
        logger.info("Creating '{}'...".format(conf_dir))
        os.makedirs(conf_dir)

    conf_data = read_json(args.conf_file)

    configure_template(conf_dir)
    configure_bblayers(conf_dir, conf_data, args.repo_dir)
    configure_local(conf_dir, conf_data)


def print_usage(args):
    print("""\n\n\n### Shell environment set up command ###

    source {0}/poky/oe-init-build-env {1}

    """.format(args.repo_dir, args.build_dir))


if __name__ == "__main__":
    args = parse_args()
    download_repos(args)
    configure(args)
    print_usage(args)
