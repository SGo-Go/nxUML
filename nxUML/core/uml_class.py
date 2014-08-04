#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_class.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""


from nxUML.core.uml_classifier import UMLClassifier

######################################################################
class UMLClass(UMLClassifier):
    """Unified (language independent) representation of class
    """
    def __init__(self, name, 
                 location = None, 
                 scope  = None,
                 methods  = [],
                 attribs  = [],
                 modifiers  = [],
                 subclasses = None,
                 parent   = None,):

        # Fill data
        self.location   = location

        self._modifiers = modifiers
        self.methods    = methods
        self.attributes = attribs

        # Fill dependencies 
        self.parent       = parent

        self.realizations = []
        self.usages       = []

        super(UMLClass, self).__init__(name = str(name), scope = scope, subclasses = subclasses)

    def add_attribute(self, attrib):
        self.attributes.append(attrib)
        # if attrib.is_utility: self._utility = False

    def add_attributes(self, attribs):
        if not self.__dict__.has_key("attributes") or self.attributes is None:
            self.attributes = attribs
        else: self.attributes.extend(attribs)

    def add_method(self, method):
        self.methods.append(method)

    def add_methods(self, methods):
        if not self.__dict__.has_key("methods") or self.methods is None:
            self.methods = methods
        else: self.methods.extend(methods)

    def add_realization(self, iface_id):
        self.realizations.append(iface_id)

    def add_usage(self, iface_id):
        self.usages.append(iface_id)

    # @property
    # def id(self):
    #     return self.name

    @property
    def modifiers(self):
        modifiers  = []
        if self.is_interface: modifiers.append('interface')
        if self.is_utility:   modifiers.append('utility')
        modifiers.extend(self._modifiers)
        return modifiers

    def has_modifiers(self):
        if self.is_interface:     return True
        if self.is_utility:       return True
        if len(self._modifiers): return True
        return False

    def add_modifier(self, modifier):
        self._modifiers.append(modifier)

    @property
    def is_interface(self):
        if len(self.attributes) > 0:
            return False
        for method in self.methods:
            if not method.is_destructor and not method.is_abstract: 
                return False
        return True

    @property
    def is_utility(self):
        for attrib in self.attributes:
            if not attrib.is_utility: return False
        for method in self.methods:
            if not method.is_destructor and not method.is_utility: return False
        
        return True

    def __str__(self):
        modifiers  = self.modifiers
        return "{line}\n{modifiers:^40}\n[{self.scope}]{self.name}\n{line}\n{attributes}\n{line}\n{methods}\n{line}".\
            format(self=self, line= chr(196)*40, #unicode('\x80abc', errors='replace')*
                   attributes = "\n".join(map(str,self.attributes)),
                   methods    = "\n".join(map(str,self.methods)),
                   modifiers  = "" if len(modifiers) == 0 else "<<%s>>"%",".join(modifiers))

    def methods_iter(self, visibility = '+'):
        """Iterate over the methods
        """
        for uml_method in self.methods:
            if uml_method.visibility[0] == visibility:
                yield (uml_method)

    def toXML(self, root = None, reference = False):
        if reference:
            from nxUML.core.uml_datatype import UMLDataTypeStub

            xmlClass = UMLDataTypeStub(self.name, self.scope).toXML(root)
            xmlClass.set("hrefId", self.id)
        else:
            from lxml import etree

            modifiers  = self.modifiers

            if root is None:
                xmlClass = etree.Element("class")
            else: xmlClass = etree.SubElement(root, "class")
            xmlClass.text   = self.name
            xmlClass.set("utility", "yes" if self.is_utility else "no")
            if self.is_interface:
                xmlClass.set("interface", "yes")
            xmlModifs       = etree.SubElement(xmlClass, "modifiers")
            xmlModifs.text  = "" if len(modifiers) == 0 else ",".join(modifiers)

            if self.scope is not None:
                xmlClass.set("scope", self.scope.full_name)

            if len(self.location)>0:
                xmlClass.set("location", self.location)

            xmlAttribs      = etree.SubElement(xmlClass, "attributes")
            for attrib in self.attributes:
                xmlAttrib = attrib.toXML(xmlAttribs)

            xmlMethods      = etree.SubElement(xmlClass, "methods")
            for method in self.methods:
                xmlMethod = method.toXML(xmlMethods)

        return xmlClass

######################################################################
class UMLClassAttribute:
    def __init__(self, name, type, 
                 visibility, 
                 constant = False,
                 utility = False):
        self.name       = name
        self.type       = type
        self.visibility = visibility
        self._utility     = utility
        self.properties = []
        if constant: self.properties.append('readOnly') #friend, extern

    @property
    def is_utility(self):
        return self._utility

    def __str__(self):
        return " {utility}{self.visibility} {self.name}:{self.type}".\
            format(self=self, utility = 'u' if self._utility else ' ',)

    def toXML(self, root = None):
        from lxml import etree
        if root is None:
            createElem = lambda root, name: etree.Element(name)
        else: createElem = etree.SubElement

        xmlAttrib = createElem(root, "attribute",
                               visibility = self.visibility,)
        if self.is_utility:
            xmlAttrib.set("utility", "yes")
        if len(self.properties) > 0:
            xmlAttrib.set("properties", "{%s}"%",".join(self.properties))

        # @TODO move it to uml_diagram
        if self.__dict__.has_key('unfolding_level'):
            xmlAttrib.set('unfolding-level', str(self.unfolding_level))

        xmlAttrib.text  = self.name
        xmlType         = self.type.toXML(xmlAttrib)
        return xmlAttrib

######################################################################
class UMLClassMethod:
    def __init__(self, name, 
                 rtnType, parameters,
                 visibility,
                 abstract   = False,
                 utility    = False,
                 properties = []):
        self.name       = str(name)
        self.rtnType    = rtnType
        self.parameters = parameters
        self.visibility = visibility

        self.properties = properties

        self._abstract = abstract
        self._utility  = utility

    @property
    def is_constructor(self):
        return self.name == "<<create>>" 

    @property
    def is_destructor(self):
        return self.name == "<<destroy>>" 

    @property
    def is_abstract(self):
        return self._abstract

    @property
    def is_utility(self):
        return self._utility

    def __str__(self):
        return "{abstract}{utility}{self.visibility}{self.name}(){rtnType}{properties}".\
            format(self=self, 
                   abstract = 'a' if self._abstract else ' ',
                   utility  = 'u' if self._utility else ' ',
                   properties= "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),
                   rtnType  = "" if self.rtnType is None else ":%s" % self.rtnType)

    def toXML(self, root = None):
        from lxml import etree
        if root is None:
            createElem = lambda root, name: etree.Element(name)
        else: createElem = etree.SubElement

        xmlMethod = createElem(root, "method",
                               visibility = self.visibility,)
        if self.is_utility:
            xmlMethod.set("utility", "yes")
        if self.is_abstract:
            xmlMethod.set("abstract", "yes")

        xmlMethod.text  = self.name

        if len(self.properties) > 0:
            xmlMethod.set("properties", "{%s}"%",".join(self.properties))

        xmlRetType      = etree.SubElement(xmlMethod, 'datatype')
        xmlRetType.text = self.rtnType

        xmlRetType      = etree.SubElement(xmlMethod, 'parameters')
        xmlRetType.text = self.rtnType

        # xmlParams       = etree.SubElement(xmlMethod, 'parameters')
        for paramId, parameter in zip(xrange(len(self.parameters)), self.parameters):
            paramName, paramType = parameter
            xmlParam      = etree.SubElement(xmlMethod, #xmlParams, 
                                             'parameter')
            xmlParam.set('id', str(paramId))
            xmlParamType  = etree.SubElement(xmlParam, 'datatype')
            xmlParam.text = paramName
            xmlParamType.text = paramType

        # if self.rtnType is not None:
        #     xmlRetType      = self.rtnType.toXML(xmlMethod)
        return xmlMethod

######################################################################
class UMLInterface(object):
    def __init__(self, name, 
                 scope    = None,
                 stereotypes = [],):
        # Extract data
        self.name     = str(name)
        self.scope    = scope
        self.stereotypes = stereotypes

    @property
    def id(self):
        return self.name

    def __str__(self):
        return r'{stereotypes}{self.scope}.{self.name}'.\
            format(self=self,
                   stereotypes = "<<%s>>"%",".join(self.stereotypes),)
