#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_feature.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import UMLRedefinableElement
from nxUML.core.uml_modifier            import UMLModifierStack

######################################################################
class UMLFeature(UMLRedefinableElement): 
    """Feature represents a structural or behavioral characteristic of 
    a classifier or of instances of classifiers. 
    """
    def __init__(self, name, utility = False):
        self.utility    = utility
        super(UMLFeature, self).__init__(name)


    @property
    def is_utility(self):
        """Synonym for `is_static`"""
        return self.utility

    @property
    def is_static(self):
        """Feature could be either non static feature or static feature.
        Non static feature characterizes individual instances of classifier.
        Static feature represents some characteristic of the classifier itself.
        """
        return self.utility

    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object 
        """
        raise NotImplementedError('{0} objects have no tag'.format(type(self)))

    def toXML(self, root = None):
        from lxml import etree
        if root is None:
            xmlFeature = etree.Element(self.tag)
        else: xmlFeature = etree.SubElement(root, self.tag)

        xmlFeature.text  = self.name
        if self.is_utility: xmlFeature.set("utility", "yes")

        return xmlFeature

############################################################
# Structural
############################################################
class UMLStructuralFeature(UMLFeature): 
    """A structural feature is a typed feature of a classifier 
    that specifies the structure of instances of the classifier, 
    it specifies that instances of the featuring classifier 
    have a slot whose value or values are of a specified type. 
    """
    def __init__(self, name, type, 
                 visibility, 
                 constant = False,
                 utility = False):
        self.visibility = visibility

        self.type       = type

        self.modifiers = UMLModifierStack()
        if constant: self.modifiers.append('readOnly') #friend, extern
        super(UMLStructuralFeature, self).__init__(name, utility)

    @property
    def isReadOnly(self):
        return 'readOnly' in self.modifiers

    def __repr__(self):
        return " {utility}{self.visibility} {self.name}:{self.type}".\
            format(self=self, utility = 'u' if self.utility else ' ',)

    def toXML(self, root = None):
        xmlFeature = super(UMLStructuralFeature, self).toXML(root)

        xmlFeature.set('visibility', self.visibility)
        xmlType = self.type.toXML(xmlFeature)

        if len(self.modifiers) > 0:
            xmlFeature.set("modifiers", str(self.modifiers))

        # # @TODO move it to uml_diagram
        # if self.__dict__.has_key('unfolding_level'):
        #     xmlAttrib.set('unfolding-level', str(self.unfolding_level))

        return xmlFeature

############################################################
# Behavioral
############################################################
class UMLBehavioralFeature(UMLFeature): 
    """A behavioral feature is a feature of a classifier 
    that specifies an aspect of the behavior of its instances.
    A behavioral feature specifies that an instance of a classifier 
    will respond to specific requests by invoking behavior.
    """
    def __init__(self, name, 
                 rtnType, parameters,
                 visibility,
                 utility    = False,
                 modifiers = UMLModifierStack()):
        self.visibility = visibility

        self.rtnType    = rtnType
        self.parameters = parameters

        self.modifiers = modifiers
        # if constant: self.modifiers.append('readOnly') #friend, extern
        super(UMLBehavioralFeature, self).__init__(name, utility)

    @property
    def isQuery(self):
        return 'query' in self.modifiers

    def toXML(self, root = None):
        xmlFeature = super(UMLBehavioralFeature, self).toXML(root)

        xmlFeature.set('visibility', self.visibility)

        if len(self.modifiers) > 0:
            xmlFeature.set("modifiers", str(self.modifiers))

        xmlRetType = self.rtnType.toXML(xmlFeature, reference = True)
        xmlParams  = self.parameters.toXML(xmlFeature)

        return xmlFeature
