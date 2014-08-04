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

from nxUML.core.uml_class_primitives    import UMLNamedPackageableElement

######################################################################
class UMLPackage(UMLNamedPackageableElement):
    def add_component(self, component):
        pass

    def __contains__(self, key):
        return False # @TODO implement check

    def __repr__(self):
        return str(self.full_name)

    def toXML(self, root = None, reference = False, scope = False):
        from lxml import etree
        if scope:
            xmlPackage = etree.SubElement(root, "scope")
            xmlPackage.set('name', self.name)
            xmlPackage.set('hrefId', self.id)
            xmlPackage.text = self.full_name
        else:
            if root is None:
                xmlPackage = etree.Element("package")
            else: xmlPackage = etree.SubElement(root, "package")
            xmlPackage.set('name', self.full_name)
            xmlPackage.set('hrefId', self.id)
        return xmlPackage

