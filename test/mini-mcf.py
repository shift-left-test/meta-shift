#!/usr/bin/python

import argparse
import errno
import getpass
import os
import subprocess
import tempfile
import json
import logging
import constants


logging.basicConfig(level=logging.INFO, format="[ %(levelname)s ] %(message)s")
logger = logging.getLogger(__name__)

REPO_BASE_DIR = os.path.join(tempfile.gettempdir(), "meta-shift-repos-%s" % getpass.getuser())
DEFAULT_BRANCH = constants.BRANCH
DEFAULT_DIR = "build"

REPOS = {
    "poky": {"url": "http://mod.lge.com/hub/yocto/mirror/poky.git", "location": "poky", "layer": "poky/meta"},
    "meta-oe": {"url": "http://mod.lge.com/hub/yocto/mirror/meta-openembedded.git", "location": "meta-openembedded", "layer": "meta-openembedded/meta-oe"},
    "meta-python": {"url": "http://mod.lge.com/hub/yocto/mirror/meta-openembedded.git", "location": "meta-openembedded", "layer": "meta-openembedded/meta-python"},
    "meta-qt5": {"url": "http://mod.lge.com/hub/yocto/mirror/meta-qt5.git", "location": "meta-qt5", "layer": "meta-qt5"},
    "meta-clang": {"url": "http://mod.lge.com/hub/yocto/mirror/meta-clang.git", "location": "meta-clang", "layer": "meta-clang"},
    "meta-shift": {"url": os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "location": "meta-shift", "layer": "meta-shift"},
    "meta-sample": {"url": "http://mod.lge.com/hub/yocto/sample/meta-sample.git", "location": "meta-sample", "layer": "meta-sample"},
    "meta-sample-test": {"url": "http://mod.lge.com/hub/yocto/sample/meta-sample-test.git", "location": "meta-sample-test", "layer": "meta-sample-test"},
}


def parse_args():
    def exist_file(path):
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError("File not exist: {}".format(path))
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError("Not a file: {}".format(path))
        return path

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="branch", default=DEFAULT_BRANCH, help="Name of the branch to checkout for the git repositories (default: %s)" % DEFAULT_BRANCH)
    parser.add_argument("-c", type=exist_file, dest="filename", required=True, help="Configuration file path")
    parser.add_argument("-d", type=str, dest="directory", default=DEFAULT_DIR, help="Path to populate the build directory (default: %s)" % DEFAULT_DIR)
    parser.add_argument("-r", dest="repodir", default=REPO_BASE_DIR, help="Path to download the git repositories (default: %s)" % REPO_BASE_DIR)
    return parser.parse_args()


def execute(cmd):
    return subprocess.check_call(cmd, shell=True)


def download_repo(url, branch, path):
    if not os.path.exists(path):
        execute("git clone {} -b {} {}".format(url, branch, path))
    else:
        execute("git --git-dir={0}/.git --work-tree={0} checkout {1}".format(path, branch))
        execute("git --git-dir={0}/.git --work-tree={0} pull --ff-only".format(path))


def download_repos(args):
    logger.info("Downloading repos at {}...".format(args.repodir))
    for name, repo in REPOS.items():
        if name == "meta-shift":
            continue
        path = os.path.join(args.repodir, repo["location"])
        logger.info("REPO: {}".format(path))
        download_repo(repo["url"], args.branch, path)
    logger.info("Done")


def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def cleanup_build_conf(args):
    configures = [
        os.path.join(args.directory, "conf", "bblayers.conf"),
        os.path.join(args.directory, "conf", "local.conf")
    ]
    for configure in configures:
        if os.path.exists(configure):
            logger.warn("Removing the existing configuration file: {}".format(configure))
            os.remove(configure)


def configure_bblayers(args):
    logger.info("Initializing bblayers.conf...")
    commands = []
    commands.append("source {}/{}/oe-init-build-env {}".format(args.repodir, REPOS["poky"]["location"], args.directory))
    conf = read_json(args.filename)
    for include in conf["includes"]:
        path = os.path.join(args.repodir, REPOS[include]["layer"]) if include != "meta-shift" else REPOS[include]["url"]
        commands.append("bitbake-layers add-layer {}".format(path))
    execute('bash -c "{}"'.format("; ".join(commands)))
    logger.info("Done")


def configure_local(args):
    logger.info("Initializing local.conf...")
    local_conf = os.path.join(args.directory, "conf", "local.conf")
    conf = read_json(args.filename)
    for key, value in conf["local.conf"].items():
        value = os.environ.get(key, value)
        with open(local_conf, "a") as f:
            f.write('{} = "{}"\n'.format(key, value))
    logger.info("Done")


def print_usage(args):
    print("""\n\n\n### Shell environment set up command ###

    source {0}/poky/oe-init-build-env {1}

    """.format(args.repodir, args.directory))


if __name__ == "__main__":
    args = parse_args()
    download_repos(args)
    cleanup_build_conf(args)
    configure_bblayers(args)
    configure_local(args)
    print_usage(args)
