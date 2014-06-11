#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         setup.py
@author       Sergiy Gogolenko

Setup script for DoxyUML.
You can install DoxyUML with 'python setup.py install'
######################################################################
"""
from glob import glob
import os
import sys
# if os.path.exists('MANIFEST'):
#     os.remove('MANIFEST')

from setuptools import setup

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 7):
    print("DoxyUML requires Python 2.7 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

# Write the version information.
sys.path.insert(0, 'DoxyUML')
import release
version = release.write_versionfile()
sys.path.pop(0)

packages=["DoxyUML",]

docdirbase = 'share/doc/doxyuml-%s' % version
# add basic documentation
data = [(docdirbase, glob("*.md"))]
# add examples
for d in []:
    dd = os.path.join(docdirbase,'examples', d)
    pp = os.path.join('examples', d)
    data.append((dd, glob(os.path.join(pp ,"*.py"))))
    data.append((dd, glob(os.path.join(pp ,"*.hpp"))))
    data.append((dd, glob(os.path.join(pp ,"*.json"))))

# add the tests
package_data = {
    'DoxyUML': ['tests/*.py'],
    }

install_requires = ['networkx >= 1.8.0', 'CppHeaderParser >= 2.0.0']

if __name__ == "__main__":

    setup(
        name = release.name.lower(),
        version = version,
        maintainer = release.maintainer,
        maintainer_email = release.maintainer_email,
        author = release.authors['Gogolenko'][0],
        author_email = release.authors['Gogolenko'][1],
        description = release.description,
        keywords = release.keywords,
        long_description = release.long_description,
        license = release.license,
        platforms = release.platforms,
        url = release.url,
        download_url = release.download_url,
        classifiers = release.classifiers,
        packages = packages,
        data_files = data,
        package_data = package_data,
        install_requires = install_requires,
        test_suite = 'unittest',
        tests_require = ['unittest'],
        zip_safe = False,
        )
