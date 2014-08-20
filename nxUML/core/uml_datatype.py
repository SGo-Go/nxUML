#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_datatype.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import IUMLElement, \
    UMLNamedElement, UMLTemplateableElement #, UMLNamespace
from nxUML.core.uml_multiplicity        import UMLMultiplicityStack
from nxUML.core.uml_classifier          import UMLClassifier
######################################################################
class IUMLDataType(UMLNamedElement): 
    def toXML(self, root = None, reference = False):
        from lxml import etree

        if root is None:
            xmlType = etree.Element("datatype")
        else: xmlType = etree.SubElement(root, "datatype")
        return super(IUMLDataType, self).toXML(xmlType, reference = reference)

######################################################################
class UMLPrimitiveDataType(IUMLDataType):
    @property
    def id(self): return self.name
    def __repr__(self): return self.name

    def toXML(self, root = None, reference = False):
        xmlType = super(UMLPrimitiveDataType, self).toXML(root = root, reference = reference)
        xmlType.set("type", "primitive")
        return xmlType

UMLInt       = UMLPrimitiveDataType('int')
UMLBoolean   = UMLPrimitiveDataType('boolean')
UMLNone      = UMLPrimitiveDataType('')
UMLChar      = UMLPrimitiveDataType('char')
UMLUndefined = UMLPrimitiveDataType('undefined')
UMLReal      = UMLPrimitiveDataType('real')

######################################################################
class UMLDataTypeStub(IUMLDataType, UMLTemplateableElement):
    def __init__(self, name, 
                 scope = None, 
                 parameters = [],):
        super(UMLDataTypeStub, self).__init__(name = name, 
                                              scope = scope, 
                                              parameters = parameters)

    def __eq__(self, uml_classifier):
        if isinstance(uml_classifier, UMLClassifier):
            return self.name == uml_classifier.name and self.scope == uml_classifier.scope
        else:
            super(self, UMLDataTypeStub).__eq__(uml_classifier)

    def __repr__(self):
        parameters = ','.join(map(str,self.parameters))
        return '{self.full_name}{parameters}'.\
            format(self=self,
                   parameters = '' if len(parameters) == 0 else '<%s>' % parameters)

    def toXML(self, root = None, reference = False):
        # return IUMLDataType.toXML(self, root)
        return super(UMLDataTypeStub, self).toXML(root, reference)

######################################################################
class UMLDataTypeDecorator(IUMLElement):
    def __init__(self, base, 
                 properties = [],
                 multiplicity = None):
        self.base         = base
        self.multiplicity = UMLMultiplicityStack() if multiplicity is None else multiplicity
        self._properties  = properties
        super(UMLDataTypeDecorator, self).__init__()

    @property
    def name(self): return self.base.name

    @property
    def scope(self): return self.base.scope

    def add_property(self, name):
        if not  self.__dict__.has_key('_properties') or self._properties is None: 
            self._properties = []
        self._properties.append(name)

    @property
    def properties(self):
        if self.__dict__.has_key('_properties') and self._properties is not None: 
            return self._properties
        else: return []

    def __repr__(self):
        strMulti = str(self.multiplicity)
        return r'{self.base}{multi}{properties}'.\
            format(self=self, multi = '[%s]' % strMulti if len(strMulti) > 0 else '',
                   properties = "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),)

    @property
    def composite(self):
        return len(self.multiplicity) == 0 or self.multiplicity[0].composite

    def toXML(self, root = None, reference = True):
        from nxUML.core.uml_class import UMLClass

        if isinstance(self.base, UMLClass):
            xmlType = UMLDataTypeStub(self.base.name, self.base.scope).toXML(root = root)
            # print self.base.id
            xmlType.set("hrefId", self.base.id)
            xmlType.set("type", "class")
        else: 
            xmlType = self.base.toXML(root = root, reference = True)

        if not self.composite:
            xmlMulti = self.multiplicity.toXML(xmlType)
            # xmlType.set("multiplicity", str(self.multiplicity))

        return xmlType
