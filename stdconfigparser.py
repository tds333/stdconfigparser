# -*- coding: utf-8 -*-
# Copyright (c) 2016 Wolfgang Langner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module provides the StdConfigParser class. A simple
standard INI configuration parser with a specified format. All is based
on the Python standard library configparser.
For Python 2.7 it contains backported classes from Python 3.5 configparser
module.

The StdConfigParser includes also additional converter methods.
They allow really powerful configurations by keeping all simple for the user.
See what can be done for your configuration with only these few additional lines
of code.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


__version__ = "0.7.dev0"

__all__ = ["NoSectionError", "DuplicateOptionError", "DuplicateSectionError",
           "NoOptionError", "InterpolationError", "InterpolationDepthError",
           "InterpolationMissingOptionError", "InterpolationSyntaxError",
           "ParsingError", "MissingSectionHeaderError",
           "ConfigParser", "SafeConfigParser", "RawConfigParser",
           "Interpolation", "BasicInterpolation", "ExtendedInterpolation",
           "LegacyInterpolation", "SectionProxy", "ConverterMapping",
           "DEFAULTSECT", "MAX_INTERPOLATION_DEPTH",
           "StdConfigParser"]


import sys
import json


PY2 = sys.version_info[0] == 2
PY33 = sys.version_info[:2] == (3, 3)
PY34 = sys.version_info[:2] == (3, 4)


def from_none(exc):
    """raise from_none(ValueError('a')) == raise ValueError('a') from None"""
    exc.__cause__ = None
    exc.__suppress_context__ = True
    return exc

# whole Python 2 implementation based on the backport of configparser
# lot of stuff copied also from Python standard library implementation
if PY2:

    from collections import MutableMapping
    try:
        from collections import OrderedDict
    except ImportError:
        from ordereddict import OrderedDict

    from io import open
    try:
        from thread import get_ident
    except ImportError:
        try:
            from _thread import get_ident
        except ImportError:
            from _dummy_thread import get_ident


    # stuff from backports helpers

    str = type('str') # same as str = unicode because of __future__.unicode_literals

    # constants
    DEFAULTSECT = "DEFAULT"

    MAX_INTERPOLATION_DEPTH = 10

    # Used in parser getters to indicate the default behaviour when a specific
    # option is not found it to raise an exception. Created to enable `None' as
    # a valid fallback value.
    _UNSET = object()


    # from reprlib 3.2.1
    def recursive_repr(fillvalue='...'):
        'Decorator to make a repr function return fillvalue for a recursive call'

        def decorating_function(user_function):
            repr_running = set()

            def wrapper(self):
                key = id(self), get_ident()
                if key in repr_running:
                    return fillvalue
                repr_running.add(key)
                try:
                    result = user_function(self)
                finally:
                    repr_running.discard(key)
                return result

            # Can't use functools.wraps() here because of bootstrap issues
            wrapper.__module__ = getattr(user_function, '__module__')
            wrapper.__doc__ = getattr(user_function, '__doc__')
            wrapper.__name__ = getattr(user_function, '__name__')
            wrapper.__annotations__ = getattr(user_function, '__annotations__', {})
            return wrapper

        return decorating_function

    # from collections 3.2.1
    class ChainMap(MutableMapping):
        ''' A ChainMap groups multiple dicts (or other mappings) together
        to create a single, updateable view.

        The underlying mappings are stored in a list.  That list is public and can
        accessed or updated using the *maps* attribute.  There is no other state.

        Lookups search the underlying mappings successively until a key is found.
        In contrast, writes, updates, and deletions only operate on the first
        mapping.

        '''

        def __init__(self, *maps):
            '''Initialize a ChainMap by setting *maps* to the given mappings.
            If no mappings are provided, a single empty dictionary is used.

            '''
            self.maps = list(maps) or [{}]          # always at least one map

        def __missing__(self, key):
            raise KeyError(key)

        def __getitem__(self, key):
            for mapping in self.maps:
                try:
                    return mapping[key]             # can't use 'key in mapping' with defaultdict
                except KeyError:
                    pass
            return self.__missing__(key)            # support subclasses that define __missing__

        def get(self, key, default=None):
            return self[key] if key in self else default

        def __len__(self):
            return len(set().union(*self.maps))     # reuses stored hash values if possible

        def __iter__(self):
            return iter(set().union(*self.maps))

        def __contains__(self, key):
            return any(key in m for m in self.maps)

        @recursive_repr()
        def __repr__(self):
            return '{0.__class__.__name__}({1})'.format(
                self, ', '.join(map(repr, self.maps)))

        @classmethod
        def fromkeys(cls, iterable, *args):
            'Create a ChainMap with a single dict created from the iterable.'
            return cls(dict.fromkeys(iterable, *args))

        def copy(self):
            'New ChainMap or subclass with a new copy of maps[0] and refs to maps[1:]'
            return self.__class__(self.maps[0].copy(), *self.maps[1:])

        __copy__ = copy

        def new_child(self):                        # like Django's Context.push()
            'New ChainMap with a new dict followed by all previous maps.'
            return self.__class__({}, *self.maps)

        @property
        def parents(self):                          # like Django's Context.pop()
            'New ChainMap from maps[1:].'
            return self.__class__(*self.maps[1:])

        def __setitem__(self, key, value):
            self.maps[0][key] = value

        def __delitem__(self, key):
            try:
                del self.maps[0][key]
            except KeyError:
                raise KeyError('Key not found in the first mapping: {!r}'.format(key))

        def popitem(self):
            'Remove and return an item pair from maps[0]. Raise KeyError is maps[0] is empty.'
            try:
                return self.maps[0].popitem()
            except KeyError:
                raise KeyError('No keys found in the first mapping.')

        def pop(self, key, *args):
            'Remove *key* from maps[0] and return its value. Raise KeyError if *key* not in maps[0].'
            try:
                return self.maps[0].pop(key, *args)
            except KeyError:
                raise KeyError('Key not found in the first mapping: {!r}'.format(key))

        def clear(self):
            'Clear maps[0], leaving maps[1:] intact.'
            self.maps[0].clear()

if PY33 or PY34:

    from reprlib import recursive_repr
    from collections import ChainMap, MutableMapping, OrderedDict  # noqa
    from configparser import _UNSET, DEFAULTSECT, MAX_INTERPOLATION_DEPTH

if PY2 or PY33 or PY34:

    import functools
    from io import StringIO
    import itertools
    import re
    import warnings


    # exception classes
    class Error(Exception):
        """Base class for ConfigParser exceptions."""

        def __init__(self, msg=''):
            self.message = msg
            Exception.__init__(self, msg)

        def __repr__(self):
            return self.message

        __str__ = __repr__


    class NoSectionError(Error):
        """Raised when no section matches a requested option."""

        def __init__(self, section):
            Error.__init__(self, 'No section: %r' % (section,))
            self.section = section
            self.args = (section, )


    class DuplicateSectionError(Error):
        """Raised when a section is repeated in an input source.

        Possible repetitions that raise this exception are: multiple creation
        using the API or in strict parsers when a section is found more than once
        in a single input file, string or dictionary.
        """

        def __init__(self, section, source=None, lineno=None):
            msg = [repr(section), " already exists"]
            if source is not None:
                message = ["While reading from ", repr(source)]
                if lineno is not None:
                    message.append(" [line {0:2d}]".format(lineno))
                message.append(": section ")
                message.extend(msg)
                msg = message
            else:
                msg.insert(0, "Section ")
            Error.__init__(self, "".join(msg))
            self.section = section
            self.source = source
            self.lineno = lineno
            self.args = (section, source, lineno)


    class DuplicateOptionError(Error):
        """Raised by strict parsers when an option is repeated in an input source.

        Current implementation raises this exception only when an option is found
        more than once in a single file, string or dictionary.
        """

        def __init__(self, section, option, source=None, lineno=None):
            msg = [repr(option), " in section ", repr(section),
                   " already exists"]
            if source is not None:
                message = ["While reading from ", repr(source)]
                if lineno is not None:
                    message.append(" [line {0:2d}]".format(lineno))
                message.append(": option ")
                message.extend(msg)
                msg = message
            else:
                msg.insert(0, "Option ")
            Error.__init__(self, "".join(msg))
            self.section = section
            self.option = option
            self.source = source
            self.lineno = lineno
            self.args = (section, option, source, lineno)


    class NoOptionError(Error):
        """A requested option was not found."""

        def __init__(self, option, section):
            Error.__init__(self, "No option %r in section: %r" %
                           (option, section))
            self.option = option
            self.section = section
            self.args = (option, section)


    class InterpolationError(Error):
        """Base class for interpolation-related exceptions."""

        def __init__(self, option, section, msg):
            Error.__init__(self, msg)
            self.option = option
            self.section = section
            self.args = (option, section, msg)


    class InterpolationMissingOptionError(InterpolationError):
        """A string substitution required a setting which was not available."""

        def __init__(self, option, section, rawval, reference):
            msg = ("Bad value substitution: option {0!r} in section {1!r} contains "
                   "an interpolation key {2!r} which is not a valid option name. "
                   "Raw value: {3!r}".format(option, section, reference, rawval))
            InterpolationError.__init__(self, option, section, msg)
            self.reference = reference
            self.args = (option, section, rawval, reference)


    class InterpolationSyntaxError(InterpolationError):
        """Raised when the source text contains invalid syntax.

        Current implementation raises this exception when the source text into
        which substitutions are made does not conform to the required syntax.
        """


    class InterpolationDepthError(InterpolationError):
        """Raised when substitutions are nested too deeply."""

        def __init__(self, option, section, rawval):
            msg = ("Recursion limit exceeded in value substitution: option {0!r} "
                   "in section {1!r} contains an interpolation key which "
                   "cannot be substituted in {2} steps. Raw value: {3!r}"
                   "".format(option, section, MAX_INTERPOLATION_DEPTH,
                             rawval))
            InterpolationError.__init__(self, option, section, msg)
            self.args = (option, section, rawval)


    class ParsingError(Error):
        """Raised when a configuration file does not follow legal syntax."""

        def __init__(self, source=None, filename=None):
            # Exactly one of `source'/`filename' arguments has to be given.
            # `filename' kept for compatibility.
            if filename and source:
                raise ValueError("Cannot specify both `filename' and `source'. "
                                 "Use `source'.")
            elif not filename and not source:
                raise ValueError("Required argument `source' not given.")
            elif filename:
                source = filename
            Error.__init__(self, 'Source contains parsing errors: %r' % source)
            self.source = source
            self.errors = []
            self.args = (source, )

        @property
        def filename(self):
            """Deprecated, use `source'."""
            warnings.warn(
                "The 'filename' attribute will be removed in future versions.  "
                "Use 'source' instead.",
                DeprecationWarning, stacklevel=2
            )
            return self.source

        @filename.setter
        def filename(self, value):
            """Deprecated, user `source'."""
            warnings.warn(
                "The 'filename' attribute will be removed in future versions.  "
                "Use 'source' instead.",
                DeprecationWarning, stacklevel=2
            )
            self.source = value

        def append(self, lineno, line):
            self.errors.append((lineno, line))
            self.message += '\n\t[line %2d]: %s' % (lineno, line)


    class MissingSectionHeaderError(ParsingError):
        """Raised when a key-value pair is found before any section header."""

        def __init__(self, filename, lineno, line):
            Error.__init__(
                self,
                'File contains no section headers.\nfile: %r, line: %d\n%r' %
                (filename, lineno, line))
            self.source = filename
            self.lineno = lineno
            self.line = line
            self.args = (filename, lineno, line)



    class Interpolation(object):
        """Dummy interpolation that passes the value through with no changes."""

        def before_get(self, parser, section, option, value, defaults):
            return value

        def before_set(self, parser, section, option, value):
            return value

        def before_read(self, parser, section, option, value):
            return value

        def before_write(self, parser, section, option, value):
            return value


    class BasicInterpolation(Interpolation):
        """Interpolation as implemented in the classic ConfigParser.

        The option values can contain format strings which refer to other values in
        the same section, or values in the special default section.

        For example:

            something: %(dir)s/whatever

        would resolve the "%(dir)s" to the value of dir.  All reference
        expansions are done late, on demand. If a user needs to use a bare % in
        a configuration file, she can escape it by writing %%. Other % usage
        is considered a user error and raises `InterpolationSyntaxError'."""

        _KEYCRE = re.compile(r"%\(([^)]+)\)s")

        def before_get(self, parser, section, option, value, defaults):
            L = []
            self._interpolate_some(parser, option, L, value, section, defaults, 1)
            return ''.join(L)

        def before_set(self, parser, section, option, value):
            tmp_value = value.replace('%%', '') # escaped percent signs
            tmp_value = self._KEYCRE.sub('', tmp_value) # valid syntax
            if '%' in tmp_value:
                raise ValueError("invalid interpolation syntax in %r at "
                                 "position %d" % (value, tmp_value.find('%')))
            return value

        def _interpolate_some(self, parser, option, accum, rest, section, map,
                              depth):
            rawval = parser.get(section, option, raw=True, fallback=rest)
            if depth > MAX_INTERPOLATION_DEPTH:
                raise InterpolationDepthError(option, section, rawval)
            while rest:
                p = rest.find("%")
                if p < 0:
                    accum.append(rest)
                    return
                if p > 0:
                    accum.append(rest[:p])
                    rest = rest[p:]
                # p is no longer used
                c = rest[1:2]
                if c == "%":
                    accum.append("%")
                    rest = rest[2:]
                elif c == "(":
                    m = self._KEYCRE.match(rest)
                    if m is None:
                        raise InterpolationSyntaxError(option, section,
                              "bad interpolation variable reference %r" % rest)
                    var = parser.optionxform(m.group(1))
                    rest = rest[m.end():]
                    try:
                        v = map[var]
                    except KeyError:
                        raise from_none(InterpolationMissingOptionError(
                            option, section, rawval, var))
                    if "%" in v:
                        self._interpolate_some(parser, option, accum, v,
                                               section, map, depth + 1)
                    else:
                        accum.append(v)
                else:
                    raise InterpolationSyntaxError(
                        option, section,
                        "'%%' must be followed by '%%' or '(', "
                        "found: %r" % (rest,))


    class ExtendedInterpolation(Interpolation):
        """Advanced variant of interpolation, supports the syntax used by
        `zc.buildout'. Enables interpolation between sections."""

        _KEYCRE = re.compile(r"\$\{([^}]+)\}")

        def before_get(self, parser, section, option, value, defaults):
            L = []
            self._interpolate_some(parser, option, L, value, section, defaults, 1)
            return ''.join(L)

        def before_set(self, parser, section, option, value):
            tmp_value = value.replace('$$', '') # escaped dollar signs
            tmp_value = self._KEYCRE.sub('', tmp_value) # valid syntax
            if '$' in tmp_value:
                raise ValueError("invalid interpolation syntax in %r at "
                                 "position %d" % (value, tmp_value.find('$')))
            return value

        def _interpolate_some(self, parser, option, accum, rest, section, map,
                              depth):
            rawval = parser.get(section, option, raw=True, fallback=rest)
            if depth > MAX_INTERPOLATION_DEPTH:
                raise InterpolationDepthError(option, section, rawval)
            while rest:
                p = rest.find("$")
                if p < 0:
                    accum.append(rest)
                    return
                if p > 0:
                    accum.append(rest[:p])
                    rest = rest[p:]
                # p is no longer used
                c = rest[1:2]
                if c == "$":
                    accum.append("$")
                    rest = rest[2:]
                elif c == "{":
                    m = self._KEYCRE.match(rest)
                    if m is None:
                        raise InterpolationSyntaxError(option, section,
                              "bad interpolation variable reference %r" % rest)
                    path = m.group(1).split(':')
                    rest = rest[m.end():]
                    sect = section
                    opt = option
                    try:
                        if len(path) == 1:
                            opt = parser.optionxform(path[0])
                            v = map[opt]
                        elif len(path) == 2:
                            sect = path[0]
                            opt = parser.optionxform(path[1])
                            v = parser.get(sect, opt, raw=True)
                        else:
                            raise InterpolationSyntaxError(
                                option, section,
                                "More than one ':' found: %r" % (rest,))
                    except (KeyError, NoSectionError, NoOptionError):
                        raise from_none(InterpolationMissingOptionError(
                            option, section, rawval, ":".join(path)))
                    if "$" in v:
                        self._interpolate_some(parser, opt, accum, v, sect,
                                               dict(parser.items(sect, raw=True)),
                                               depth + 1)
                    else:
                        accum.append(v)
                else:
                    raise InterpolationSyntaxError(
                        option, section,
                        "'$' must be followed by '$' or '{', "
                        "found: %r" % (rest,))


    class LegacyInterpolation(Interpolation):
        """Deprecated interpolation used in old versions of ConfigParser.
        Use BasicInterpolation or ExtendedInterpolation instead."""

        _KEYCRE = re.compile(r"%\(([^)]*)\)s|.")

        def before_get(self, parser, section, option, value, vars):
            rawval = value
            depth = MAX_INTERPOLATION_DEPTH
            while depth:                    # Loop through this until it's done
                depth -= 1
                if value and "%(" in value:
                    replace = functools.partial(self._interpolation_replace,
                                                parser=parser)
                    value = self._KEYCRE.sub(replace, value)
                    try:
                        value = value % vars
                    except KeyError as e:
                        raise from_none(InterpolationMissingOptionError(
                            option, section, rawval, e.args[0]))
                else:
                    break
            if value and "%(" in value:
                raise InterpolationDepthError(option, section, rawval)
            return value

        def before_set(self, parser, section, option, value):
            return value

        @staticmethod
        def _interpolation_replace(match, parser):
            s = match.group(1)
            if s is None:
                return match.group()
            else:
                return "%%(%s)s" % parser.optionxform(s)


    class RawConfigParser(MutableMapping):
        """ConfigParser that does not do interpolation."""

        # Regular expressions for parsing section headers and options
        _SECT_TMPL = r"""
            \[                                 # [
            (?P<header>[^]]+)                  # very permissive!
            \]                                 # ]
            """
        _OPT_TMPL = r"""
            (?P<option>.*?)                    # very permissive!
            \s*(?P<vi>{delim})\s*              # any number of space/tab,
                                               # followed by any of the
                                               # allowed delimiters,
                                               # followed by any space/tab
            (?P<value>.*)$                     # everything up to eol
            """
        _OPT_NV_TMPL = r"""
            (?P<option>.*?)                    # very permissive!
            \s*(?:                             # any number of space/tab,
            (?P<vi>{delim})\s*                 # optionally followed by
                                               # any of the allowed
                                               # delimiters, followed by any
                                               # space/tab
            (?P<value>.*))?$                   # everything up to eol
            """
        # Interpolation algorithm to be used if the user does not specify another
        _DEFAULT_INTERPOLATION = Interpolation()
        # Compiled regular expression for matching sections
        SECTCRE = re.compile(_SECT_TMPL, re.VERBOSE)
        # Compiled regular expression for matching options with typical separators
        OPTCRE = re.compile(_OPT_TMPL.format(delim="=|:"), re.VERBOSE)
        # Compiled regular expression for matching options with optional values
        # delimited using typical separators
        OPTCRE_NV = re.compile(_OPT_NV_TMPL.format(delim="=|:"), re.VERBOSE)
        # Compiled regular expression for matching leading whitespace in a line
        NONSPACECRE = re.compile(r"\S")
        # Possible boolean values in the configuration.
        BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                          '0': False, 'no': False, 'false': False, 'off': False}

        def __init__(self, defaults=None, dict_type=OrderedDict,
                     allow_no_value=False, **kwargs):

            # keyword-only arguments
            delimiters = kwargs.get('delimiters', ('=', ':'))
            comment_prefixes = kwargs.get('comment_prefixes', ('#', ';'))
            inline_comment_prefixes = kwargs.get('inline_comment_prefixes', None)
            strict = kwargs.get('strict', True)
            empty_lines_in_values = kwargs.get('empty_lines_in_values', True)
            default_section = kwargs.get('default_section', DEFAULTSECT)
            interpolation = kwargs.get('interpolation', _UNSET)
            converters = kwargs.get('converters', _UNSET)

            self._dict = dict_type
            self._sections = self._dict()
            self._defaults = self._dict()
            self._converters = ConverterMapping(self)
            self._proxies = self._dict()
            self._proxies[default_section] = SectionProxy(self, default_section)
            if defaults:
                for key, value in defaults.items():
                    self._defaults[self.optionxform(key)] = value
            self._delimiters = tuple(delimiters)
            if delimiters == ('=', ':'):
                self._optcre = self.OPTCRE_NV if allow_no_value else self.OPTCRE
            else:
                d = "|".join(re.escape(d) for d in delimiters)
                if allow_no_value:
                    self._optcre = re.compile(self._OPT_NV_TMPL.format(delim=d),
                                              re.VERBOSE)
                else:
                    self._optcre = re.compile(self._OPT_TMPL.format(delim=d),
                                              re.VERBOSE)
            self._comment_prefixes = tuple(comment_prefixes or ())
            self._inline_comment_prefixes = tuple(inline_comment_prefixes or ())
            self._strict = strict
            self._allow_no_value = allow_no_value
            self._empty_lines_in_values = empty_lines_in_values
            self.default_section = default_section
            self._interpolation = interpolation
            if self._interpolation is _UNSET:
                self._interpolation = self._DEFAULT_INTERPOLATION
            if self._interpolation is None:
                self._interpolation = Interpolation()
            if converters is not _UNSET:
                self._converters.update(converters)

        def defaults(self):
            return self._defaults

        def sections(self):
            """Return a list of section names, excluding [DEFAULT]"""
            # self._sections will never have [DEFAULT] in it
            return list(self._sections.keys())

        def add_section(self, section):
            """Create a new section in the configuration.

            Raise DuplicateSectionError if a section by the specified name
            already exists. Raise ValueError if name is DEFAULT.
            """
            if section == self.default_section:
                raise ValueError('Invalid section name: %r' % section)

            if section in self._sections:
                raise DuplicateSectionError(section)
            self._sections[section] = self._dict()
            self._proxies[section] = SectionProxy(self, section)

        def has_section(self, section):
            """Indicate whether the named section is present in the configuration.

            The DEFAULT section is not acknowledged.
            """
            return section in self._sections

        def options(self, section):
            """Return a list of option names for the given section name."""
            try:
                opts = self._sections[section].copy()
            except KeyError:
                raise from_none(NoSectionError(section))
            opts.update(self._defaults)
            return list(opts.keys())

        def read(self, filenames, encoding=None):
            """Read and parse a filename or a list of filenames.

            Files that cannot be opened are silently ignored; this is
            designed so that you can specify a list of potential
            configuration file locations (e.g. current directory, user's
            home directory, systemwide directory), and all existing
            configuration files in the list will be read.  A single
            filename may also be given.

            Return list of successfully read files.
            """
            if isinstance(filenames, (str, bytes)):
                filenames = [filenames]
            read_ok = []
            for filename in filenames:
                try:
                    with open(filename, encoding=encoding) as fp:
                        self._read(fp, filename)
                except IOError:
                    continue
                read_ok.append(filename)
            return read_ok

        def read_file(self, f, source=None):
            """Like read() but the argument must be a file-like object.

            The `f' argument must be iterable, returning one line at a time.
            Optional second argument is the `source' specifying the name of the
            file being read. If not given, it is taken from f.name. If `f' has no
            `name' attribute, `<???>' is used.
            """
            if source is None:
                try:
                    source = f.name
                except AttributeError:
                    source = '<???>'
            self._read(f, source)

        def read_string(self, string, source='<string>'):
            """Read configuration from a given string."""
            sfile = StringIO(string)
            self.read_file(sfile, source)

        def read_dict(self, dictionary, source='<dict>'):
            """Read configuration from a dictionary.

            Keys are section names, values are dictionaries with keys and values
            that should be present in the section. If the used dictionary type
            preserves order, sections and their keys will be added in order.

            All types held in the dictionary are converted to strings during
            reading, including section names, option names and keys.

            Optional second argument is the `source' specifying the name of the
            dictionary being read.
            """
            elements_added = set()
            for section, keys in dictionary.items():
                section = str(section)
                try:
                    self.add_section(section)
                except (DuplicateSectionError, ValueError):
                    if self._strict and section in elements_added:
                        raise
                elements_added.add(section)
                for key, value in keys.items():
                    key = self.optionxform(str(key))
                    if value is not None:
                        value = str(value)
                    if self._strict and (section, key) in elements_added:
                        raise DuplicateOptionError(section, key, source)
                    elements_added.add((section, key))
                    self.set(section, key, value)

        def readfp(self, fp, filename=None):
            """Deprecated, use read_file instead."""
            warnings.warn(
                "This method will be removed in future versions.  "
                "Use 'parser.read_file()' instead.",
                DeprecationWarning, stacklevel=2
            )
            self.read_file(fp, source=filename)

        def get(self, section, option, **kwargs):
            """Get an option value for a given section.

            If `vars' is provided, it must be a dictionary. The option is looked up
            in `vars' (if provided), `section', and in `DEFAULTSECT' in that order.
            If the key is not found and `fallback' is provided, it is used as
            a fallback value. `None' can be provided as a `fallback' value.

            If interpolation is enabled and the optional argument `raw' is False,
            all interpolations are expanded in the return values.

            Arguments `raw', `vars', and `fallback' are keyword only.

            The section DEFAULT is special.
            """
            # keyword-only arguments
            raw = kwargs.get('raw', False)
            vars = kwargs.get('vars', None)
            fallback = kwargs.get('fallback', _UNSET)

            try:
                d = self._unify_values(section, vars)
            except NoSectionError:
                if fallback is _UNSET:
                    raise
                else:
                    return fallback
            option = self.optionxform(option)
            try:
                value = d[option]
            except KeyError:
                if fallback is _UNSET:
                    raise NoOptionError(option, section)
                else:
                    return fallback

            if raw or value is None:
                return value
            else:
                return self._interpolation.before_get(self, section, option, value,
                                                      d)

        def _get(self, section, conv, option, **kwargs):
            return conv(self.get(section, option, **kwargs))

        def _get_conv(self, section, option, conv, **kwargs):
            # keyword-only arguments
            kwargs.setdefault('raw', False)
            kwargs.setdefault('vars', None)
            fallback = kwargs.pop('fallback', _UNSET)
            try:
                return self._get(section, conv, option, **kwargs)
            except (NoSectionError, NoOptionError):
                if fallback is _UNSET:
                    raise
                return fallback

        # getint, getfloat and getboolean provided directly for backwards compat
        def getint(self, section, option, **kwargs):
            # keyword-only arguments
            kwargs.setdefault('raw', False)
            kwargs.setdefault('vars', None)
            kwargs.setdefault('fallback', _UNSET)
            return self._get_conv(section, option, int, **kwargs)

        def getfloat(self, section, option, **kwargs):
            # keyword-only arguments
            kwargs.setdefault('raw', False)
            kwargs.setdefault('vars', None)
            kwargs.setdefault('fallback', _UNSET)
            return self._get_conv(section, option, float, **kwargs)

        def getboolean(self, section, option, **kwargs):
            # keyword-only arguments
            kwargs.setdefault('raw', False)
            kwargs.setdefault('vars', None)
            kwargs.setdefault('fallback', _UNSET)
            return self._get_conv(section, option, self._convert_to_boolean,
                                  **kwargs)

        def items(self, section=_UNSET, raw=False, vars=None):
            """Return a list of (name, value) tuples for each option in a section.

            All % interpolations are expanded in the return values, based on the
            defaults passed into the constructor, unless the optional argument
            `raw' is true.  Additional substitutions may be provided using the
            `vars' argument, which must be a dictionary whose contents overrides
            any pre-existing defaults.

            The section DEFAULT is special.
            """
            if section is _UNSET:
                return super(RawConfigParser, self).items()
            d = self._defaults.copy()
            try:
                d.update(self._sections[section])
            except KeyError:
                if section != self.default_section:
                    raise NoSectionError(section)
            # Update with the entry specific variables
            if vars:
                for key, value in vars.items():
                    d[self.optionxform(key)] = value
            value_getter = lambda option: self._interpolation.before_get(self,
                                          section, option, d[option], d)
            if raw:
                value_getter = lambda option: d[option]
            return [(option, value_getter(option)) for option in d.keys()]

        def popitem(self):
            """Remove a section from the parser and return it as
            a (section_name, section_proxy) tuple. If no section is present, raise
            KeyError.

            The section DEFAULT is never returned because it cannot be removed.
            """
            for key in self.sections():
                value = self[key]
                del self[key]
                return key, value
            raise KeyError

        def optionxform(self, optionstr):
            return optionstr.lower()

        def has_option(self, section, option):
            """Check for the existence of a given option in a given section.
            If the specified `section' is None or an empty string, DEFAULT is
            assumed. If the specified `section' does not exist, returns False."""
            if not section or section == self.default_section:
                option = self.optionxform(option)
                return option in self._defaults
            elif section not in self._sections:
                return False
            else:
                option = self.optionxform(option)
                return (option in self._sections[section]
                        or option in self._defaults)

        def set(self, section, option, value=None):
            """Set an option."""
            if value:
                value = self._interpolation.before_set(self, section, option,
                                                       value)
            if not section or section == self.default_section:
                sectdict = self._defaults
            else:
                try:
                    sectdict = self._sections[section]
                except KeyError:
                    raise from_none(NoSectionError(section))
            sectdict[self.optionxform(option)] = value

        def write(self, fp, space_around_delimiters=True):
            """Write an .ini-format representation of the configuration state.

            If `space_around_delimiters' is True (the default), delimiters
            between keys and values are surrounded by spaces.
            """
            if space_around_delimiters:
                d = " {0} ".format(self._delimiters[0])
            else:
                d = self._delimiters[0]
            if self._defaults:
                self._write_section(fp, self.default_section,
                                    self._defaults.items(), d)
            for section in self._sections:
                self._write_section(fp, section,
                                    self._sections[section].items(), d)

        def _write_section(self, fp, section_name, section_items, delimiter):
            """Write a single section to the specified `fp'."""
            fp.write("[{0}]\n".format(section_name))
            for key, value in section_items:
                value = self._interpolation.before_write(self, section_name, key,
                                                         value)
                if value is not None or not self._allow_no_value:
                    value = delimiter + str(value).replace('\n', '\n\t')
                else:
                    value = ""
                fp.write("{0}{1}\n".format(key, value))
            fp.write("\n")

        def remove_option(self, section, option):
            """Remove an option."""
            if not section or section == self.default_section:
                sectdict = self._defaults
            else:
                try:
                    sectdict = self._sections[section]
                except KeyError:
                    raise from_none(NoSectionError(section))
            option = self.optionxform(option)
            existed = option in sectdict
            if existed:
                del sectdict[option]
            return existed

        def remove_section(self, section):
            """Remove a file section."""
            existed = section in self._sections
            if existed:
                del self._sections[section]
                del self._proxies[section]
            return existed

        def __getitem__(self, key):
            if key != self.default_section and not self.has_section(key):
                raise KeyError(key)
            return self._proxies[key]

        def __setitem__(self, key, value):
            # To conform with the mapping protocol, overwrites existing values in
            # the section.

            # XXX this is not atomic if read_dict fails at any point. Then again,
            # no update method in configparser is atomic in this implementation.
            if key == self.default_section:
                self._defaults.clear()
            elif key in self._sections:
                self._sections[key].clear()
            self.read_dict({key: value})

        def __delitem__(self, key):
            if key == self.default_section:
                raise ValueError("Cannot remove the default section.")
            if not self.has_section(key):
                raise KeyError(key)
            self.remove_section(key)

        def __contains__(self, key):
            return key == self.default_section or self.has_section(key)

        def __len__(self):
            return len(self._sections) + 1 # the default section

        def __iter__(self):
            # XXX does it break when underlying container state changed?
            return itertools.chain((self.default_section,), self._sections.keys())

        def _read(self, fp, fpname):
            """Parse a sectioned configuration file.

            Each section in a configuration file contains a header, indicated by
            a name in square brackets (`[]'), plus key/value options, indicated by
            `name' and `value' delimited with a specific substring (`=' or `:' by
            default).

            Values can span multiple lines, as long as they are indented deeper
            than the first line of the value. Depending on the parser's mode, blank
            lines may be treated as parts of multiline values or ignored.

            Configuration files may include comments, prefixed by specific
            characters (`#' and `;' by default). Comments may appear on their own
            in an otherwise empty line or may be entered in lines holding values or
            section names.
            """
            elements_added = set()
            cursect = None                        # None, or a dictionary
            sectname = None
            optname = None
            lineno = 0
            indent_level = 0
            e = None                              # None, or an exception
            for lineno, line in enumerate(fp, start=1):
                comment_start = sys.maxsize
                # strip inline comments
                inline_prefixes = dict(
                    (p, -1) for p in self._inline_comment_prefixes)
                while comment_start == sys.maxsize and inline_prefixes:
                    next_prefixes = {}
                    for prefix, index in inline_prefixes.items():
                        index = line.find(prefix, index + 1)
                        if index == -1:
                            continue
                        next_prefixes[prefix] = index
                        if index == 0 or (index > 0 and line[index - 1].isspace()):
                            comment_start = min(comment_start, index)
                    inline_prefixes = next_prefixes
                # strip full line comments
                for prefix in self._comment_prefixes:
                    if line.strip().startswith(prefix):
                        comment_start = 0
                        break
                if comment_start == sys.maxsize:
                    comment_start = None
                value = line[:comment_start].strip()
                if not value:
                    if self._empty_lines_in_values:
                        # add empty line to the value, but only if there was no
                        # comment on the line
                        if (comment_start is None and
                                cursect is not None and
                                optname and
                                cursect[optname] is not None):
                            cursect[optname].append('') # newlines added at join
                    else:
                        # empty line marks end of value
                        indent_level = sys.maxsize
                    continue
                # continuation line?
                first_nonspace = self.NONSPACECRE.search(line)
                cur_indent_level = first_nonspace.start() if first_nonspace else 0
                if (cursect is not None and optname and
                        cur_indent_level > indent_level):
                    cursect[optname].append(value)
                # a section header or option header?
                else:
                    indent_level = cur_indent_level
                    # is it a section header?
                    mo = self.SECTCRE.match(value)
                    if mo:
                        sectname = mo.group('header')
                        if sectname in self._sections:
                            if self._strict and sectname in elements_added:
                                raise DuplicateSectionError(sectname, fpname,
                                                            lineno)
                            cursect = self._sections[sectname]
                            elements_added.add(sectname)
                        elif sectname == self.default_section:
                            cursect = self._defaults
                        else:
                            cursect = self._dict()
                            self._sections[sectname] = cursect
                            self._proxies[sectname] = SectionProxy(self, sectname)
                            elements_added.add(sectname)
                        # So sections can't start with a continuation line
                        optname = None
                    # no section header in the file?
                    elif cursect is None:
                        raise MissingSectionHeaderError(fpname, lineno, line)
                    # an option line?
                    else:
                        mo = self._optcre.match(value)
                        if mo:
                            optname, vi, optval = mo.group('option', 'vi', 'value')
                            if not optname:
                                e = self._handle_error(e, fpname, lineno, line)
                            optname = self.optionxform(optname.rstrip())
                            if (self._strict and
                                    (sectname, optname) in elements_added):
                                raise DuplicateOptionError(sectname, optname,
                                                           fpname, lineno)
                            elements_added.add((sectname, optname))
                            # This check is fine because the OPTCRE cannot
                            # match if it would set optval to None
                            if optval is not None:
                                optval = optval.strip()
                                cursect[optname] = [optval]
                            else:
                                # valueless option handling
                                cursect[optname] = None
                        else:
                            # a non-fatal parsing error occurred. set up the
                            # exception but keep going. the exception will be
                            # raised at the end of the file and will contain a
                            # list of all bogus lines
                            e = self._handle_error(e, fpname, lineno, line)
            # if any parsing errors occurred, raise an exception
            if e:
                raise e
            self._join_multiline_values()

        def _join_multiline_values(self):
            defaults = self.default_section, self._defaults
            all_sections = itertools.chain((defaults,),
                                           self._sections.items())
            for section, options in all_sections:
                for name, val in options.items():
                    if isinstance(val, list):
                        val = '\n'.join(val).rstrip()
                    options[name] = self._interpolation.before_read(self,
                                                                    section,
                                                                    name, val)

        def _handle_error(self, exc, fpname, lineno, line):
            if not exc:
                exc = ParsingError(fpname)
            exc.append(lineno, repr(line))
            return exc

        def _unify_values(self, section, vars):
            """Create a sequence of lookups with 'vars' taking priority over
            the 'section' which takes priority over the DEFAULTSECT.

            """
            sectiondict = {}
            try:
                sectiondict = self._sections[section]
            except KeyError:
                if section != self.default_section:
                    raise NoSectionError(section)
            # Update with the entry specific variables
            vardict = {}
            if vars:
                for key, value in vars.items():
                    if value is not None:
                        value = str(value)
                    vardict[self.optionxform(key)] = value
            return ChainMap(vardict, sectiondict, self._defaults)

        def _convert_to_boolean(self, value):
            """Return a boolean value translating from other types if necessary.
            """
            if value.lower() not in self.BOOLEAN_STATES:
                raise ValueError('Not a boolean: %s' % value)
            return self.BOOLEAN_STATES[value.lower()]

        def _validate_value_types(self, **kwargs):
            """Raises a TypeError for non-string values.

            The only legal non-string value if we allow valueless
            options is None, so we need to check if the value is a
            string if:
            - we do not allow valueless options, or
            - we allow valueless options but the value is not None

            For compatibility reasons this method is not used in classic set()
            for RawConfigParsers. It is invoked in every case for mapping protocol
            access and in ConfigParser.set().
            """
            # keyword-only arguments
            section = kwargs.get('section', "")
            option = kwargs.get('option', "")
            value = kwargs.get('value', "")

            # Python2 stuff
            if isinstance(section, bytes):
                section = section.decode('utf8')
            if isinstance(option, bytes):
                option = option.decode('utf8')
            if isinstance(value, bytes):
                value = value.decode('utf8')

            if not isinstance(section, str):
                raise TypeError("section names must be strings")
            if not isinstance(option, str):
                raise TypeError("option keys must be strings")
            if not self._allow_no_value or value:
                if not isinstance(value, str):
                    raise TypeError("option values must be strings")

            return section, option, value

        @property
        def converters(self):
            return self._converters


    class ConfigParser(RawConfigParser):
        """ConfigParser implementing interpolation."""

        _DEFAULT_INTERPOLATION = BasicInterpolation()

        def set(self, section, option, value=None):
            """Set an option.  Extends RawConfigParser.set by validating type and
            interpolation syntax on the value."""
            _, option, value = self._validate_value_types(option=option, value=value)
            super(ConfigParser, self).set(section, option, value)

        def add_section(self, section):
            """Create a new section in the configuration.  Extends
            RawConfigParser.add_section by validating if the section name is
            a string."""
            section, _, _ = self._validate_value_types(section=section)
            super(ConfigParser, self).add_section(section)


    class SafeConfigParser(ConfigParser):
        """ConfigParser alias for backwards compatibility purposes."""

        def __init__(self, *args, **kwargs):
            super(SafeConfigParser, self).__init__(*args, **kwargs)
            warnings.warn(
                "The SafeConfigParser class has been renamed to ConfigParser "
                "in Python 3.2. This alias will be removed in future versions."
                " Use ConfigParser directly instead.",
                DeprecationWarning, stacklevel=2
            )


    class SectionProxy(MutableMapping):
        """A proxy for a single section from a parser."""

        def __init__(self, parser, name):
            """Creates a view on a section of the specified `name` in `parser`."""
            self._parser = parser
            self._name = name
            for conv in parser.converters:
                key = 'get' + conv
                getter = functools.partial(self.get, _impl=getattr(parser, key))
                setattr(self, key, getter)

        def __repr__(self):
            return '<Section: {0}>'.format(self._name)

        def __getitem__(self, key):
            if not self._parser.has_option(self._name, key):
                raise KeyError(key)
            return self._parser.get(self._name, key)

        def __setitem__(self, key, value):
            _, key, value = self._parser._validate_value_types(option=key, value=value)
            return self._parser.set(self._name, key, value)

        def __delitem__(self, key):
            if not (self._parser.has_option(self._name, key) and
                    self._parser.remove_option(self._name, key)):
                raise KeyError(key)

        def __contains__(self, key):
            return self._parser.has_option(self._name, key)

        def __len__(self):
            return len(self._options())

        def __iter__(self):
            return self._options().__iter__()

        def _options(self):
            if self._name != self._parser.default_section:
                return self._parser.options(self._name)
            else:
                return self._parser.defaults()

        @property
        def parser(self):
            # The parser object of the proxy is read-only.
            return self._parser

        @property
        def name(self):
            # The name of the section on a proxy is read-only.
            return self._name

        def get(self, option, fallback=None, **kwargs):
            """Get an option value.

            Unless `fallback` is provided, `None` will be returned if the option
            is not found.

            """
            # keyword-only arguments
            kwargs.setdefault('raw', False)
            kwargs.setdefault('vars', None)
            _impl = kwargs.pop('_impl', None)
            # If `_impl` is provided, it should be a getter method on the parser
            # object that provides the desired type conversion.
            if not _impl:
                _impl = self._parser.get
            return _impl(self._name, option, fallback=fallback, **kwargs)


    class ConverterMapping(MutableMapping):
        """Enables reuse of get*() methods between the parser and section proxies.

        If a parser class implements a getter directly, the value for the given
        key will be ``None``. The presence of the converter name here enables
        section proxies to find and use the implementation on the parser class.
        """

        GETTERCRE = re.compile(r"^get(?P<name>.+)$")

        def __init__(self, parser):
            self._parser = parser
            self._data = {}
            for getter in dir(self._parser):
                m = self.GETTERCRE.match(getter)
                if not m or not callable(getattr(self._parser, getter)):
                    continue
                self._data[m.group('name')] = None   # See class docstring.

        def __getitem__(self, key):
            return self._data[key]

        def __setitem__(self, key, value):
            try:
                k = 'get' + key
            except TypeError:
                raise ValueError('Incompatible key: {} (type: {})'
                                 ''.format(key, type(key)))
            if k == 'get':
                raise ValueError('Incompatible key: cannot use "" as a name')
            self._data[key] = value
            func = functools.partial(self._parser._get_conv, conv=value)
            func.converter = value
            setattr(self._parser, k, func)
            for proxy in self._parser.values():
                getter = functools.partial(proxy.get, _impl=func)
                setattr(proxy, k, getter)

        def __delitem__(self, key):
            try:
                k = 'get' + (key or None)
            except TypeError:
                raise KeyError(key)
            del self._data[key]
            for inst in itertools.chain((self._parser,), self._parser.values()):
                try:
                    delattr(inst, k)
                except AttributeError:
                    # don't raise since the entry was present in _data, silently
                    # clean up
                    continue

        def __iter__(self):
            return iter(self._data)

        def __len__(self):
            return len(self._data)


# This is for Python 3, should work with 3.5 and above
# yes it is short, because the Python 3.5 configparser module provides a lot
else:
    from configparser import *
    from collections import OrderedDict


# implementation for Python 3 and Python 2.7


def _convert_lines(value):
    """
    Split string value into lines and return this list without empty lines.
    """
    lines = [line for line in value.splitlines() if line]
    return lines


def _convert_listing(value):
    """
    Split string values by ',' trim the values and return it as list.
    """
    listing = [e for e in (elem.strip() for elem in value.split(',')) if e]
    return listing


class StdInterpolation(ExtendedInterpolation):
    """Interpolation based on the configparser.ExtendedInterpolation.

    Adds only the feature to be more tolerant and support ':' also in the
    section name.
    """

    def _interpolate_some(self, parser, option, accum, rest, section, map,
                          depth):
        rawval = parser.get(section, option, raw=True, fallback=rest)
        if depth > MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rawval)
        while rest:
            p = rest.find("$")
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            # p is no longer used
            c = rest[1:2]
            if c == "$":
                accum.append("$")
                rest = rest[2:]
            elif c == "{":
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise InterpolationSyntaxError(option, section,
                          "bad interpolation variable reference %r" % rest)
                path = m.group(1).split(':')
                rest = rest[m.end():]
                sect = section
                opt = option
                try:
                    if len(path) == 1:
                        opt = parser.optionxform(path[0])
                        v = map[opt]
                    elif len(path) == 2:
                        sect = path[0]
                        opt = parser.optionxform(path[1])
                        v = parser.get(sect, opt, raw=True)
                    else:
                        sect = ":".join(path[0:-1])
                        opt = parser.optionxform(path[-1])
                        v = parser.get(sect, opt, raw=True)
                        # raise InterpolationSyntaxError(
                        #     option, section,
                        #     "More than one ':' found: %r" % (rest,))
                except (KeyError, NoSectionError, NoOptionError):
                    raise from_none(InterpolationMissingOptionError(
                        option, section, rawval, ":".join(path)))
                if "$" in v:
                    self._interpolate_some(parser, opt, accum, v, sect,
                                           dict(parser.items(sect, raw=True)),
                                           depth + 1)
                else:
                    accum.append(v)
            else:
                raise InterpolationSyntaxError(
                    option, section,
                    "'$' must be followed by '$' or '{', "
                    "found: %r" % (rest,))


class StdConfigParser(ConfigParser):

    def __init__(self, defaults=None, converters=None, interpolate=False):
        _converters = {"lines": _convert_lines,
                       "listing": _convert_listing}
        if converters:
            _converters.update(converters)
        interpolation = StdInterpolation() if interpolate else Interpolation()
        super(StdConfigParser, self).__init__(defaults=defaults,
                                              dict_type=OrderedDict,
                                              allow_no_value=False,
                                              delimiters=('=', ':'),
                                              comment_prefixes=('#', ),
                                              inline_comment_prefixes=None,
                                              strict=True,
                                              empty_lines_in_values=True,
                                              default_section=DEFAULTSECT,
                                              interpolation=interpolation,
                                              converters=_converters)

    def read(self, filenames):
        super(StdConfigParser, self).read(filenames, "utf-8")

    # Needed for improved error messages if a converter fails
    def _get_conv(self, section, option, conv, **kwargs):
        try:
            return super(StdConfigParser, self)._get_conv(section, option, conv, **kwargs)
        except Exception as ex:
            ex.args += ("This error occured by getting option %r in section %r"
                        " with converter %r." % (option, section, conv.__name__), )
            raise

# If someone looks at this implementation,
# yes the ConfigParser of Python 3 is very powerful, used with good defaults
# and some useful converters you get a widely usable and powerful configuration
# parsing class with only these lines of code.
