"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import bb.utils
import logging
import os
import sys

logger = logging.getLogger("bitbake-layers")

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


def status(args):
    def getVar(key, default=""):
        return tinfoil.config_data.getVar(key, True) or default

    def hasVar(key):
        return key in tinfoil.config_data.keys()

    def bblayers():
        layerconfs = tinfoil.config_data.varhistory.get_variable_items_files("BBFILE_COLLECTIONS", tinfoil.config_data)
        for name, path in layerconfs.items():
            layerdir = os.path.dirname(os.path.dirname(path))
            yield os.path.basename(layerdir), name, layerdir

    def findFiles(path, suffix=".conf"):
        if not os.path.exists(path):
            return []
        return [ os.path.splitext(os.path.basename(f))[0] for f in os.listdir(path) if f.endswith(suffix) ]

    def findAllImages():
        images = []
        pkg_pn = tinfoil.cooker.recipecaches[''].pkg_pn
        (latest_versions, preferred_versions) = bb.providers.findProviders(tinfoil.config_data, tinfoil.cooker.recipecaches[''], pkg_pn)
        for p in sorted(pkg_pn):
            pref = preferred_versions[p]
            realfn = bb.cache.virtualfn2realfn(pref[1])
            preffile = realfn[0]
            if not any("core-image" == os.path.splitext(os.path.basename(inherit_class))[0] for
                       inherit_class in tinfoil.cooker_data.inherits.get(preffile, [])):
                continue
            images.append(p)
        return sorted(images)

    report = Reporter()

    report.section("Project Configuration")
    report.add_value("Machine", getVar("MACHINE"))
    report.add_value("Codename", getVar("LAYERSERIES_CORENAMES", "unknown"))
    report.add_value("Distro", getVar("DISTRO"))
    report.add_value("Parallelism", hasVar("BB_NUMBER_THREADS"))
    report.add_value("own-mirrors", bb.utils.contains("INHERIT", "own-mirrors", "True", "False", tinfoil.config_data))

    machines = []
    distros = []
    for layer, name, layerdir in bblayers():
        machines.extend(findFiles(os.path.join(layerdir, "conf", "machine")))
        distros.extend(findFiles(os.path.join(layerdir, "conf", "distro")))

    report.section("Additional Information")
    report.add_value("Images", findAllImages())
    report.add_value("Machines", sorted(machines))
    report.add_value("Distros", sorted(distros))

    report.dump()


def register_commands(subparsers):
    parser = subparsers.add_parser("status",
                                   help="Show the detailed information on the project.",
                                   description="Return the detailed information on the project including images, machines, distros, etc.")
    parser.set_defaults(func=status, parserecipes=True)
