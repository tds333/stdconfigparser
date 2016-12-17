#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest
import json

from stdconfigparser import (StdConfigParser, InterpolationMissingOptionError,
                             ParsingError, MissingSectionHeaderError)


def test_init():
    parser = StdConfigParser()
    assert parser
    parser = StdConfigParser(defaults={u"mydefault": u"true"})
    assert parser
    assert parser.getboolean(u"DEFAULT", u"mydefault")
    parser = StdConfigParser(converters={u"bool": bool})
    assert parser
    assert parser.getbool(u"DEFAULT", u"notthere", fallback=True)


def test_simple():
    parser = StdConfigParser()
    test = u"""
    [test]
    key = value
    key2: value2
    key3 = value =
    key4: value:
    [test:]
    key:= v
    key2=: v
    [test=]
    $=$
    [more]
    empty=
    """
    parser.read_string(test)
    assert u"value" == parser.get(u"test", u"key")
    assert u"value" == parser[u"test"][u"key"]
    assert u"value2" == parser.get(u"test", u"key2")
    assert u"value =" == parser.get(u"test", u"key3")
    assert u"value:" == parser.get(u"test", u"key4")
    assert u"= v" == parser.get(u"test:", u"key")
    assert u": v" == parser.get(u"test:", u"key2")
    assert u"test=" in parser.sections()
    assert u"$" == parser.get(u"test=", u"$")
    assert u"" == parser.get(u"more", u"empty")
    assert u"" == parser.get(u"more", u"nokey", fallback="")
    assert u"xyz" == parser.get(u"more", u"nokey", vars={u"nokey": u"xyz"})
    assert u"xyz" == parser.get(u"test", u"key", vars={u"key": u"xyz"})


def test_missing_section():
    parser = StdConfigParser()
    test = u"""
    key = value
    """
    with pytest.raises(MissingSectionHeaderError):
        parser.read_string(test)


def test_default_section():
    parser = StdConfigParser()
    test = u"""
    [DEFAULT]
    key = vd
    key2 = default
    [test]
    key = value
    """
    parser.read_string(test)
    assert u"value" == parser[u"test"][u"key"]
    assert u"default" == parser[u"test"][u"key2"]
    assert u"vd" == parser[u"DEFAULT"][u"key"]
    vars = {u"key3": u"three", u"key2": u"vars"}
    assert u"three" == parser.get(u"test", u"key3", vars=vars)
    assert u"vars" == parser.get(u"test", u"key2", vars=vars)


def test_getlines():
    parser = StdConfigParser()
    test = u"""
    [test]
    multiline = 1
        2
        3
        4
    """
    parser.read_string(test)
    lines = parser.getlines(u"test", u"multiline")
    assert len(lines) > 0
    assert [str(i) for i in range(1, 5)] == lines


def test_getlines_trim():
    parser = StdConfigParser()
    test = u"""
    [test]
    multiline =
        \tvalue 1\t
          value 2   """
    parser.read_string(test)
    lines = parser.getlines(u"test", u"multiline")
    assert len(lines) > 0
    assert [u"value 1", u"value 2"] == lines


def test_getlisting():
    parser = StdConfigParser()
    test = u"""
    [test]
    listing = value 1,value 2, value 3 , v4
    list_empty = v1,,v2, ,v3
    """
    parser.read_string(test)
    li = parser.getlisting(u"test", u"listing")
    assert len(li) > 0
    assert [u"value 1", u"value 2", u"value 3", u"v4"] == li
    li = parser.getlisting(u"test", u"list_empty")
    assert [u"v1", u"v2", u"v3"] == li


def test_getlisting_multi():
    parser = StdConfigParser()
    test = u"""
    [test]
    listing = value 1,
        value 2, value 3
         , v4
    """
    parser.read_string(test)
    li = parser.getlisting(u"test", u"listing")
    assert len(li) > 0
    assert [u"value 1", u"value 2", u"value 3", u"v4"] == li


def test_getjson():
    parser = StdConfigParser(converters={u"json": json.loads})
    test = u"""
    [test]
    list = [1,2,3, "4"]
    object = {"a": "val b", "b": 1.7}
    string = "xyz"
    number = 10000000
    float = 3.14
    """
    parser.read_string(test)
    sec = parser[u"test"]
    assert sec.getjson(u"list") == [1,2,3, u"4"]
    assert sec.getjson(u"object") == {u"a": u"val b", u"b": 1.7}
    assert sec.getjson(u"string") == u"xyz"
    assert sec.getjson(u"number") == 10000000
    assert sec.getjson(u"float") == 3.14


def test_interpolation():
    parser = StdConfigParser(interpolate=True)
    test = u"""
    [DEFAULT]
    a = 100
    [test]
    x = 0
    value_a = ${a}
    value_x = ${x}
    value_ix = ${i:x}
    value_y = ${y}
    value_iy = ${i:y}
    [i]
    x = 1
    y = 2
    """
    parser.read_string(test)
    sec = parser[u"test"]
    assert sec.getint(u"x") == 0
    assert sec[u"x"] == u"0"
    assert sec[u"value_a"] == u"100"
    assert sec[u"value_x"] == u"0"
    assert sec[u"value_ix"] == u"1"
    assert sec[u"value_iy"] == u"2"
    with pytest.raises(InterpolationMissingOptionError):
        sec[u"value_y"]


def test_sectioninterpolation():
    parser = StdConfigParser(interpolate=True)
    test = u"""
    [test]
    x = 0
    value_x = ${x}
    value_ix = ${inter:sec:x}
    value_iy = ${inter:sec:y}
    value_is = ${:strange::::::::::sec::s}
    [inter:sec]
    x = 1
    [:strange::::::::::sec:]
    s = 9
    """
    parser.read_string(test)
    sec = parser[u"test"]
    assert sec.getint(u"x") == 0
    assert sec[u"x"] == u"0"
    assert sec[u"value_x"] == u"0"
    assert sec[u"value_ix"] == u"1"
    with pytest.raises(InterpolationMissingOptionError):
        sec[u"value_iy"]
    assert sec[u"value_is"] == u"9"


def test_conv_error():
    parser = StdConfigParser()
    test = u"""
    [test]
    int = 100
    bool = true
    string = bla
    float = 3.14
    """
    parser.read_string(test)
    sec = parser[u"test"]
    assert sec.getint(u"int") == 100
    with pytest.raises(ValueError):
        assert sec.getint(u"string")
    with pytest.raises(ValueError):
        assert sec.getfloat(u"string")
    with pytest.raises(ValueError):
        assert sec.getboolean(u"string")


def test_ParsingError():
    parser = StdConfigParser()
    test = u"""
    [test]
    int @ 100
    """
    with pytest.raises(ParsingError):
      parser.read_string(test)
    parser = StdConfigParser()
    test = u"""
    [test
    ]
    """
    with pytest.raises(ParsingError):
      parser.read_string(test)


def test_complex():
    example = u"""
[mysection]
a = b
list = [1,
  # second
  2,4,
  "last",
  # empty line

  true,
  null,
  [1,2]
  , {"1":2}
  , "${int}"
  , "${name}"
  , "$${name}"
  ]
dict = {"a": 1, "b": 2}
multiline = first value
  some_text
  more_than_one_line

    and somethind with spaces
  # comment
       space end    \

  ${int}
  ${section2:name2}
  end

int = 1
float = 1.555
name = My troublesome name

[section2]
name2 = ${mysection:name}

[sec.one]
name = bla
[sec.two]
name = ${sec.one:name}

[my one]
name=one
[my two]
name=two
[my t3]
[my t4]
[my t5]
[my t6]
name=${my one:name}

[json]
list = [1,2,3]
object = {"a": "myval", "b": "otherval"}
with_comment = [1, "200",
    # comment

    "400", true, false, null, 3.14,
    {"another": 5,
     "second": "bla"}]
not_invalid =
  ["a", "b"]
"""

    parser = StdConfigParser(converters={u"json": json.loads}, interpolate=True)
    parser.read_string(example)
    assert parser.get(u"mysection", u"name") == u"My troublesome name"
    assert parser.get(u"section2", u"name2") == u"My troublesome name"
    assert parser.getjson(u"mysection", u"dict") == {u"a": 1, u"b": 2}
    #assert parser.getjson(u"mysection", u"list") == []
    #assert parser.getlines(u"mysection", u"multiline") == []
    assert parser.get(u"sec.two", u"name") == u"bla"
    assert parser.get(u"my two", u"name") == u"two"
    assert parser.get(u"my t6", u"name") == u"one"
    assert parser.getjson(u"json", u"list") == [1,2,3]
    assert parser.getjson(u"json", u"object") == {u"a": u"myval", u"b": u"otherval"}
    assert parser.getjson(u"json", u"with_comment") == [1, u"200", u"400", True,
                                                      False, None, 3.14,
                                                      {u"another": 5,
                                                       u"second": u"bla"}]
    assert parser.getjson(u"json", u"not_invalid") == [u"a", u"b"]
    assert parser.getjson(u"json", u"invalid", fallback="not found") == u"not found"
    assert [section.split()[1] for section in parser if section.startswith(u"my ")] ==\
           [u"one", u"two", u"t3", u"t4", u"t5", u"t6"]

