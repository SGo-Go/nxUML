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
                 detalization_level   = 0,
                 detalization_levels  = {},
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
            self.add_clases(uml_pool, cls_list,
                            detalization_level = detalization_level,
                            detalization_levels= detalization_levels,
                            with_generalizations = with_generalizations,
                            with_associations    = with_associations,
                            auto_aggregation     = auto_aggregation,)

    def add_clases(self, uml_pool, classes, 
                   detalization_level = 0,
                   detalization_levels= {},
                   with_generalizations = True,
                   with_associations    = False,
                   auto_aggregation     = False):
        """
        @param level       detalization level
        |     level     | Description                   |
        |-----------------------------------------------|
        |       0       | hide class                    |
        |       1       | details suppressed            |
        |       2       | analysis level details        |
        |       3       | implementation level details  |
        |       4       | maximum details               |
        @return dictionary with node settings for graphviz
        """
        
        for uml_class in classes:
            uml_class = uml_pool.Class[uml_class]
            self.add_class(uml_class, detalization_levels.get(uml_class.id, detalization_level))

        if with_generalizations and uml_pool:
            for uml_relationship in uml_pool.generalizations_iter():
                self.add_relationship(uml_relationship)

        if with_associations: pass

        if auto_aggregation:
            self.extract_aggregations()
        self._relationships = []

    def extract_aggregations(self):
        import sets
        classes = sets.Set(self._classes.keys())
        for uml_class in self._classes.values():
            for attrib in uml_class.attributes:
                if attrib.type.name in classes:
                    aggr = UMLAggregation(uml_class, 
                                          self._classes[attrib.type.name], attrib)
                    attrib.unfolding_level = 4
                    self.add_relationship(aggr)

    def add_class(self, uml_class, detalization_level = None):
        self._classes[uml_class.id] = uml_class
        self.add_node(uml_class.id)
        if detalization_level is not None:
            uml_class.detalization_level = detalization_level

    def add_relationship(self, uml_relationship, forced = False):
        source, dest = uml_relationship.source.id, uml_relationship.destination.id
        if not self.has_node(source) :
            if forced: self.add_node(source)
            else: return
        if not self.has_node(dest) :
            if forced: self.add_node(dest)
            else: return

        self.add_edge(source, dest, data = uml_relationship)

    # def __str__(self):
    #     return ""
    # self._relationships.append(uml_relationship)

    def toXML(self, root = None):
        from lxml import etree
        from itertools import izip

        def expotXMLattributes(node, uml_obj, attribs):
            for attr in attribs:
                if uml_obj.__dict__.has_key(attr):
                    node.set(attr.replace('_', '-'), str(uml_obj.__dict__[attr]))
                    # if attr == 'unfolding_level':
                    #     print uml_obj.name, uml_obj.unfolding_level, node.text

        if root is None:
            xmlDiag   = etree.Element("diagram")
        else: xmlDiag = etree.SubElement(root, "diagram")
        xmlDiag.set('type', 'class')
        xmlDiag.set('name', self.name)

        xmlClasses = etree.SubElement(xmlDiag, "classes")
        for class_name in self:
            uml_class = self._classes[class_name]
            xmlClass  = uml_class.toXML(xmlClasses)

            if uml_class.__dict__.has_key('detalization_level'):
                #print uml_class.id, uml_class.detalization_level
                xmlClass.set('detalization-level', str(uml_class.detalization_level))
            else:
                xmlClass.set('detalization-level', str(0))

            expotXMLattributes(xmlClass, uml_class, ('fillcolor', 'framecolor'))

            # for xmlAttrib, uml_attrib in izip(xmlClass.xpath('//class/attributes/*'), uml_class.attributes):
            #     expotXMLattributes(xmlAttrib, uml_attrib, ('unfolding_level',))

            # for method in uml_class.methods:
            #     if method.is_constructor or method.is_destructor:
            #         xmlMethod.set('unfolding_level', '2')
                
        return xmlDiag

