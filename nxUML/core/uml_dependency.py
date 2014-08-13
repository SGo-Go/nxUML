#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_dependency.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.

Implementation partially follows:
http://www.uml-diagrams.org/dependency.html
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

######################################################################
# Relationships
######################################################################

from nxUML.core.uml_class_relationships import UMLBinaryRelationship

######################################################################
class  UMLDependency(UMLBinaryRelationship):
    """ @brief Dependency (supplier-client relationship) class.

    A directed relationship which is used to show that 
    some UML element or a set of elements requires, needs or depends on 
    other model elements for specification or implementation.
    """
    def __repr__(self):
        return "{self.source.name}-->{self.destination.name}".format(self=self)

class UMLUsage(UMLDependency):
    """@brief Usage 

    A dependency in which one named element (client) requires another named element (supplier) 
    for its full definition or implementation
    """
    def __repr__(self):
        return "{self.source.name}<-<<use>>-{self.destination.name}".format(self=self)

    def toXML(self, root = None):
        xmlLink = super(UMLUsage, self).toXML(root)
        xmlLink.set('type', 'usage')
        return xmlLink

class UMLAbstraction(UMLDependency):
    """@brief Abstraction 

    A dependency relationship that relates two elements or sets of elements 
    representing the same concept but at different levels of abstraction or from different viewpoints. 
    """
    def __repr__(self):
        return "{self.source.name}<-<<abstraction>>-{self.destination.name}".format(self=self)

class UMLRealization(UMLAbstraction):
    """@brief Realization

    A specialized abstraction relationship between two sets of model elements, 
    one representing a specification (the supplier) 
    and the other represents an implementation of the latter.
    """
    def __repr__(self):
        return "{self.source.name}<-<<abstraction>>-{self.destination.name}".format(self=self)

    def toXML(self, root = None):
        xmlLink = super(UMLRealization, self).toXML(root)
        xmlLink.set('type', 'realization')
        return xmlLink


######################################################################
class UMLInterfaceUsage(UMLUsage):
    """ @brief Interface usage (required interface)

    Specifies services that a classifier needs in order to 
    perform its function and fulfill its own obligations to its clients.
    """
    def __init__(self, uml_classifier, uml_iface):
        super(UMLInterfaceUsage, self).__init__(uml_classifier, uml_iface)

    @property
    def classifier(self):
        return self.source

    @property
    def interface(self):
        return self.destination

    def __repr__(self):
        return "{self.classifier.name}-({self.interface.name}".format(self=self)


######################################################################
class UMLInterfaceRealization(UMLRealization):
    """ @brief Interface realization 

    A specialized realization relationship between a classifier and an interface. 
    This relationship signifies that the realizing classifier 
    conforms to the contract specified by the interface. 
    """
    def __init__(self, uml_classifier, uml_iface):
        super(UMLInterfaceRealization, self).__init__(uml_classifier, uml_iface)

    @property
    def classifier(self):
        return self.source

    @property
    def interface(self):
        return self.destination

    def __repr__(self):
        return "{self.classifier.name}-(){self.interface.name}".format(self=self)
