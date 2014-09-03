#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
 Project       nxUML
 (c) copyright 2014 All Right Reserved
######################################################################
 @file          brownie_documenter.py
 @author        Sergiy Gogolenko
 @email         sergiy.gogolenko@gmail.com
 @license       GPL
 
 Create XML schemes for UML pool objects for further XSL transform to 
 HTML pages
######################################################################
"""
from nxUML.core import UMLPool, UMLPoolDocumenter, UMLClassRelationsGraph #UMLClassDiagram, 
from nxUML.core import UMLNamespace, UMLPackage, UMLClassifier #UMLClass, 
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


    def packageable2XML(self, uml_packageable):
        xmlPackageable  = uml_packageable.toXML(reference = False)
        
        scopeParts = []
        scope = uml_packageable
        while isinstance(scope.scope, UMLNamespace) and not scope.isRoot:
            scope = scope.scope
            if not scope.isRoot:
                scopeParts.append(scope)
        if len(scopeParts) > 0:
            from lxml import etree
            xmlScope = etree.SubElement(xmlPackageable, "scope")
            while len(scopeParts) > 0: 
                scope = scopeParts.pop()
                xmlScopePart = scope.toXML(xmlScope, reference = True)
        return xmlPackageable

    def package2XML(self, uml_package):
        return self.packageable2XML(uml_package)

    def interface2XML(self, uml_interface):
        xmlIface = self.packageable2XML(uml_interface)
        xmlRelationships = self.relationships2XML(uml_interface, xmlIface)
        return xmlIface

    def relationships2XML(self, uml_element, xmlRoot):
        from lxml import etree
        elementId = uml_element.id
        xmlRelationships = etree.SubElement(xmlRoot, 'relationships')

        # Iterate over all relationships
        for uml_relationship in self.inheritances.relationships_iter(uml_element):
            xmlLink = uml_relationship.toXML(xmlRelationships)
            xmlLink.attrib['direction'] = 'in' if uml_relationship.destination.id == elementId else 'out'
        return xmlRelationships

    def class2XML(self, uml_class):
        from lxml import etree

        # classId = uml_class.id
        xmlClass  = self.packageable2XML(uml_class)

        # Fill up relationships section
        xmlRelationships = self.relationships2XML(uml_class, xmlClass)
        
        # Walk through inheritance tree to find out whether class supports Brownie interfaces
        stereo_dict = dict([(x,None) for x in ('ServiceCallable', 'LocalCallable', 'LocalCallback')])
        for parent in uml_class.parents_dfs():
            if isinstance(parent, UMLClassifier):
                for stereotype in parent.modifiers:
                    if stereotype in stereo_dict.keys():
                        stereo_dict[stereotype] = parent

        xmlBrownieRelationships = etree.SubElement(xmlRelationships, 'brownie')
        for stereotype, classProvider in stereo_dict.items():
            xmlBrownieItem = etree.SubElement(xmlBrownieRelationships, 'relationship', type = stereotype)
            xmlSource = uml_class.toXML(xmlBrownieItem, reference = True)
            if stereo_dict[stereotype]:
                xmlDest   = stereo_dict[stereotype].toXML(xmlBrownieItem, reference = True)

            # if isinstance(uml_relationship, UMLBrownieUsage):
            #     xmlRemotes = etree.SubElement(xmlLink, 'remotes')
            #     if isinstance(uml_relationship.interface, UMLBrownieInterface):
            #         for uml_realization in self.inheritances.in_relationships_iter(uml_relationship.interface):
            #             if isinstance(uml_realization, UMLBrownieRealization):
            #                 uml_realization.classifier.toXML(xmlRemotes, reference=True)
            #         # print(etree.tostring(xmlLink, pretty_print=True))

            # elif isinstance(uml_relationship, UMLBrownieRealization):
            #     xmlRemotes = etree.SubElement(xmlLink, 'remotes')
            #     if isinstance(uml_relationship.interface, UMLBrownieInterface):
            #         for uml_realization in self.inheritances.in_relationships_iter(uml_relationship.interface):
            #             if isinstance(uml_realization, UMLBrownieUsage):
            #                 uml_realization.classifier.toXML(xmlRemotes, reference=True)
            #         # print(etree.tostring(xmlLink, pretty_print=True))


        # if classId in self.aggregations:
        #     xmlAggregations = etree.SubElement(xmlRelationships, 'aggregations')
        #     for cls_whole, cls_part, data in self.aggregations.in_edges_iter(uml_class.id, data=True):
        #         uml_class_whole = self.pool.Class[cls_whole]

        #         xmlLink = data['data'].toXML(xmlAggregations)
        #         xmlLink.set('direction', 'part')
            # for attrib in uml_class_whole.attributes:
            #     if attrib.name == data['data'].role and attrib.type.name == uml_class.name:
            #         # if attrib:
            #         xmlAttrib = attrib.toXML(xmlAggregations)
            #         xmlAttrib.set('owner', uml_class_whole.id)
            #         xmlAttrib.set('owner-name', uml_class_whole.name)
            #         xmlAttrib.set('owner-scope', str(uml_class_whole.scope))
                
        return xmlClass

