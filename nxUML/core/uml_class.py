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

from nxUML.core.uml_stereotype  import UMLStereotypeStack, UMLStereotype
from nxUML.core.uml_classifier  import UMLClassifier
# from nxUML.core.uml_operation import UMLClassOperation
# from nxUML.core.uml_property  import UMLClassAttribute

######################################################################
class UMLClass(UMLClassifier):
    """Unified (language independent) representation of class
    """
    def __init__(self, name, 
                 manifestation = None, 
                 scope  = None,
                 operations  = [],
                 attribs  = [],
                 stereotypes  = UMLStereotypeStack(),
                 subclasses = None,
                 parent   = None,):

        # Fill data
        self.manifestation = manifestation

        self.extra_stereotypes = stereotypes
        self.operations    = operations
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

    def add_operation(self, operation):
        self.operations.append(operation)

    def add_operations(self, operations):
        if not self.__dict__.has_key("operations") or self.operations is None:
            self.operations = operations
        else: self.operations.extend(operations)

    def add_realization(self, iface_id):
        self.realizations.append(iface_id)

    def add_usage(self, iface_id):
        self.usages.append(iface_id)

    @property
    def stereotypes(self):
        stereotypes  = UMLStereotypeStack(self.extra_stereotypes)
        # if self.is_interface: stereotypes.append('interface')
        if self.is_utility:   stereotypes.append(UMLStereotypeStack.utility.application())
        stereotypes.extend(self.extra_stereotypes)
        return stereotypes

    def has_stereotypes(self):
        if self.is_interface:    return True
        if self.is_utility:      return True
        if len(self.extra_stereotypes): return True
        return False

    def add_stereotype(self, stereotype):
        self.extra_stereotypes.append(stereotype)

    @property
    def is_interface(self):
        if len(self.attributes) > 0:
            return False
        for operation in self.operations:
            if not operation.is_destructor and not operation.is_abstract: 
                return False
        return True

    @property
    def is_utility(self):
        for attrib in self.attributes:
            if not attrib.is_utility: return False
        for operation in self.operations:
            if not operation.is_destructor and not operation.is_utility: return False
        
        return True

    def __str__(self):
        return "{line}\n{stereotypes:^40}\n[{self.scope}]{self.name}\n{line}\n{attributes}\n{line}\n{operations}\n{line}".\
            format(self=self, line= chr(196)*40, #unicode('\x80abc', errors='replace')*
                   attributes  = "\n".join(map(str,self.attributes)),
                   operations  = "\n".join(map(str,self.operations)),
                   stereotypes = str(self.stereotypes))

    def operations_iter(self, visibility = '+'):
        """Iterate over the operations
        """
        for uml_operation in self.operations:
            if uml_operation.visibility[0] == visibility:
                yield (uml_operation)
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
class UMLInterface(UMLClassifier): #pass
    @property
    def tag(self):
        """Specifies XML tag `interface' for the serialized instances of UML interfaces
        """
        return 'interface'

    def toXML(self, root = None, reference = False):
        xmlInterface = super(UMLInterface, self).toXML(root = root, reference = reference)
        if not reference: xmlInterface.set("interface", "yes")
        return xmlInterface
