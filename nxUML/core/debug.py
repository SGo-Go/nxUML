#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         debug.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.

http://www.uml-diagrams.org/class-reference.html
http://support.objecteering.com/objecteering6.1/help/us/cxx_developer/tour/code_model_equivalence.htm
######################################################################
"""
from __future__ import print_function
def warning(*objs):
    import sys
    print("WARNING: ", *objs, file=sys.stderr)
def error(*objs):
    import sys
    print("ERROR: ", *objs, file=sys.stderr)
def debug(*args):
    import sys
    print("DBG: ", *args, file=sys.stderr)

__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""
