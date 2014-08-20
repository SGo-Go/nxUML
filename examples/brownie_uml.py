#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         brownie_parser.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core import UMLInterfaceUsage, UMLInterfaceRealization, UMLInterface
from nxUML.core import UMLNone, UMLClassAttribute, UMLClassMethod

class UMLBrownieUsage(UMLInterfaceUsage):
    def __init__(self, uml_classifier, uml_iface, visibility, type = None):
        self.visibility = visibility
        self.type = type
        super(UMLBrownieUsage, self).__init__(uml_classifier, uml_iface)

    def toXML(self, root = None):
        xmlLink = super(UMLBrownieUsage, self).toXML(root)
        xmlLink.attrib['type'] = 'brownie::usage'
        xmlLink.attrib['visibility'] = self.visibility
        xmlLink.text = self.type
        return xmlLink

class UMLBrownieRealization(UMLInterfaceRealization):
    def __init__(self, uml_classifier, uml_iface, visibility, type = None):
        self.visibility = visibility
        self.type       = type
        super(UMLBrownieRealization, self).__init__(uml_classifier, uml_iface)

    def toXML(self, root = None):
        xmlLink = super(UMLBrownieRealization, self).toXML(root)
        xmlLink.attrib['type'] = 'brownie::realization'
        xmlLink.attrib['visibility'] = self.visibility
        xmlLink.text = self.type
        return xmlLink

# class UMLBrownieInterfaceStub(UMLDataTypeStub): pass
# class UMLBrownieCallStub(UMLBrownieInterfaceStub): pass
# class UMLBrownieNotificationStub(UMLBrownieInterfaceStub): pass

class UMLBrownieInterface(UMLInterface): pass

class UMLBrownieCall(UMLBrownieInterface):
    def __init__(self, name, 
                 scope         = None,
                 argument_type = None,
                 result_type   = None,
                 error_type    = None,
                 visibility    = '+ '):
        self.methods = (
            UMLClassMethod(name, rtnType = result_type, 
                           parameters = (('argument', argument_type),),
                           errors     = (error_type,),
                           visibility = visibility,
                           abstract   = True),)
        super(UMLBrownieCall, self).__init__(name, scope)

class UMLBrownieNotification(UMLBrownieInterface):
    def __init__(self, name, 
                 scope         = None,
                 value_type    = None,
                 argument_type = UMLNone,
                 visibility    = '+ '):
        self.attributes = (
            UMLClassAttribute(name, type = value_type, 
                              # default    = argument_type,
                              visibility = visibility,),)
        super(UMLBrownieNotification, self).__init__(name, scope)
