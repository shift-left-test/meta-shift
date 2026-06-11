#-*- coding: utf-8 -*-

"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""


def test_show_recipes(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes")
    assert o.stdout.matchesAll("autotools-project[ ]+1.0.0[ ]+meta-sample",
                               "cmake-project[ ]+1.0.0[ ]+meta-sample",
                               "humidifier-project[ ]+1.0.0[ ]+meta-sample",
                               "qmake-project[ ]+1.0.0[ ]+meta-sample",
                               "sqlite3wrapper[ ]+0.1.0[ ]+meta-sample")


def test_show_no_recipes_without_test_enabled(release_build):
    o = release_build.shell.execute("bitbake-layers test-recipes")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake-project",
                                    "sqlite3wrapper")


def test_show_recipes_with_pnspec(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes *-project")
    assert o.stdout.matchesAll("autotools-project[ ]+1.0.0[ ]+meta-sample",
                               "cmake-project[ ]+1.0.0[ ]+meta-sample",
                               "humidifier-project[ ]+1.0.0[ ]+meta-sample",
                               "qmake-project[ ]+1.0.0[ ]+meta-sample")
    assert not o.stdout.matchesAll("sqlite3wrapper[ ]+0.1.0[ ]+meta-sample")


def test_show_no_recipes_with_pnspec_without_test_enabled(release_build):
    o = release_build.shell.execute("bitbake-layers test-recipes *-project")
    assert not o.stdout.containsAny("autotools-project",
                                    "cmake-project",
                                    "humidifier-project",
                                    "qmake-project",
                                    "sqlite3wrapper")


def test_show_no_untestable_recipes(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes")
    assert not o.stdout.matchesAny(r"nativesdk-.+-project", r".+-project-native")


def test_show_recipes_with_image(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes --image core-image-minimal")
    assert o.stdout.matchesAll("autotools-project[ ]+1.0.0[ ]+meta-sample",
                               "cmake-project[ ]+1.0.0[ ]+meta-sample",
                               "humidifier-project[ ]+1.0.0[ ]+meta-sample",
                               "qmake-project[ ]+1.0.0[ ]+meta-sample",
                               "sqlite3wrapper[ ]+0.1.0[ ]+meta-sample")


def test_show_no_recipes_outside_image_graph(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes --image core-image-minimal")
    # testable, but not part of the image's build graph
    assert not o.stdout.containsAny("enact-project", "stringutils")


def test_show_recipes_with_image_and_pnspec(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes --image core-image-minimal *-project")
    assert o.stdout.matchesAll("autotools-project[ ]+1.0.0[ ]+meta-sample",
                               "cmake-project[ ]+1.0.0[ ]+meta-sample",
                               "humidifier-project[ ]+1.0.0[ ]+meta-sample",
                               "qmake-project[ ]+1.0.0[ ]+meta-sample")
    # sqlite3wrapper is in the image graph but fails the pnspec; enact-project
    # matches the pnspec but is outside the image graph -- both excluded.
    assert not o.stdout.containsAny("sqlite3wrapper", "enact-project", "stringutils")


def test_show_no_recipes_with_invalid_image(test_build):
    o = test_build.shell.execute("bitbake-layers test-recipes --image invalid-image-pn")
    assert o.returncode != 0


def test_show_header_with_image_and_zero_match(test_build):
    # stringutils is testable but outside core-image-minimal's graph: header
    # prints, zero data rows, normal exit.
    o = test_build.shell.execute("bitbake-layers test-recipes --image core-image-minimal stringutils")
    assert o.returncode == 0
    assert o.stdout.contains("recipe")
    assert not o.stdout.contains("stringutils")
