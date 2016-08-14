Introduction
============

This module provides a StdConfigParser class a simple
standard INI configuration parser with a specified format. All is based
on the Python standard library configuration parser.
For Python 2.7 it contains also a backport of the Python 3 ConfigurationParser
class.

Additionally it extends the configuration parser with useful converter methods.
They allow really powerful configurations by keeping all simple for the user.

An Example is better than a lot of words:

.. code-block:: ini

	[section]
	key = value

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
	name = ${section:key}


As you can see a lot is possible with simple INI style syntax.
The StdConfigParser class uses the ConfigurationParser from Python with
specified defaults and additional powerful converters.
A standard configuration format for all of your applications.
Easy to embed or use as a standalone module. All distributed as one file.

You can also use this module in Python 2 as a back port of the Python 3
configuration parser module. Even if you don't want to use the StdConfigParser
class. It is the only back ported module distributed as single file. Easy
to vendor and distribute it as private part of your application.
If you don't need the extra power of the converters, keep in mind they are
optional, everything is also usable for the simplest key value configuration.



Human readable configuration
----------------------------

First everyone should know, if a configuration is directly used by humans
it is a user interface and should be threated so.
Second, keep it as simple as possible.

The long story. Be careful by trying to invent your own configuration format.
A lot of people had tried this before and there are a lot of formats available.
I did the same, it is fun to invent an own format that is really better and
has more features and ... But at the end it is really one other format not
revolutionizing the world and swamped away by the next wave of this configuration
syntax is better "invention".
Sit down think some minutes (for me this took months not minutes) go back and
ask yourself what is the real goal.
For me the requirements are:

1. It must be simple, have not that much time to learn another new configuration
format.
2. I (a human) have to read and write stuff in this format. So it should be
based on text I can read and write with a simple text editor.
3. It should allow me to customize some parts of a program or application. I
don't want to change source code for it nor I want to write program logic in the
configuration.
4. If possible, have the configuration for my applications in one place, best is
to have it in one file. So I don't have to search through the file system.

All this is not very specific and your needs may be more detailed and you have
more requirements. But for me it comes down to:
I want something where I can specify configurations keys and assign a value to
them. If I want to do everything in one file I need also a way to say something
like this belongs to that part of my application. I need to split it up and
name the sections.
The result of this is a format already know by lot of people it is called the
INI style configuration format. It is not specified in detail, but simple to use
and fulfills all my needs. And yes all needs for a good human readable
configuration format. But there is only one problem. It is not specified in
detail. The key value separator varies and other things like comments. Even
nuances about word case. To be interchangeable this has to be specified.
This module tries to specifies the format in more detail
and provides a parser for it in Python.


Features
--------

- Already known by most people. INI Style format is there for years.
- Simple key value string only. (at user level)
- Extends only the value part to support more advanced needs.
- Reduced to have only one preferable way to write something.
  In this case use the most widely used characters (= to assign, # to comment)
- Keys are case insensitive, so forgive the user if he/she did not know the
  exact spelling
- Flat structure, only one level. (no sections in sections)
- Allow complex stuff but only if needed. Start simple but can scale.
- The programmer decides how complex a value is and how to parse a value
  for the user it is still a simple string.
- The user must only know sections, comments, keys, values and multi line values.
  Nothing more is needed to get the configuration syntax right.
- Substitution is supported by the "${KEY}" interpolation format.

Ultimate goal: Become the standard way for Python applications to configure
something and be the one interchangeable user readable configuration format.
So everyone knows it and uses it. Don't rule the world only a title part of it.


Why do I care about a configuration format?
-------------------------------------------

Valid question, simple by my own use case and needs and because I am a little
tiered to learn the next new better format with advanced features.
But my main motivation is to bring in mind: If the configuration is there to be
used by humans sit down think a minute and make it really friendly and
human usable. I added friendly because this is essential for me. Forgive the
users also some errors they are not perfect and I am a user too.
Define a format usable for a lot of stuff. But not to complex and yet powerful.
Hopefully everyone loves it and then uses it.

Some words about other know formats:

TOML - Also useful solves more complex problems. But no final specification
       and tries to solve problems to complex for most users.
       Supports nested mappings and lists in a way like a programmer will do it
       but not as a user will like it. Don't burden the user of the
       configuration with your preferred result structure. If the configuration
       format supports deeply nested configuration syntax. Someone will use it
       and then it is no longer easy for the user. The syntax is one step to
       complex to be easy and user friendly.

YAML - Initially looks nice and the real solution for every configuration need.
       But at the end, it is complex and there are to many ways to specify
       something. Also parsers are not easy to implement in a correct way for
       it. The user gets the load of the structure the programmer wants.
       It is not forgiving to user errors and does not avoid complex structures
       hence not that user friendly at the end. It is only good if your
       configuration is simple but in this case also has a more complex syntax.
       Everytime I have to write YAML configuration, first I must consult the
       manual of the package and the YAML specification to do it right.
       The syntax is twos steps to complex to be easy and user friendly.

JSON - Good interchangeable serialization format but not so good for
       configuration. Allows no comments. Syntax is to complex and error prone
       for simple configuration needs. To use it as a configuration syntax it
       must be extended and you create your own new format no longer compatible
       with bare JSON.
       But can be usable to specify complex values. It is widely know and the
       basic syntax is easy. Good parser support for a lot of languages.

XML - Verbose and the user must know how to program. Open close tags needed,
      other stuff only in attributes. Allows deep and complex structures by
      nesting. In the end it is not easy and most of the time not really human
      readable. Avoid XML as user interface if you can. It may be the solution
      for other problems but not for configuration.


At the end, I have really tried a lot of formats and used them. Also written my
own. Learned a lot over time. Came to the conclusion: Keep your configuration
as simple as possible. This implies also, don't write the configuration only
for your needs write it for none programmer users in mind. Avoid deep nested
structures and don't require knowledge from your users about dictionaries or
lists and nested structures. Also not about how to format integer or strings
in the syntax. Really, keep it simple. Every format listed above avoids this
in one or another way.


My configuration history (in short)
-----------------------------------

In the past 20 years I had to work with a lot of configuration formats.
The worst human readable ever was XML. Some years ago with the XML hype arising
my first choice was also to do new configuration in XML. But XML is not good for
human readable configuration stuff. Also not as a script like language. It
may be a good data exchange format but solves not every problem on earth.
And really solves nothing in the are like configuration and scripting.
Good luck, I invented never a big enough XML configuration format only had to
use some. One of my first configuration style formats I had to use was the
INI style based format. Most used on Windows years ago even before the registry
arises. I used a lot of formats starting from the Apache style config due to the
Zope xml style config and nearly everything between. Have written some parsers
for own invented config formats and also tried to invent the next best format
capable to handle a lot of use cases.
But for all of this I have noticed the really first one is still one of the best.
Why? It is simple. The simplest configuration format nearly every one understood
from the beginning is something like you have a key and it has a value.
The INI style adds to this only something like sections. Which allows to have
different configurations in one file. At the end of my configuration history I
am back to the beginning. Simple key value with a bonus.


The specification
=================

In short:

.. code-block:: ini

    [section]
    # comment
    key = value

All Unicode, if a file it must be UTF-8 encoded.

That is all you must know to write and read configuration files in the specified
format. But I will go into detail with examples for more parts of the specification.
You can also call it a defined variant of an INI style configuration format.

The configparser module in Python 3 is really good, it can and will be used to
parse the specified "standard" format here. Also I explain my decisions for
a choice in detail.

First we must limit the possibilities. Most INI style formats allow more than
one way to do something. But the standard format here limits this to one way.


Comments
--------

Are line based start simple by "#" character. Inline comments are not allowed.
This is to prevent errors in a value where the character "#" also can be present.
Spaces in front of "#" are allowed so indention of comments is possible.

.. code-block:: ini

    [section]

    # this is a comment
        # this is also a comment only indented

    key = value # not a valid comment

    key = value; also not a valid comment


The ";" character as an additional comment character is not allowed. Also in
some variants the ";" is used for inline comments. To prevent errors and provide
only one way this is not allowed. This opens also the possibility to use ";" as
a path separator for values.

Keep in mind comment lines are handled by the parser and remove before you get
the value out of the parser. This is also the case for multi line values where
every line starting with "#" will be removed.
This allows to have comment lines in every format of multi line values.
Even if you decide you parse the value as JSON or another fancy not yet invented
format.


Sections
--------

Are there to separate different parts of your configuration. Also to have
configuration of different programs in the same file.

A section starts with a "[" and ends with a "]" all between is part of the
section name (case sensitive). As with comments sections can be indented but
try to avoid this.
It implies a structure and this structure is not there when parsed.
Also avoid ":" in the section name. Later on this for interpolation.

.. code-block:: ini

    [section]

    [another_section]


Best is to have some convention if you want to do something special with sections.
Section name = Program name.
You have an application library "myfantastic" with a configuration need. Not
very complicated only needs some key value settings.
Use the section name "myfantastic" (good is to use the same name as your Python
package or module name) and place the whole configuration in this section.

.. code-block:: ini

    [myfantastic]
    port = 1811
    loglevel = debug

    [anothermodule]
    bird = fly

This allows having configuration for other libraries, applications in the same
file. Your module is only interested in your section.

A second convention, sometimes you have the need to structure your configuration
more deeply and have nearly similar sections describing the parts.
Still use one section with your module/package name, this is your main configuration
section. For the other more detailed configuration sections prefix your module
name followed by a space. The space is the separator. Don't use other characters
and avoid the ":" in the section.

Example:

.. code-block:: ini

    [mymodule]
    environmentlist = py27,py34,py35

    [mymodule py27]
    path = /py27

    [mymodule py34]
    path = /py34

    [mymodule py35]
    path = /py35


Here the main module has a list of environments, each environment has it's own
path configuration. My preference is to list the environments in the main module
section and make all explicit. It allows also to do something like
having a key "active_environments" and list there the active ones. So the user
can leave the other in the configuration and declare the active ones.
But it is also enough to have only the sections. You can easily iterate the
sections and filter out every section starting with "mymodule ". (space at the end)
If the space is not yours. Consider using the "." as an alternative separator.
But keep your module/package name in front.
All this avoids also clashes with section names of other modules/packages.

If you have a complex package with different levels of configuration needs
another solution is to use the full module name as configuration structure
in sections.

Example:

.. code-block:: ini

    [myxml.parser]
    validate = true

    [myxml.writer]
    prettyformat = true

    [myxml.logger]
    level = debug


This is really seldom needed best is still to have all in one section with
good documented keys. But if your modules are really independent and have their
own configuration this is also a possible way to separate stuff and avoid name
collisions. You can still find every section for myxml by filtering them by
"myxml.". In this case the amount of configuration sections is defined by your
installed modules. A good indicator for such a use case is if "myxml" is a
namespace package.


Keys
----

Keys start at position one in a line and are all lower case. That said, it is
good to write them lower case in the configuration file because they will be
lowered lated by the configuration parser. In your application you also will
access them in lower case. For your user, the are case insensitive. This avoids
confusion about should I use camel case for this key or must I use a big letter
there. Keys are essential so be forgiving there is the motto.
I said start as position one in a line, the exact meaning is, ok indention is
allowed also but if possible avoid it.

.. code-block:: ini

    [section]
    key = value
    AnotherKey = no good example because camel case but allowed
    anotherkey = same as "AnotherKey", but duplicates are not allowed


Values
------

Now the interesting part comes. Values are simple strings and it is up to the
application to handle them. For the user of your configuration, they are
really simple strings but you can make them more useful if you want.
Try to escape the "$" sign with "$$" if you use interpolation. No other
specialties needed to be known. Or simple, in valid values for your application
do not use "$" if possible. So the user has not to care about it.
That said, we will specify some standard enhancements here also.
But to start simple:

.. code-block:: ini

    [section]
    key = value
    next_key = Value with spaces in the string
    integer = 1
    float = 1.5
    bool = true

All values are valid. If you simple get them in your application they are all
strings. It is up to the application using the configuration parser what to
get out of them. But more about this later.
It is allowed to have values over multiple lines. The value is still a simple
string for the user and the interpretation is up to you. Multiline values must
be indented to distinguish them from a key and make them part of the value.

Example:

.. code-block:: ini

    [section]
    multiline = This value is over
    			multilple lines
    			and another one

    [section2]
    multiline2 =
    	event this is
    	a
    	multiline
    	value

    [section3]
    multiup =
    	comments are
    	allowed
    	# my comment
    	in the value
    	event

    	empty lines


As you can see, the user has the possibility to write values over multiple lines
they have only to be indented. This can be very useful to list something
or only to have a bigger string. But all this is up to the application.
But the StdConfigParser will help you in this area. More about it later.

For multi line values keep in mind they must be indented, use same indent level
for every line. The indention is cleaned up by the parser for you. You get still
one big string.


Default section
---------------

This is a feature sometimes useful and inherited from the Python library
configuration parser. There can be a default section in your configuration
file. You are normally free to name it, the StdConfigParser uses the default one
named "DEFAULT". Yes in big letters and this is fixed.
Can look ugly, but most of the time you don't need this section. And if needed
by a user it is really visible and good named.
Why should I avoid to use it?

Because the application should uses good default values and
uses the defaults parameter of the parser there is no need to have them also
in the file. The need to have them because of interpolation is also lowered.
We can specify the section explicitly.

For all of this, keep in mind, there can be a special section in a file called
"DEFAULTS". If you see it remember my words about it.
If you use the write method of the parser you will also see these defaults.



Interpolation
-------------

Only mentioned before but not described in detail.
I self thought long about it, should it be part of the StdConfigParser or not.
For me the conclusion was, it is useful for the end user and can help him/her
a lot. But if not needed in the configuration to have it will not disturb.
The user decides to use it. And because most users are lazy like me and don't
want to change the same value at 1000 places they will use it. It is also
super elegant solution to provide and describe default values.

One possible way is to have an option at the parser for it. But I want to
have one standard way and not two ways. So I decided it is there.
After this the decision for the format was really easy. We use simply the
extended interpolation format of Python configparser module.
Interpolation for the configuration is simple a replace "this by that" at access
time. It is not like a template at parsing time. Really when you access the
key the replacement is done every time again when you access the key. No cache
you are up to date for changes in other places. Don't care about performance
it is not the problem at configuration level. Here we care about most up to date
and good usable defaults. Even if someone changes something at another level.
This is a feature you will later as a user and programmer learn to love and
understand the full power of it.
Lot of other configuration solution do this wrong and prefer performance over
up to date values, which is not what a user want.

Enough text, the format is simple: ``${key}`` to insert the value of the key
when accessing. Or over sections: ``${section:key}``

.. code-block:: ini

    [myapp]
    path = /user
    log_path = ${path}

    [otherapp]
    path = ${myapp:path}/other
    dollarsign = $$



Interpolation can simplify the live for the user by having to specify the
value in one place and use it also in another place.
It can also simplify the application developers live by using it for good
default values.
Because of the ":" as separator between section and key, avoid the ":" in
sections. If your section uses ":" in the name it cannot be used in complex
interpolations. It is still not an error. Because if you decide to not
interpolate something or interpolate only at application level. All is still
fine.
To use the ``$`` sign escape it with another one and use ``$$``.


Interface
---------

Is really a thin wrapper around the Python library ConfigParser with sensible
default values chosen. So you don't have to think about it. You can simple use
this library and it's additional goodies.

The Python standard library configuration parser has a really long list of
options. The StdConfigParser will simplify this to two. I'll describe in detail
the default set for you.

Python ConfigParser init option:

defaults=None

This is a dictionary with your default values. So useful you will get it also
with the same default.

dict_type=collections.OrderedDict

Good default choice, the module uses the default and does not provide an option
here.

allow_no_value=False

Good default. Use the same and will not provide this option. It brings up
configuration errors earlier. If the user has forget to specify a value this will
be an error.

delimiters=('=', )

The StdConfigParser allows only "=" as key value delimiter. No changes possible.

comment_prefixes=('#', )

The StdConfigParser allows only "#" as a comment prefix. One way is enough to
comment.

inline_comment_prefixes=None

The default is used and not provided as option to the outside. It is also good
to have no inline comment prefix. As the documentation states, it can prevent
some characters in values or have wrong values.

strict=True

Default is used not provided to the outside. Don't allow duplicate sections or
options. The user will get errors earlier.


empty_lines_in_values=True

We allow this and it is good for multi line values. Cannot be changed.


default_section=configparser.DEFAULTSECT

We use the default and provide this option not to the outside.


interpolation=ExtendedInterpolation()

We use the ExtendedInterpolation class. But this is not optional.


converters=None

Instead of the default "{}" we use None. I don't like mutable default values.
But internally an empty dictionary is used as default. This option is the second
one available. Can be useful for your own converter functions. But keep in mind
don't overact it. The StdConfigParser provides two additional one for you.


Goodies
-------

Sometimes you need a little bit more than a simple string as a value.
The ConfigParser provides converter functions for you for the most basic
types like: int, bool, float usable by parser.getInt(), parser.getfloat()
and parser.getboolean() function.
If you use these functions the value will be converted for you as specified.
And yes by using converters you can really do a lot. Still keeping the
configuration format simple but providing real benefit for your application.

Here comes the difference of the StdConfigParser to other configuration formats.
It invents not a completely new configuration syntax nor a complete new parser.
It uses the existing stuff and specifies and extends it where useful.

Often there is the need to have a more complex configuration structure.
Multiple values nested structure and more. I know the real need but as most
other people did the wrong and mad all this part of my configuration syntax.
Complicating everything.
The StdConfigParser does this not. The user of a configuration file should not
learn a new syntax. Everything is section, key (option) value format. The value
is documented by the application how the string is interpreted.


Multiple values
---------------

For most configurations there are extended use cases. One is to specify a
list of values. The simplest way for an user is to specify this line by line,
every line is a value. For the application this is the method "getlines".
A simple helping converting allowing a easy multi line value syntax.

Example:

.. code-block:: ini

    [section]
    multiline = value 1
                value 2
                value 3
                # comment for four
                value 4

                value 5

    simple_indent_multi_is_enough =
    	line 1
    	line 2
    	line 3


As you can see, simple valid multi line syntax. Easy for the user to see this
is a list of values.
The "getlines" function on the parser does all other for you. It returns a list
with the string values for you. Every line is one value in the list. Comments
and empty lines are removed. So you get a clean list and the user has the
possibility to comment it values and have empty lines to separate some values.

Even for your application you can still do some other list handling like
the values are separated with "," and in one line and have a custom parser for
it. I recommend simple use the getlines function and multiline value feature
for this use case.


Advanced value syntax
---------------------

Sometimes, hopefully never, you have the need for more complex configuration
structure. If you cannot avoid it and you really need something like a deeper
structure or you have demand of types in your value lists I have also a solution
for it. The solution is JSON. Why? What?
Yes in this complex case I don't reinvent the wheel. Most users for a
Python application are already familiar to the Python syntax and JSON is nearly
similar. It is documented and easy to read/write.
But you may ask, I want to comment complex stuff. The answer is, yes you can.
Comments are handled by the ConfigParser in a normal way. Only line comments are
allowed. Also empty lines. But value indent must also be kept for JSON values.
Even if you use JSON values keep in mind the value is handled as multi line
string by the parser before you get it.
I considered also providing ast.literal_eval(). But after first test, removed it
in favor of using JSON. There is one simple problem with literal_eval, if you
have a demand for Python 2 you will be in the bytes, str, unicode hell of it.
In this case it is really not easy to write configuration code working with
Python 2 and Python 3. And the configuration should be all unicode strings.


Example:

.. code-block:: ini

    [section]
    key = ["some value in a list"]

    object = {"data": "in a dict", "x": 10}

    now_it_gets_complex = {
    	"key": "value",
    	# with comment
    	"feature": "over multiple",

    	"lines": 7,
    	"5": ["in", "a", "list", true, null, 3.14]
    	}

    event_interpolated = [${object}, {}, "it works"]



As you can see, these are still valid string values but if you use
the "getjson" method of the parser, the value will be parsed for you
and you get back the Python values. Comments are allowed, empty lines also
as know by multi line configuration values. The user has the possibility
to write it in a readable way. The application let Python parse the syntax in
a safe way. This is really powerful. You can do nearly all complex configuration
needs with it. Even to complex for the users. Keep this in mind.
If you know this, use it only for the configuration keys where it is really
needed. You have the power but your users must be able to handle it.

Not complicated enough? Even the interpolation in the last line works as expected.
Keep in mind the interpolation is still a simple string interpolation on access
before the converter is called. The result of the interpolation must be valid
JSON.


Style guide
===========

Yes it makes sense to have also a style guide for configuration. The format
allows some stuff and not everything is an error but considered bad style.


Sections
--------

White space before and after the section name are allowed but everything between
the "[" and "]" is the section name. So don't use spaces before or after the
section name. Also the name is case sensitive, to keep it simple use only lower
case letters for the name.

Sections can be indented but avoid this. Even if you do something like
partitioning of the section name. Keep it flat.

Example:

.. code-block:: INI

    # good style
    [mymodulename]

    # bad style
    [  mymodule  ]

        [mymodule]


Keys and values
---------------

Use a space before the "=" and after it. You cannot prevent your users from
doing different things but for best practice in documentation and for your
default configuration use this style.

Example:

.. code-block:: INI

    # good style
    [mymodule]
    key = value

    # bad style
    keybad1=value
      keybad2 = value
      keybad3=value


Indention
---------

Is usefull for values to have them over multiple lines. Try to use it only in
this case. Try to use the same indention level. Preferred are four spaces.
Same as the Python standard. Don't indent sections. Don't use multiple levels
of indention. Keep it simple for your user. Everytime something is indented it
should be a sing for a multiline value, nothing more.
Only if you use complex value format like JSON, it makes sens to use additional
indention. But in this case it should be only for visibility.

Example:

.. code-block:: INI

    # good style
    [mymodule]
    key = value over
        multiple
        lines

    another =
        multi
        line
        value

    # bad style
    keybad1 = value over
      multiple
        lines

      keybad2 = value
        multi
        line

    keybad3 =
        value
           more value
              more value



Examples
========

Examples describe a special use case and the solution how to handle
this with the StdConfigParser.

Simple
------

You need a configuration for a small module only with some configuration
keys. No need for a nested configuration.

In this case you will have one line overhead, the section. Use the same
name as your module or package as section name. This enables later use
of one configuration file for different packages. Even if you don't need it
know, it is for interoperability.

Example:

Your module or package name is 'mymodule'

.. code-block:: INI

    [mymodule]
    data_dir = /data
    temp_dir = /temp

In your program code create the config parser instance retrieve the section
and only use your section.

.. code-block:: Python

    from stdconfigparser import StdConfigParser

    def get_config(path):
        parser = StdConfigParser()
        parser.read(path)
        config = parser["mymodule"]
        return config

    def main():
        config = get_config("~/mymodule.cfg")
        data_dir = config.get("data_dir")
        temp_dir = config.get("temp_dir")

Defaults
--------

List of values
--------------

Multiple sections
-----------------

Interpolation and defaults
--------------------------

Config file with interpolation
------------------------------

Your use case is to have a configuration file in a specific configuration
directory. The directory path should also be usable in the configuration
as interpolation value.

Use the defaults parameter to set the configuration directory.

.. code-block:: INI

    [mymodule]
    project_dir = ${config_dir}/..
    log_dir = ${project_dir}/log
    temp_dir = ${project_dir}/tmp


.. code-block:: Python

    import os
    from stdconfigparser import StdConfigParser

    def get_config(path):
        config_dir = os.path.abspath(os.path.dirname(path))
        parser = StdConfigParser(defaults={"config_dir": config_dir})
        parser.read(path)
        config = parser["mymodule"]
        return config

    def main():
        config = get_config("~/mymodule.cfg")
        project_dir = config.get("project_dir")


Environment
-----------

The os environment information is needed in the configuration as as
interpolation value.
The solution is simple, add a section with this information before you read
your configuration. Don't write it to the default section, make it explicit
into a new documented section. In the configuration this section can be used
for substitutions. Document also the environment information will not be updated
it is only read at startup.

.. code-block:: INI

    [mymodule]
    project_dir = ${os.environ:home}

In this example the environment section is simply named by the Python module path.
``os.environ``. But if you prefer a shorter solution you can use the name ``env``
which is also common to name the environment.
The environment information is also read before the configuration, this allows
overwriting in the configuration file. Can be used as a feature for testing.

.. code-block:: Python

    import os
    from stdconfigparser import StdConfigParser

    def get_config(path):
        parser = StdConfigParser()
        parser.read_dict({"os.environ": os.environ}, "environment")
        parser.read(path)
        config = parser["mymodule"]
        return config

    def main():
        config = get_config("~/mymodule.cfg")
        project_dir = config.get("project_dir")


Complex
-------

Your users are mainly programmers and already familiar with JSON.
You cannot resist and want to provide powerful features at configuration level.


Config file includes
--------------------

In a big application sometimes there is the need to have more than one
configuration file. But one main file should be used to specify the other
include files.

In this case best is to donate a special key named ``include`` with multi line
values to name the additional files. Try to avoid recursive includes and other
more complex stuff here. A feature you thought to be useful can bring you
near to the hell.

Best here is to support absolute paths and relative paths. Where a relative
path starts with a ``.`` (dot) and is relative to the specified configuration
file.

.. code-block:: INI

    [mymodule]
    include = ./names.cfg
              ./connections.cfg
              /etc/mymodule.cfg

    project_name = lotincludes

To solve this we read the main configuration file to get the included ones.
Build the paths for the files to handle the relative ones.
Read them and overwrite the result with the main configuration. Because this
is what most users expect.


.. code-block:: Python

    import os
    from stdconfigparser import StdConfigParser

    def get_config(path):
        config_dir = os.path.abspath(os.path.dirname(path))
        main_config = StdConfigParser()
        main_config.read(path)
        config_include = main_config.getlines("mymodule", "include", fallback=[])
        includes = []
        for include in includes:
            if include.startswith("."):
                include = os.path.abspath(os.path.join(config_dir, include))
            includes.append(include)
        config = StdConfigParser()
        config.read(includes)
        config.read_dict(main_config)
        return config

    def main():
        config = get_config("~/mymodule.cfg")
        project_dir = config.get("myproject", "project_dir")

