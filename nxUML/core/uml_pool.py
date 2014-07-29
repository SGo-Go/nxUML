#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_pool.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import UMLClass, UMLInterface, UMLSimpleDataType, UMLDataTypeDecorator
from nxUML.core.uml_class_relationships import *
from nxUML.core.uml_artifacts           import *
from nxUML.core.uml_class_diag          import UMLClassRelationsGraph

class UMLDeploymentPool(object):
    def __init__(self, name='', 
                 sources = None,
                 source_prefix = '',
                 **attr):
        if sources is None:
            self.sources = UMLSourceFilesGraph(source_prefix)
        else: self.sources = sources

    def source(self, sourceId):
        return self.sources.source[sourceId]

class UMLPool(object):
    """Pool of classes with relationships between them
    """
    def __init__(self, name='', 
                 deployment = None, 
                 deployment_class = UMLDeploymentPool, source_prefix = '',
                 **attr):
        """Constructor 
        """
        self.Class           = {}
        self.package         = {}
        self.Interface       = {}
        self._relationships  = []

        if deployment is None: 
            self.deployment = deployment_class(source_prefix = source_prefix)
        else: self.deployment = deployment

    def add_class(self, uml_class):
        self.Class[uml_class.id] = uml_class

    def add_package(self, uml_package):
        self.package[uml_package.id] = uml_package

    def add_interface(self, uml_iface):
        self.Interface[uml_iface.id] = uml_iface

    def add_file(self, uml_iface):
        self.Interface[uml_iface.id] = uml_iface

    def add_relationship(self, uml_relationship):
        self._relationships.append(uml_relationship)

    def __str__(self):
        """String representation of information about the pool.

        @return The list of the classes in the pool with count of relationship.
        """
        #return 'Pool of {nclasses} classes with {nrelations} relationships: {classes}'.
        return 'Pool of {nclasses} class(es) with {nrelations} relationship(s)'.\
            format(nrelations = len(self._relationships), 
                   nclasses = len(self.Class.keys()),
                   classes = ', '.join(self.Class.keys()))

    def __contains__(self, cls):
        """Check if the given name is a name of class from pool
        Use the expression 'cls in uml_pool'.
        
        @param cls name of class to check
        @return True if cls is a class from pool, False otherwise.
        """
        return self.Class.has_key(cls)

    def __len__(self):
        """Number of classes in pool.
        Use the expression `len(pool)`

        @return the number of classes.
        """
        return len(self.Class)

    def __iter__(self):
        """Iterate over the classes.
        """
        return iter(self.Class)

    def classes_iter(self, scope = ''):
        """Iterate over the classes from the given package.
        """
        for cls_name, uml_class in self.Classes.items():
            if len(scope) == 0:
                yield (uml_class)
            elif uml_class.scope == scope:
                yield (uml_class)

    def relationships_iter(self):
        return iter(self._relationships)

    def generalizations_iter(self, parents = None, childs = None):
        for relationship in self.relationships_iter():
            if isinstance(relationship, UMLGeneralization): 
                yield (relationship)

    def get(self, uml_relname, max_scope):
        scope = max_scope
        while isinstance(scope, UMLPackage) or isinstance(scope, UMLClass):
            item = scope.get(uml_relname)
            if item:    return item
            else:       scope = scope.scope
        return None

class UMLPoolDocumenter(object):
    """Pool of classes with relationships between them
    """
    def __init__(self, uml_pool, **attr):
        """Constructor 
        """
        self.pool = uml_pool
        self.inheritances = UMLClassRelationsGraph(uml_pool = uml_pool, 
                                                   with_generalizations = True,
                                                   with_interfaces = False,
                                                   auto_aggregation = False,
                                                   forced_relationships = True
                                                   )

        self.aggregations = UMLClassRelationsGraph(uml_pool = uml_pool, 
                                                   with_generalizations = False,
                                                   with_interfaces = False,
                                                   auto_aggregation = True,
                                                   forced_relationships = True
                                                   )

        self.ifaces = UMLClassRelationsGraph(uml_pool = uml_pool, 
                                             with_generalizations = False,
                                             with_interfaces = True,
                                             auto_aggregation = False,
                                             forced_relationships = True
                                             ).reverse()

    def class2XML(self, classId):
        uml_class = self.pool.Class[classId]
        xmlClass = uml_class.toXML(root = None)

    def class2XML(self, classId):
        uml_class = self.pool.Class[classId]
        xmlClass = uml_class.toXML(root = None)
