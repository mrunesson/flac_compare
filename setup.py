#!/usr/bin/env python

from distutils.core import setup

setup(name='flac_compare',
      version='0.1',
      description='Compare two flac files',
      author='Magnus Runesson',
      author_email='magru@linuxalert.org',
      url='http://www.linuxalert.org/flac-utils/',
      requires=['mutagen(>=1.19)'],
      packages=['flac_compare'],
      py_modules=['flac_compare'],
      package_dir={'flac_compare': 'src/'},
      license='GPL'
     )
