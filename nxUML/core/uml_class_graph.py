#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       nxUML
(c) copyright 2014
######################################################################
@file         uml_class_graph.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
######################################################################

from networkx import MultiDiGraph
from nxUML.core import *
from brownie_uml import *
# UMLClassifier

class UMLClassRelationsGraph(MultiDiGraph):
    """Classes diagram representation in the form of networkx.MultiDiGraph
    for further analysis and visualization as needed
    """
    def __init__(self, name ='', 
                 uml_pool = None, 
                 classes  = None, 
                 # element_types = 
                 forced_relationships = False,
                 data=None,
                 **attr):
        """Constructor 
        """
        self._classes       = {}
        self._relationships = []

        super(UMLClassRelationsGraph, self).__init__(data=data,name=name,**attr)

        if uml_pool is None: 
            if classes is not None: 
                self._classes = {cls:UMLType(cls) for cls in classes}
        else:
            if classes is None: 
                cls_list = uml_pool.Class.keys()
            else:
                cls_list = classes

            # self.add_clases(uml_pool, cls_list,
            #                 with_generalizations = with_generalizations,
            #                 with_generalizations      = with_generalizations,
            #                 group_generalizations     = group_generalizations,
            #                 with_associations    = with_associations,
            #                 auto_aggregation     = auto_aggregation,
            #                 forced_relationships = forced_relationships)

    def import_clases(self, uml_pool, classes, 
                      with_generalizations = False,
                      group_generalizations= False,
                      with_associations    = False,
                      auto_aggregation     = False,
                      forced_relationships = False,
                      ):

        for uml_class in classes:
            uml_class = uml_pool.Class[uml_class]
            self.add_class(uml_class)

        if with_generalizations and uml_pool:
            self.import_generalizations(uml_pool, forced_relationships)
        if with_associations and uml_pool:
            self.import_associations(uml_pool, forced_relationships)
        if with_generalizations and uml_pool:
            self.import_generalizations(uml_pool, forced_relationships)
        if auto_aggregation:
            self.import_aggregations()
        return self

    def import_relationships(self, uml_pool, relationship_types = None, forced = True):
        for uml_relationship in uml_pool.relationships_iter(): #(relationship_types = relationship_types):
            self.add_relationship(uml_relationship, forced)
        return self

    def import_generalizations(self, uml_pool, forced = True):
        for uml_relationship in uml_pool.generalizations_iter():
            self.add_relationship(uml_relationship, forced)

    def import_associations(self, uml_pool, forced = True):
        pass
    
    def import_aggregations(self):
        import sets
        classes = sets.Set(self._classes.keys())
        for uml_class in self._classes.values():
            for attrib in uml_class.attributes:
                if attrib.type.base.id in classes:
                    aggr = UMLAggregation(uml_class, self._classes[attrib.type.base.id], attrib)
                    attrib.unfolding_level = 4
                    self.add_relationship(aggr)

    def import_usages(self, uml_pool, forced = True):
        for uml_class in self.classes_iter(root):
            for uml_relationship in uml_class.relationships_iter():
                if   isinstance(uml_relationship, UMLInterfaceRealization):
                    self.add_relationship(uml_relationship, forced)
                elif isinstance(uml_relationship, UMLInterfaceUsage):
                    self.add_relationship(uml_relationship, forced)

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

    def relationships_iter(self, uml_class):
        if isinstance(uml_class, str):
            classId = uml_class
        elif isinstance(uml_class, UMLClassifier):
            classId = uml_class.id
        else: return 
        for classIdFrom, classIdTo, data in self.in_edges_iter(classId, data=True):
            yield(data['data'])
        for classIdFrom, classIdTo, data in self.out_edges_iter(classId, data=True):
            yield(data['data'])

    def in_relationships_iter(self, uml_class):
        if isinstance(uml_class, str):
            classId = uml_class
        elif isinstance(uml_class, UMLClassifier):
            classId = uml_class.id
        else: return 
        # if uml_class.name == 'SetProfileDataCall':
        #     print self.in_degree(classId), self.out_degree(classId), classId
        for classIdFrom, classIdTo, data in self.in_edges_iter(classId, data=True):
            yield(data['data'])

    def out_relationships_iter(self, uml_class):
        if isinstance(uml_class, str):
            classId = uml_class
        elif isinstance(uml_class, UMLClassifier):
            classId = uml_class.id
        else: return 
        for classIdFrom, classIdTo, data in self.out_edges_iter(classId, data=True):
            yield(data['data'])

