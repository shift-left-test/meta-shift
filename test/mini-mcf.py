#!/usr/bin/python

import argparse
import errno
import getpass
import os
import shutil
import subprocess
import tempfile
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PWD = os.path.dirname(os.path.abspath(__file__))
REPO_BASE_DIR = os.path.join(*[tempfile.gettempdir(), "meta-shift-repos", getpass.getuser()])
DEFAULT_BRANCH = "morty"

repos = {
    "poky": { "url": "http://mod.lge.com/hub/yocto/poky.git", "location": "poky", "layer": "poky/meta" },
    "meta-oe": { "url": "http://mod.lge.com/hub/yocto/meta-openembedded.git", "location": "meta-openembedded", "layer": "meta-openembedded/meta-oe" },
    "meta-python": { "url": "http://mod.lge.com/hub/yocto/meta-openembedded.git", "location": "meta-openembedded", "layer": "meta-openembedded/meta-python" },
    "meta-sample": { "url": "http://mod.lge.com/hub/yocto/meta-sample.git", "location": "meta-sample", "layer": "meta-sample" },
    "meta-sample-test": { "url": "http://mod.lge.com/hub/yocto/meta-sample-test.git", "location": "meta-sample-test", "layer": "meta-sample-test" },
}

def getopts():
    def exist_file(path):
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError("File not exist: {}".format(path))
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError("Not a file: {}".format(path))
        return path

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="branch", default=DEFAULT_BRANCH, help="Name of the branch to checkout for the git repositories (default: %s)" % DEFAULT_BRANCH)
    parser.add_argument("-c", type=exist_file, dest="filename", required=True, help="Configuration file path")
    parser.add_argument("-d", type=str, dest="directory", required=True, help="Path to populate the build directory")
    parser.add_argument("-r", dest="repodir", help="Path to download the git repositories (default: %s)" % REPO_BASE_DIR, default=REPO_BASE_DIR)
    return parser.parse_args()

def execute(cmd):
    return subprocess.call(cmd, shell=True)

def downloadRepos(repodir, branch):
    if os.path.exists(REPO_BASE_DIR):
        logger.info("Remove the git repositories: {}".format(REPO_BASE_DIR))
        shutil.rmtree(REPO_BASE_DIR)

    for name, repo in repos.items():
        path = os.path.join(repodir, repo["location"])
        execute("git clone {} -b {} {}".format(repo["url"], branch, path))

def initBuildEnv(repodir, directory):
    path = os.path.join(repodir, repos["poky"]["location"])
    execute('bash -c "source {}/oe-init-build-env {}"'.format(path, directory))

def configure(repodir, directory, filename):
    with open(filename, "r") as f:
        conf = json.load(f)

    bblayers_conf = os.path.join(directory, "conf/bblayers.conf")

    with open(bblayers_conf, "a") as f:
        f.write('BBLAYERS_append = " {}"\n'.format(os.path.abspath(os.path.dirname(PWD))))

    for include in conf["includes"]:
        path = os.path.abspath(os.path.join(repodir, repos[include]["layer"]))
        with open(bblayers_conf, "a") as f:
            f.write('BBLAYERS_append = " {}"\n'.format(path))

    local_conf = os.path.join(directory, "conf/local.conf")
    for key, value in conf["local.conf"].items():
        with open(local_conf, "a") as f:
            f.write('{} = "{}"\n'.format(key, value.replace("${HOME}", os.path.expanduser("~"))))


if __name__ == "__main__":
    options = getopts()

    logger.info("Downloading repos at {0}...".format(options.repodir))
    downloadRepos(options.repodir, options.branch)
    logger.info("Done.")

    logger.info("Initialzing build environment...")
    initBuildEnv(options.repodir, options.directory)
    logger.info("Done.")

    logger.info("Configuring files...")
    configure(options.repodir, options.directory, options.filename)
    logger.info("Done.")
