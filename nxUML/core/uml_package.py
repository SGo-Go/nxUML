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

from nxUML.core.uml_class_primitives    import UMLNamespace

######################################################################
class UMLPackage(UMLNamespace):
    def add_component(self, component):
        pass

    def __contains__(self, key):
        return False # @TODO implement check

    def __repr__(self):
        return str(self.full_name)

    def toXML(self, root = None, reference = False):
        if reference:
            from nxUML.core.uml_datatype import UMLDataTypeStub

            xmlPackage = UMLDataTypeStub(self.name, self.scope).toXML(root)
            xmlPackage.set("hrefId", self.id)
            # xmlPackage = etree.SubElement(root, "datatype")
            # xmlPackage.set('name', self.name)
            # xmlPackage.set('hrefId', self.id)
            # xmlPackage.text = self.name
        else:
            from lxml import etree
            if root is None: 
                xmlPackage = etree.Element("package")
            else: xmlPackage = etree.SubElement(root, "package")
            xmlPackage = super(UMLPackage, self).toXML(root = xmlPackage, reference = reference)
            # # xmlPackage.set('name', self.name)
            # xmlPackage.set('name', self.name)
            # xmlPackage.set('hrefId', self.id)
        return xmlPackage

