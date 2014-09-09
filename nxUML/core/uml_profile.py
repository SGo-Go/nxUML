#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_profile.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from networkx import MultiDiGraph
from nxUML.core.uml_class_primitives    import IUMLElement
from nxUML.core.uml_property            import UMLMetaproperty
from nxUML.core.uml_stereotype          import UMLStereotype, UMLMetaclass

######################################################################
class UMLProfile(IUMLElement, MultiDiGraph):
    """Profile class 
    """
    pass
