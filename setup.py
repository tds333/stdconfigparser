#!/usr/bin/env python
import sys
import os
import runpy
from setuptools import setup


basepath = os.path.dirname(__file__)
versiondict = runpy.run_path(os.path.join(basepath, "stdconfigparser.py"))
version = versiondict["__version__"]
#with open(os.path.join(basepath, "stdconfigparser.py")) as cfgparser:
#    exec(cfgparser.read(), versiondict)

with open(os.path.join(basepath, "README.rst")) as readme:
    long_description = readme.read()

setup(name='StdConfigParser',
      version=version,
      description="A standard INI style configuration parser.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Text Processing',
          'Topic :: Software Development :: Libraries',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='configuration config ini parser configparser configuration',
      author='Wolfgang Langner',
      author_email='tds333@mailbox.org',
      url='https://github.com/tds333/stdconfigparser',
      license='MIT',
      py_modules=['stdconfigparser'],
      tests_require=['pytest'],
      test_suite='pytest',
      include_package_data=True,
      zip_safe=True)
