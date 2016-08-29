StdConfigParser
---------------

This is the Python configparser with an extra class StdConfigParser.

Provides a standard configuration syntax and the parser for it.
Also contains everything to be a backport of the ConfigParser from
Python 3.5 to Python 2.7.

Everything in one module easy to vendor or install as extra dependency.


`Documentation <http://stdconfigparser.readthedocs.org/>`_

`ChangeLog <http://stdconfigparser.readthedocs.io/en/latest/changelog.html>`_

`Source code on github <https://github.com/tds333/stdconfigparser>`_


Example config file::

    [section]
    key = value

    envlist = env1,env2,env3

    valuelist = multi line
                values
                # with comment
                fetchable as list

    complex_value = {
        "key 1": 1,
        "key 2": 2,
        # special list of environments
        "env list": ["a", "b"],
        }

    [other_section]
    name = ${section:key}-substitution
