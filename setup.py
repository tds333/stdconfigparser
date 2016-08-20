#!/usr/bin/env python
import sys
import os
from setuptools import setup


basepath = os.path.dirname(__file__)
with open(os.path.join(basepath, "stdconfigparser.py")) as cfgparser:
    versiondict = {}
    exec(cfgparser.read(), versiondict)
    version = versiondict["__version__"]


setup(name='StdConfigParser',
      version=version,
      description="A standard INI style configuration parser.",
      long_description="""\
This is the Python configparser with an extra class StdConfigParser.

Provides a standard configuration syntax and the parser for it.
Also contains everything to be a backport of the ConfigParser from
Python 3.5 to Python 2.7.
Everything in one module easy to vendor or install as extra dependency.
""",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='configuration config ini parser',
      author='Wolfgang Langner',
      author_email='tds333@mailbox.org',
      url='https://github.com/tds333/stdconfigparser',
      license='MIT',
      py_modules=['stdconfigparser'],
      tests_require=['pytest'],
      test_suite='pytest',
      include_package_data=True,
      zip_safe=True)
