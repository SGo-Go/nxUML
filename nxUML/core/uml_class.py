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

from nxUML.core.uml_class_primitives    import IUMLElement
from nxUML.core.uml_modifier            import UMLModifierStack

from nxUML.core.uml_classifier          import UMLClassifier
from nxUML.core.uml_feature             import UMLBehavioralFeature, UMLProperty

######################################################################
class UMLClass(UMLClassifier):
    """Unified (language independent) representation of class
    """
    def __init__(self, name, 
                 manifestation = None, 
                 scope  = None,
                 methods  = [],
                 attribs  = [],
                 modifiers  = [],
                 subclasses = None,
                 parent   = None,):

        # Fill data
        self.manifestation = manifestation

        self._modifiers = modifiers
        self.methods    = methods
        self.attributes = attribs

        # Fill dependencies 
        self.parent       = parent

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
        if not self.__dict__.has_key("operations") or self.methods is None:
            self.methods = methods
        else: self.methods.extend(methods)

    def add_realization(self, iface_id):
        self.realizations.append(iface_id)

    def add_usage(self, iface_id):
        self.usages.append(iface_id)

    @property
    def modifiers(self):
        modifiers  = []
        if self.is_interface: modifiers.append('interface')
        if self.is_utility:   modifiers.append('utility')
        modifiers.extend(self._modifiers)
        return modifiers

    def has_modifiers(self):
        if self.is_interface:    return True
        if self.is_utility:      return True
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
    @property
    def tag(self):
        """Specifies XML tag `class' for the serialized instances of UML classes
        """
        return 'class'

    def toXML(self, root = None, reference = False):
        xmlClass = super(UMLClass, self).toXML(root = root, reference = reference)
        if not reference:
            xmlClass.set("utility", "yes" if self.is_utility else "no")
            if self.is_interface: xmlClass.set("interface", "yes")
        return xmlClass

######################################################################

class UMLClassAttribute(UMLProperty):
    """A property owned by a classifier
    """
    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object
        """
        return "attribute"

######################################################################
class UMLClassMethod(UMLBehavioralFeature):
    def __init__(self, name, 
                 rtnType, parameters,
                 visibility,
                 abstract   = False,
                 utility    = False,
                 errors     = None, 
                 properties = UMLModifierStack()):
        self.abstract = abstract
        super(UMLClassMethod, self).__init__(str(name), rtnType, parameters,
                                             visibility,
                                             utility    = utility,
                                             properties = properties)

    @property
    def is_constructor(self):
        return self.name == "<<create>>" 

    @property
    def is_destructor(self):
        return self.name == "<<destroy>>" 

    @property
    def is_abstract(self):
        return self.abstract

    def __repr__(self):
        return "{abstract}{utility}{self.visibility}{self.name}(){rtnType}{properties}".\
            format(self=self, 
                   abstract = 'a' if self.is_abstract else ' ',
                   utility  = 'u' if self.is_utility else ' ',
                   properties= str(self.properties),
                   rtnType  = "" if self.rtnType is None else ":%s" % self.rtnType)

    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object
        """
        return "operation"

    def toXML(self, root = None):
        xmlMethod = super(UMLClassMethod, self).toXML(root)

        if self.is_abstract:
            xmlMethod.set("abstract", "yes")

        # if self.rtnType is not None:
        #     xmlRetType      = self.rtnType.toXML(xmlMethod)
        return xmlMethod

######################################################################
class UMLInterface(UMLClassifier): #pass
    @property
    def tag(self):
        """Specifies XML tag `class' for the serialized instances of UML classes
        """
        return 'interface'

    def toXML(self, root = None, reference = False):
        xmlInterface = super(UMLInterface, self).toXML(root = root, reference = reference)
        if not reference: xmlInterface.set("interface", "yes")
        return xmlInterface
