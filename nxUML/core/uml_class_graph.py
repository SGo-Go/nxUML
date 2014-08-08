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

class UMLClassRelationsGraph(MultiDiGraph):
    """Classes diagram representation in the form of networkx.MultiDiGraph
    for further analysis and visualization as needed
    """
    def __init__(self, name ='', 
                 uml_pool = None,
                 classes  = None, 
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
            #                 with_interfaces      = with_interfaces,
            #                 group_interfaces     = group_interfaces,
            #                 with_associations    = with_associations,
            #                 auto_aggregation     = auto_aggregation,
            #                 forced_relationships = forced_relationships)

    def add_clases(self, uml_pool, classes, 
                   with_generalizations = False,
                   with_interfaces      = False,
                   group_interfaces     = False,
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
        if with_interfaces and uml_pool:
            self.import_interfaces(uml_pool, forced_relationships)
        if auto_aggregation:
            self.import_aggregations()

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
                    aggr = UMLAggregation(uml_class, 
                                          self._classes[attrib.type.base.id], attrib)
                    attrib.unfolding_level = 4
                    self.add_relationship(aggr)

    def import_interfaces(self, uml_pool, forced = True):
        from sets import Set

        ifaces_ids = Set()
        classes_ids = self.nodes()
        for classId in classes_ids:
            if classId in uml_pool.Class:
                uml_class = uml_pool.Class[classId]
                for iname in uml_class.usages:
                    self.add_edge(iname, uml_class.id)
                    ifaces_ids.add(iname)
                for iname in uml_class.realizations:
                    self.add_edge(uml_class.id, iname)
                    ifaces_ids.add(iname)
        self.disjoin_interfaces(ifaces_ids, forced = forced)
        
    def disjoin_interfaces(self, ifaces_ids, forced = True):
        for iname in ifaces_ids:
            source_ids = self.predecessors(iname)
            dest_ids   = self.successors(iname)
            self.remove_node(iname)
            if   len(source_ids) == 0 and len(dest_ids) > 0:
                if forced:
                    for dest_id in dest_ids:
                        self.add_edge(None, dest_id, iface = iname)
            elif len(source_ids) > 0 and len(dest_ids) == 0:
                if forced:
                    for source_id in source_ids:
                        self.add_edge(source_id, None, iface = iname)
            elif len(source_ids) > 0 and len(dest_ids) > 0:
                for source_id in source_ids:
                    for dest_id in dest_ids:
                        self.add_edge(source_id, dest_id, iface = iname)

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
