#!/usr/bin/env python

from distutils.core import setup

setup(name='flac_compare',
      version='0.4.0',
      author='Magnus Runesson',
      author_email='magru@linuxalert.org',
      url='http://www.linuxalert.org/project/flac-utils/',
      description='Compare two flac files',
      long_description="""Compare two flac files using the metadata in the
      file. Both audio part and tags can be compared.""",
      requires=['mutagen(>=1.19)'],
      packages=['flac_compare'],
      py_modules=['flac_compare'],
      package_dir={'flac_compare': 'src/'},
      license='GPL'
     )
