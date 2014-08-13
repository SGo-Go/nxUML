#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
 Project       nxUML
 (c) copyright 2014
######################################################################
 @file         brownie_documenter.py
 @author       Sergiy Gogolenko
 
 Create XML schemes for UML pool objects for further XSL transform to 
 HTML pages
######################################################################
"""
from nxUML.core import UMLPool, UMLPoolDocumenter, UMLClassRelationsGraph #UMLClassDiagram, 
from nxUML.core import UMLPackage, UMLClassifier #UMLClass, 
from brownie_uml import * #UMLBrownieUsage, UMLBrownieRealization, UMLBrownieInterface, UMLBrownieCall,UMLBrownieNotification

class BrowniePoolDocumenter(UMLPoolDocumenter):
    def source2XML(self, headerId):
        from lxml import etree
        uml_header = self.pool.deployment.source(headerId)

        xmlSource = etree.Element('source')
        xmlSource.set('id', uml_header.id)
        xmlSource.set('name', uml_header.name)
        xmlSource.set('ext', uml_header.ext)
        xmlSource.set('folder', uml_header.folder)

        includes_list = self.pool.deployment.sources.successors(uml_header.id)
        xmlIncludes = etree.SubElement(xmlSource, 'includes')
        if len(includes_list) > 0:
            for header_id in includes_list:
                uml_include = self.pool.deployment.source(header_id)
                xmlInclude = etree.SubElement(xmlIncludes, 'include')
                xmlInclude.set('id', uml_include.id)
                xmlInclude.set('name', uml_include.name)
                xmlInclude.set('ext', uml_include.ext)
                xmlInclude.set('folder', uml_include.folder)

        xmlClasses = etree.SubElement(xmlSource, 'classes')
        for name in uml_header.classes:
            uml_class = self.pool.Class[name]
            xmlClass = etree.SubElement(xmlIncludes, 'include')
            xmlClass.set('id', uml_class.id)
            xmlClass.set('name', uml_class.name)
            xmlClass.set('scope', uml_class.scope)
        return xmlSource

    def class2XML(self, uml_class):
        from lxml import etree

        classId = uml_class.id
        xmlClass  = uml_class.toXML()

        if isinstance(uml_class.scope, UMLPackage):
            xmlScope = uml_class.scope.toXML(xmlClass, scope = True)

        # for rel in self.inheritances.relationships_iter(uml_class):
        #     print rel

        # Walk through inheritance tree to find out whether class supports Brownie interfaces
        stereo_dict = dict([(x,None) for x in ('ServiceCallable', 'LocalCallable', 'LocalCallback')])
        for parent in uml_class.parents_dfs():
            if isinstance(parent, UMLClassifier):
                for stereotype in parent.modifiers:
                    if stereotype in stereo_dict.keys():
                        stereo_dict[stereotype] = parent

        xmlRelationships = etree.SubElement(xmlClass, 'relationships')
        xmlBrownieRelationships = etree.SubElement(xmlRelationships, 'brownie')
        for stereotype, classProvider in stereo_dict.items():
            xmlBrownieItem = etree.SubElement(xmlBrownieRelationships, 'relationship', type = stereotype)
            xmlSource = uml_class.toXML(xmlBrownieItem, reference = True)
            if stereo_dict[stereotype]:
                xmlDest   = stereo_dict[stereotype].toXML(xmlBrownieItem, reference = True)

        # Iterate over all relationships
        for uml_relationship in self.inheritances.relationships_iter(uml_class):
            xmlLink = uml_relationship.toXML(xmlRelationships)
            xmlLink.attrib['direction'] = 'in' if uml_relationship.destination.id == classId else 'out'
            if isinstance(uml_relationship, UMLBrownieUsage):
                xmlRemotes = etree.SubElement(xmlLink, 'remotes')
                if isinstance(uml_relationship.interface, UMLBrownieInterface):
                    for uml_realization in self.inheritances.in_relationships_iter(uml_relationship.interface):
                        if isinstance(uml_realization, UMLBrownieRealization):
                            uml_realization.classifier.toXML(xmlRemotes, reference=True)
                    # print(etree.tostring(xmlLink, pretty_print=True))

            elif isinstance(uml_relationship, UMLBrownieRealization):
                xmlRemotes = etree.SubElement(xmlLink, 'remotes')
                if isinstance(uml_relationship.interface, UMLBrownieInterface):
                    for uml_realization in self.inheritances.in_relationships_iter(uml_relationship.interface):
                        if isinstance(uml_realization, UMLBrownieUsage):
                            uml_realization.classifier.toXML(xmlRemotes, reference=True)
                    # print(etree.tostring(xmlLink, pretty_print=True))


        xmlInheritances = etree.SubElement(xmlRelationships, 'inheritances')
        for baseId, ownId, data in self.inheritances.out_edges_iter(uml_class.id, data=True):
            xmlLink = data['data'].toXML(xmlInheritances)
            xmlLink.set('direction', 'base')
            # print(etree.tostring(xmlLink, pretty_print=True))

        for ownId, baseId, data in self.inheritances.in_edges_iter(uml_class.id, data=True):
            xmlLink = data['data'].toXML(xmlInheritances)
            xmlLink.set('direction', 'derived')

        #subclasses      = uml_class.subclasses

        if classId in self.aggregations:
            xmlAggregations = etree.SubElement(xmlRelationships, 'aggregations')
            for cls_whole, cls_part, data in self.aggregations.in_edges_iter(uml_class.id, data=True):
                uml_class_whole = self.pool.Class[cls_whole]

                xmlLink = data['data'].toXML(xmlAggregations)
                xmlLink.set('direction', 'part')
            # for attrib in uml_class_whole.attributes:
            #     if attrib.name == data['data'].role and attrib.type.name == uml_class.name:
            #         # if attrib:
            #         xmlAttrib = attrib.toXML(xmlAggregations)
            #         xmlAttrib.set('owner', uml_class_whole.id)
            #         xmlAttrib.set('owner-name', uml_class_whole.name)
            #         xmlAttrib.set('owner-scope', str(uml_class_whole.scope))
                
        # xmlBrownie = etree.SubElement(xmlClass, 'interfaces')
        # xmlBrownieIn  = etree.SubElement(xmlBrownie, 'in')

        # xmlLink = data['data'].toXML(xmlInheritances)
        # xmlLink.set('direction', 'base')
        # xmlBrownieOut = etree.SubElement(xmlBrownie, 'out')

        # for ifaceId in uml_class.usages:
        #     [cls_provide, name] = ifaceId[3:].split('.')
        #     item_type = 'call' if ifaceId[1] == 'c' else 'notification'
        #     xmlBrownieItem = etree.SubElement(xmlBrownieIn, 'interface', name = name, type = item_type)
        #     xmlBrownieItem.set('owner-name', cls_provide)

        # for cls_require, cls_provide, data in self.ifaces.edges_iter(uml_class.id, data=True):
        #     if data.has_key('iface'):
        #         ifaceId = data['iface']
        #         [clsProvide, name] = ifaceId[3:].split('.')
        #         item_type = 'call' if ifaceId[1] == 'c' else 'notification'

        #         xmlBrownieItem = etree.SubElement(xmlBrownieOut, 'interface', name = name, type = item_type)
        #         xmlBrownieItem.set('owner-name', '' if cls_provide is None else cls_provide)
        return xmlClass

