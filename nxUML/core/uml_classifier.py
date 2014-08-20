#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_classifier.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import UMLNamespace, UMLRedefinableElement
from nxUML.core.uml_class_relationships import UMLRelationship, UMLGeneralization

class UMLClassifier(UMLRedefinableElement, UMLNamespace):
    """An abstract metaclass which describes (classifies) set of instances having common features.
    The classifier is a type, templateable element, redefinable element, and namespace.
    """
    def __init__(self, name, scope, subclasses = None, **args):

        self.relationships = []
        super(UMLClassifier, self).__init__(name=name, scope=scope, **args)

    def add_relationship(self, uml_relationship):
        self.relationships.append(uml_relationship)

    # def add(self, uml_packageable_element):
    #     if isinstance(uml_packageable_element, UMLRelationship):
    #         self.add_relationship(uml_packageable_element)
    #     else:
    #         self.named_elements[uml_packageable_element.name] = uml_packageable_element

    def relationships_iter(self, type=None):
        for uml_relationship in self.relationships:
            if type is None or isinstance(uml_relationship, type):
                yield (uml_relationship)

    @property
    def generalizations(self):
        return self.relationships_iter(type=UMLGeneralization)

    def generalizations_iter(self):
        return self.relationships_iter(type=UMLGeneralization)

    def parents_dfs(self):
        """Iterate over parent classes (starting from the class itself) 
        in a depth-first order
        """
        parentsStack = [self]
        while len(parentsStack) > 0:
            parent = parentsStack.pop()
            if isinstance(parent, UMLClassifier):
                for generalization in parent.generalizations_iter():
                    if generalization.parent.id != generalization.child.id: 
                        parentsStack.append(generalization.parent)
            yield(parent)
