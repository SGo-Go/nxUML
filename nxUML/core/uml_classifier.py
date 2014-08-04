#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_classifier.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import UMLNamespace, UMLRedefinableElement

class UMLClassifier(UMLNamespace, UMLRedefinableElement):
    """An abstract metaclass which describes (classifies) set of instances having common features.
    The classifier is a type, templateable element, redefinable element, and namespace.
    """
    def __init__(self, name, scope, subclasses = None, **args):
        super(UMLClassifier, self).__init__(name=name, scope=scope, **args)
