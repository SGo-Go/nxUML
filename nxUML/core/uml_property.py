#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_property.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

# from nxUML.core.uml_class_primitives    import UMLRedefinableElement, IUMLElement
# from nxUML.core.uml_modifier            import UMLModifierStack
from nxUML.core.uml_feature             import UMLStructuralFeature

############################################################
class UMLProperty(UMLStructuralFeature): 
    """A property is a structural feature which could represent
    * an attribute of a classifier, or
    * a member end of association, or
    * a part of a structured classifier.
    """
    pass

############################################################
class UMLMetaproperty(UMLProperty):
    """Tag definition (or metaproperty) is a properties of a stereotype
    """
    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object
        """
        return "metaproperty"

######################################################################
class UMLClassAttribute(UMLProperty):
    """A property owned by a classifier
    """
    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object
        """
        return "attribute"
