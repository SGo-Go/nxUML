#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       nxUML
(c) copyright 2014
######################################################################
@file         uml_class_diag.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
######################################################################

from networkx import MultiDiGraph
from nxUML.core import *

class UMLClassDiagram(MultiDiGraph):
    """Classes diagram representation in the form of networkx.MultiDiGraph
    for further analysis and visualization as needed
    """
    def __init__(self, name ='', 
                 uml_pool = None,
                 classes  = None, 
                 level    = 3,
                 levels   = {},
                 with_generalizations = True,
                 with_associations    = False,
                 auto_aggregation     = False,
                 # max_label = 4, name2URL = None,
                 data=None, #file=None,
                 **attr):
        """Constructor 
        """
        self._classes       = {}
        self._relationships = []

        super(UMLClassDiagram, self).__init__(data=data,name=name,**attr)

        if uml_pool is None: 
            if classes is not None: 
                self._classes = {cls:UMLType(cls) for cls in classes}
        else:
            if classes is None: 
                cls_list = uml_pool.Class.keys()
            else:
                cls_list = classes
            self.add_clases(uml_pool, cls_list)


    def add_clases(self, uml_pool, classes, 
                   level        = 3,
                   levels       = {},
                   with_generalizations = True,
                   with_associations    = False,
                   auto_aggregation     = False):
        for uml_class in classes:
            self.add_class(uml_pool.Class[uml_class])

        if with_generalizations and uml_pool:
            for uml_relationship in uml_pool.generalizations_iter():
                self.add_relationship(uml_relationship)

        if with_associations: pass

        if auto_aggregation:
            self.extract_aggregations()
        self._relationships = []

    def extract_aggregations(self):
        pass

    def add_class(self, uml_class):
        self._classes[uml_class.id] = uml_class
        self.add_node(uml_class.id)

    def add_relationship(self, uml_relationship, forced = False):
        source, dest = uml_relationship.source.id, uml_relationship.destination.id
        if not self.has_node(source) :
            if forced: self.add_node(source)
            else: return
        if not self.has_node(dest) :
            if forced: self.add_node(dest)
            else: return

        self.add_edge(source, dest, data = uml_relationship)
        #self._relationships.append(uml_relationship)


    # def __str__(self):
    #     return ""
