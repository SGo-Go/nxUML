#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         __iniy__.py
@author       Sergiy Gogolenko

Root init-file.
######################################################################
"""

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for NetworkX (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# Release data
from networkx import release

__author__  = '%s <%s>\n' % (release.authors['Gogolenko'])
__license__ = release.license
__date__    = release.date
__version__ = release.version

#These are import orderwise

#from DoxyUML.brownie_doc import *
import DoxyUML.brownie_doc
