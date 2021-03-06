#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_package.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives import UMLNamespace

######################################################################
class UMLPackage(UMLNamespace):
    def add_component(self, component):
        pass

    def __contains__(self, key):
        return False # @TODO implement check

    def __repr__(self):
        return str(self.full_name)

    @property
    def tag(self):
        """Specifies XML tag `package' for the serialized instances of UML packages
        """
        return 'package'

    def toXML(self, root = None, reference = False):
        xmlPackage = super(UMLPackage, self).toXML(root = root, reference = reference)
        return xmlPackage
