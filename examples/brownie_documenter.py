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
from brownie_parser import UMLBrownieCall,UMLBrownieNotification
from nxUML.core import UMLPool, UMLPoolDocumenter, UMLClassDiagram, UMLClassRelationsGraph
from nxUML.core import UMLPackage, UMLClass

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


    def generalization2XML(self, root, tag, class_list):
        for classId in class_list:
            uml_class = self.pool.Class[classId]
            xmlItem = etree.SubElement(root, tag)
            xmlItem.set('name', uml_class.name)
            xmlItem.set('scope', uml_class.scope)
        return root

    def class2XML(self, classId):
        from lxml import etree

        uml_class = self.pool.Class[classId]
        xmlClass  = uml_class.toXML()

        if isinstance(uml_class.scope, UMLPackage):
            xmlScope = uml_class.scope.toXML(xmlClass, scope = True)

        # if len(self.location)>0:
        #     xmlClass.set("location", self.location)

        # Walk through inheritance tree to find out whether class supports Brownie interface
        stereo_dict = dict([(x,None) for x in ('ServiceCallable', 'LocalCallable', 'LocalCallback')])
        for className in self.inheritances.predecessors(classId) + [classId]:
            if className in self.pool:
                stereotypes = self.pool.Class[className].modifiers
                for stereotype in stereotypes:
                    if stereotype in stereo_dict.keys():
                        stereo_dict[stereotype] = self.pool.Class[className]

        xmlRelationships = etree.SubElement(xmlClass, 'relationships')
        xmlBrownieRelationships = etree.SubElement(xmlRelationships, 'brownie')
        for stereotype, classProvider in stereo_dict.items():
            #uml_class_ = self.pool.Class[cls_whole]
            xmlBrownieItem = etree.SubElement(xmlBrownieRelationships, 'relationship', type = stereotype)
            xmlSource = uml_class.toXML(xmlBrownieItem, reference = True)
            if stereo_dict[stereotype]:
                xmlDest   = stereo_dict[stereotype].toXML(xmlBrownieItem, reference = True)

        
        xmlInheritances = etree.SubElement(xmlRelationships, 'inheritances')
        for baseId, ownId, data in self.inheritances.in_edges_iter(uml_class.id, data=True):
            # uml_base_type = data['data'].parent #self.pool.Class[baseId]
            # xmlLink = etree.SubElement(xmlInheritances, 'link', type = 'base')
            # xmlLink.set('visibility', data['data'].visibility)
            # xmlLink.set('owner', baseId)
            # xmlLink.set('owner', uml_base_type.id)
            # xmlLink.set('owner-name', uml_base_type.name)
            # xmlLink.set('owner-scope', str(uml_base_type.scope))
            xmlLink = data['data'].toXML(xmlInheritances)
            xmlLink.set('direction', 'base')
            # print(etree.tostring(xmlLink, pretty_print=True))


        for ownId, baseId, data in self.inheritances.out_edges_iter(uml_class.id, data=True):
            # uml_base_type = data['data'].child #self.pool.Class[baseId]
            # xmlLink = etree.SubElement(xmlInheritances, 'link', type = 'derived')
            # xmlLink.set('visibility', data['data'].visibility)
            # xmlLink.set('owner', baseId)
            # xmlLink.set('owner', uml_base_type.id)
            # xmlLink.set('owner-name', uml_base_type.name)
            # xmlLink.set('owner-scope', str(uml_base_type.scope))
            xmlLink = data['data'].toXML(xmlInheritances)
            xmlLink.set('direction', 'derived')

        #subclasses      = uml_class.subclasses

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

        xmlBrownie = etree.SubElement(xmlClass, 'interfaces')
        xmlBrownieIn  = etree.SubElement(xmlBrownie, 'in')
        xmlBrownieOut = etree.SubElement(xmlBrownie, 'out')

        for ifaceId in uml_class.usages:
            [cls_provide, name] = ifaceId[3:].split('.')
            item_type = 'call' if ifaceId[1] == 'c' else 'notification'
            xmlBrownieItem = etree.SubElement(xmlBrownieIn, 'interface', name = name, type = item_type)
            xmlBrownieItem.set('owner-name', cls_provide)

        for cls_require, cls_provide, data in self.ifaces.edges_iter(uml_class.id, data=True):
            if data.has_key('iface'):
                ifaceId = data['iface']
                [clsProvide, name] = ifaceId[3:].split('.')
                item_type = 'call' if ifaceId[1] == 'c' else 'notification'

                xmlBrownieItem = etree.SubElement(xmlBrownieOut, 'interface', name = name, type = item_type)
                xmlBrownieItem.set('owner-name', '' if cls_provide is None else cls_provide)
        return xmlClass

