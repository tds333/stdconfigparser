#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from stdconfigparser import StdConfigParser


def test_init():
    parser = StdConfigParser()
    assert parser
    parser = StdConfigParser(defaults={"mydefault": "true"})
    assert parser
    assert parser.getboolean("DEFAULT", "mydefault")
    parser = StdConfigParser(converters={"bool": bool})
    assert parser
    assert parser.getbool("DEFAULT", "notthere", fallback=True)

def test_getlines():
    parser = StdConfigParser()
    test = """
    [test]
    multiline = 1
        2
        3
        4
    """
    parser.read_string(test)
    lines = parser.getlines("test", "multiline")
    assert len(lines) > 0
    assert [str(i) for i in range(1, 5)] == lines

def test_getlines_trim():
    parser = StdConfigParser()
    test = """
    [test]
    multiline =
        value 1
          value 2
    """
    parser.read_string(test)
    lines = parser.getlines("test", "multiline")
    assert len(lines) > 0
    assert ["value 1", "value 2"] == lines

def test_getlisting():
    parser = StdConfigParser()
    test = """
    [test]
    listing = value 1,value 2, value 3 , v4
    """
    parser.read_string(test)
    li = parser.getlisting("test", "listing")
    assert len(li) > 0
    assert ["value 1", "value 2", "value 3", "v4"] == li

def test_getlisting_multi():
    parser = StdConfigParser()
    test = """
    [test]
    listing = value 1,
        value 2, value 3
         , v4
    """
    parser.read_string(test)
    li = parser.getlisting("test", "listing")
    assert len(li) > 0
    assert ["value 1", "value 2", "value 3", "v4"] == li

def test_getjson():
    parser = StdConfigParser()
    test = """
    [test]
    list = [1,2,3, "4"]
    object = {"a": "val b", "b": 1.7}
    string = "xyz"
    number = 10000000
    float = 3.14
    """
    parser.read_string(test)
    sec = parser["test"]
    assert sec.getjson("list") == [1,2,3, "4"]
    assert sec.getjson("object") == {"a": "val b", "b": 1.7}
    assert sec.getjson("string") == "xyz"
    assert sec.getjson("number") == 10000000
    assert sec.getjson("float") == 3.14


def test_conv_error():
    parser = StdConfigParser()
    test = """
    [test]
    int = 100
    bool = true
    string = bla
    float = 3.14
    """
    parser.read_string(test)
    sec = parser["test"]
    assert sec.getint("int") == 100
    with pytest.raises(ValueError):
        assert sec.getint("string")
    with pytest.raises(ValueError):
        assert sec.getfloat("string")
    with pytest.raises(ValueError):
        assert sec.getboolean("string")


def test_complex():
    example = """
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

    #parser = StdConfigParser(interpolate=False)
    parser = StdConfigParser()
    parser.read_string(example)
    assert parser.get("mysection", "name") == "My troublesome name"
    assert parser.get("section2", "name2") == "My troublesome name"
    assert parser.getjson("mysection", "dict") == {"a": 1, "b": 2}
    #assert parser.getjson("mysection", "list") == []
    #assert parser.getlines("mysection", "multiline") == []
    assert parser.get("sec.two", "name") == "bla"
    assert parser.get("my two", "name") == "two"
    assert parser.get("my t6", "name") == "one"
    assert parser.getjson("json", "list") == [1,2,3]
    assert parser.getjson("json", "object") == {"a": "myval", "b": "otherval"}
    assert parser.getjson("json", "with_comment") == [1, "200", "400", True,
                                                      False, None, 3.14,
                                                      {"another": 5,
                                                       "second": "bla"}]
    assert parser.getjson("json", "not_invalid") == ["a", "b"]
    assert parser.getjson("json", "invalid", fallback="not found") == "not found"
    assert [section.split()[1] for section in parser if section.startswith("my ")] ==\
           ["one", "two", "t3", "t4", "t5", "t6"]

