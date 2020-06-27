#!/usr/bin/python

import pytest
import re


def test_mutually_exclusive_options(release_build):
    assert not release_build.shell.execute("bitbake-layers test-layers --show --add").stderr.empty()
    assert not release_build.shell.execute("bitbake-layers test-layers --show --remove").stderr.empty()
    assert not release_build.shell.execute("bitbake-layers test-layers --add --remove").stderr.empty()


def test_default_action(release_build):
    o = release_build.shell.execute("bitbake-layers test-layers")
    assert o.stdout.contains("meta-sample-test")


def test_show_layers(release_build):
    o = release_build.shell.execute("bitbake-layers test-layers --show")
    assert o.stdout.contains("meta-sample-test")


def test_show_with_basepath(release_build):
    o = release_build.shell.execute("bitbake-layers test-layers --show --basepath /dev/null")
    assert not o.stdout.contains("meta-sample-test")


def test_add_layers(release_build):
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    release_build.shell.execute("bitbake-layers test-layers --add")
    assert release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    release_build.shell.execute("bitbake-layers test-layers --remove")
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")


def test_add_layers_twice(test_build):
    assert test_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    o = test_build.shell.execute("bitbake-layers test-layers --add")
    regexp = re.compile("Specified layer .+/meta-sample-test is already in BBLAYERS", re.MULTILINE)
    assert bool(re.match(regexp, o.stderr.output))


def test_remove_layers(test_build):
    assert test_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    test_build.shell.execute("bitbake-layers test-layers --remove")
    assert not test_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    test_build.shell.execute("bitbake-layers test-layers --add")
    assert test_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")


def test_remove_layers_twice(release_build):
    assert not release_build.shell.execute("bitbake-layers show-layers").stdout.contains("meta-sample-test")
    o = release_build.shell.execute("bitbake-layers test-layers --remove")
    regexp = re.compile("No layers matching .+/meta-sample-test found in BBLAYERS", re.MULTILINE)
    assert bool(re.match(regexp, o.stderr.output))
