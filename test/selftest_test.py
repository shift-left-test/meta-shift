#-*- coding: utf-8 -*-

"""
Copyright (c) 2026 LG Electronics Inc.
SPDX-License-Identifier: MIT

Pure unit tests for the selftest support library. Unlike the rest of the
suite these run without a Yocto workspace, so they execute under a plain
`pytest test/selftest_test.py`.
"""

from selftest.output import Output, Outputs
from selftest.parsers.data import asList, multidict


def test_asList_scalar_list_and_none():
    assert asList("x") == ["x"]
    assert asList(["a", "b"]) == ["a", "b"]
    assert asList(None) == []


def test_output_predicates():
    o = Output("alpha beta gamma")
    assert o.contains("beta")
    assert o.containsAll("alpha", "gamma")
    assert o.containsAny("zeta", "gamma")
    assert not o.containsAny("zeta", "delta")
    assert o.matches(r"alpha .* gamma")
    assert Output("").empty()


def test_outputs_attribute_access_and_no_shared_default():
    a = Outputs({"returncode": 0})
    b = Outputs()
    assert a.returncode == 0
    assert b.outputs == {}


def test_multidict_collapses_repeated_keys():
    d = multidict()
    d["k"] = "1"
    d["k"] = "2"
    d["once"] = "v"
    assert d["k"] == ["1", "2"]
    assert d["once"] == "v"
