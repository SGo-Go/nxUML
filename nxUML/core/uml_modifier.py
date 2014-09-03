#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_modifier.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import IUMLElement

######################################################################
class UMLModifier(IUMLElement):
    """Optional modifiers of features"""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def toXML(self, root, reference = False):
        from lxml import etree
        xmlModif = etree.SubElement(root, "modifier")
        xmlModif.set('name', self.name)
        return xmlModif

class UMLRedefinesModifier(UMLModifier):
    """Redefines an inherited feature named feature-name"""
    def __init__(self, feature = None):
        self.feature = feature
        super(UMLRedefinesModifier, self).__init__(name)

    def __repr__(self):
        return 'redefines' + str(self.feature)

class UMLSubsetsModifier(UMLModifier):
    """A subset of the feature named feature-name"""
    def __init__(self, feature = None):
        self.feature = feature
        super(UMLSubsetsModifier, self).__init__(name)

    def __repr__(self):
        return 'subsets' + str(self.feature)

class UMLConstraint(UMLModifier):
    """A constraint that applies to the feature"""
    def __init__(self, constraint = None):
        self.constraint = constraint
        super(UMLSubsetsModifier, self).__init__('constraint')

    def __repr__(self):
        return self.constraint

######################################################################
class UMLModifierStack(list, IUMLElement):
    """List of UML modifiers"""
    # Standard modifiers of properties
    readOnly  = UMLModifier('readOnly') # read only (isReadOnly = true)
    seq       = UMLModifier('seq') # ordered bag (isUnique = false and isOrdered = true)
    union     = UMLModifier('union') # derived union of its subsets
    id        = UMLModifier('id') # part of the identifier for the class which owns the property

    # Standard modifiers of operations
    query     = UMLModifier('query') # operation does not change the state of the system

    # Common modifiers
    ordered   = UMLModifier('ordered') # ordered (isOrdered = true)
    unique    = UMLModifier('unique')  # multi-valued, no duplicates (isUnique = true)
    nonunique = UMLModifier('nonunique') # multi-valued, may have duplicates (isUnique = false)

    def __init__(self, uml_modif = []):
        super(UMLModifierStack,self).__init__(uml_modif)

    def add(self, name):
        if isinstance(name, UMLModifier):
            self.append(name)
        else:
            self.append(UMLModifier(name))

    def add_constraint(self, constraint):
        self.append(UMLConstraint(constraint))

    def __repr__(self):
        return "{%s}" % ','.join(map(str,self)) if len(self) > 0 else ''

    def toXML(self, root, reference = False):
        for multi in self:
            xmlMulti = multi.toXML(root)
