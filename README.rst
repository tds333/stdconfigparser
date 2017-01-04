StdConfigParser
---------------

This is the Python configparser with an extra class StdConfigParser.
The StdConfigParser class uses specified parameters to initialize
the Python ConfigParser and adds some useful converters.
The result is a simple well defined syntax for the INI file.
See it as a preconfigured ConfigParser class for you.
It allows interoperability in configuration between different projects.

Also contains everything to be a full backport of the configparser module from
Python 3.5 to Python 2.7, 3.3, 3.4.

Everything in one module easy to vendor or install no extra dependencies.


`Documentation <http://stdconfigparser.readthedocs.org/>`_

`ChangeLog <http://stdconfigparser.readthedocs.io/en/latest/changelog.html>`_

`Source code on github <https://github.com/tds333/stdconfigparser>`_


Example config file::

    [section]
    option = value

    envlisting = env1,env2,env3

    valuelist = multi line
                values
                # with comment
                fetchable as list

    [other_section]
    # interpolation is a optional feature
    name = ${section:option}-substitution
