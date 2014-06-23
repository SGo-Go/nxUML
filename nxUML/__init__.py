#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       nxUML
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
    m = "Python 2.7 or later is required for nxUML (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# Release data
from nxUML import release

__author__  = '%s <%s>\n' % (release.authors['Gogolenko'])
__license__ = release.license
__date__    = release.date
__version__ = release.version

#These are import orderwise

#from nxUML.brownie_doc import *
import nxUML.brownie_doc

import nxUML.core
from nxUML.core import *

import nxUML.parser
from nxUML.parser import *

import nxUML.drawing
from nxUML.drawing import *
