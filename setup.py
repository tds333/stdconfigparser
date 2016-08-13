#!/usr/bin/env python
import sys
import os
from setuptools import setup

from stdconfigparser import __version__ as version


setup(name='StdConfigParser',
      version=version,
      description="A standard INI style configuration parser.",
      long_description="""\
TODO
""",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Text Processing',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='configuration config ini parser',
      author='Wolfgang Langner',
      author_email='tds333@gmail.com',
      url='https://github.com/tds333/tempita-lite',
      license='MIT',
      packages=['stdconfigparser'],
      tests_require=['pytest'],
      test_suite='pytest',
      include_package_data=True,
      zip_safe=True,
      **kwargs
      )
