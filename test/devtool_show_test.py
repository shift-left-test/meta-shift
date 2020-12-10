#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 Sung Gon Kim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

def test_show_global_unknown_variable(bare_build):
    o = bare_build.shell.execute("devtool show UNKNOWN_VARIABLE")
    assert o.stdout.contains("WARNING: Requested variable 'UNKNOWN_VARIABLE' does not exist")


def test_show_global_variables(bare_build):
    o = bare_build.shell.execute("devtool show TUNE_ARCH BUILD_ARCH")
    assert o.stdout.containsAll('BUILD_ARCH="{BUILD_ARCH}"',
                                'TUNE_ARCH="{TUNE_ARCH}"')

def test_show_global_unexpanded_variables(bare_build):
    o = bare_build.shell.execute("devtool show MACHINE_ARCH -u")
    assert o.stdout.contains("# MACHINE_ARCH=${{@[d.getVar('TUNE_PKGARCH'), d.getVar('MACHINE')][bool(d.getVar('MACHINE'))].replace('-', '_')}}")


def test_show_global_variable_flags(bare_build):
    o = bare_build.shell.execute("devtool show BUILD_ARCH -f")
    assert o.stdout.contains('BUILD_ARCH[doc]="The name of the building architecture (e.g. i686)."')


def test_show_unknown_recipe(bare_build):
    o = bare_build.shell.execute("devtool show -r UNKNOWN_RECIPE TUNE_ARCH")
    assert o.stdout.contains("ERROR: Failed to find the recipe file for 'UNKNOWN_RECIPE'")


def test_show_recipe_unknown_variable(bare_build):
    o = bare_build.shell.execute("devtool show -r cmake UNKNOWN_VARIABLE")
    assert o.stdout.contains("WARNING: Requested variable 'UNKNOWN_VARIABLE' does not exist")


def test_show_recipe_variable(bare_build):
    o = bare_build.shell.execute("devtool show -r cmake cmake_do_configure")
    assert not o.stdout.contains("bbnote () {{")
    assert o.stdout.contains("cmake_do_configure () {{")


def test_show_recipe_dependent_variables(bare_build):
    o = bare_build.shell.execute("devtool show -r cmake cmake_do_configure -x")
    assert o.stdout.contains("bbnote () {{")
    assert o.stdout.contains("cmake_do_configure () {{")
