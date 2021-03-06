#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_class_reltioships.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

######################################################################
# Relationships
######################################################################

class UMLRelationship(object):
    def __init__(self): pass

    def toXML(self, root = None):
        from lxml import etree

        if root is None:
            xmlLink = etree.Element("relationship")
        else: xmlLink = etree.SubElement(root, "relationship")
        return xmlLink

class UMLBinaryRelationship(UMLRelationship):
    def __init__(self, source, destination):
        self.source      = source
        self.destination = destination

    def __str__(self):
        return "{self.source.name}->{self.destination.name}".format(self=self)

    def toXML(self, root = None):
        xmlLink = super(UMLBinaryRelationship, self).toXML(root)

        xmlSource = self.source.toXML(xmlLink, reference = True)
        xmlDest   = self.destination.toXML(xmlLink, reference = True)

        return xmlLink

class UMLNaryRelationship(UMLRelationship):
    def __init__(self, *classifiers):
        self.classifiers = classifiers

    def __str__(self):
        return "{{{0}}}".format(
            ','.join(map(lambda x: x.name, self.classifiers)))


######################################################################

class UMLBinaryAssociation(UMLBinaryRelationship):
    def __init__(self, classifier1, classifier2, order_reading = None):
        self.order_reading = order_reading
        super(UMLBinaryAssociation, self).__init__(classifier1, classifier2)

    def __str__(self):
        return "{self.source.name}-{order_reading}-{self.destination.name}".\
            format(self=self, 
                   order_reading = '' if order_reading == '' else \
                       '|{0}>'.format(order_reading))


class UMLNaryAssociation(UMLNaryRelationship):
    def __init__(self, classifiers, note = None):
        self.note = note
        super(UMLNaryRelationship, self).__init__(classifier1, classifier2)

    def __str__(self):
        return "[{self.note}]{out}".format(\
            self=self, out = super(UMLNaryAssociation, self).__str__())

######################################################################

class UMLDetalization(UMLBinaryRelationship):
    def __init__(self, multiplicity = '', modifiers = [], qualifier = None):
        self.multiplicity = multiplicity
        self.modifiers   = modifiers
        #self.qualifier    = qualifier

class UMLAggregation(UMLBinaryRelationship):
    def __init__(self, whole, part, attribute = None, visibility = '  '):
        if attribute is not None:
            self.visibility = attribute.visibility
            self.role = attribute.name

            self.multiplicity = attribute.type.multiplicity
            # self.composite = attribute.type.composite
            # self.qualifier = attribute.type.qualifier

            modifiers   = attribute.type.modifiers
            # if len(self.qualifier) > 0:
            #     multiplicity =  '*'
            #     if attribute.type.reference:
            #         modifiers = ['&'] + modifiers
            #     elif attribute.type.pointer:
            #         modifiers = ['*'] + modifiers
            # else:
            #     multiplicity = attribute.type.multiplicity
            # self.part_detalization = UMLDetalization(
            #     multiplicity = multiplicity, 
            #     #, qualifier = qualifier
            #     modifiers = modifiers)
        super(UMLAggregation, self).__init__(whole, part)

    @property
    def full_role(self):
        return "{self.visibility}{self.role}\n{self.qualifier}".format(self=self)

    @property
    def composite(self):
        return self.multiplicity.composite #len(self.multiplicity) == 0 or not(self.multiplicity[0].reference or self.multiplicity[0].pointer)

    @property
    def shared(self):
        return not self.composite

    @property
    def part(self):
        return self.destination

    @part.setter
    def part(self, part_class):
        self.destination = part_class

    @property
    def whole(self):
        return self.source

    @whole.setter
    def whole(self, whole_class):
        self.source = whole_class

    def __str__(self):
        return "{self.whole.name}<>-[{self.full_role}]-{self.destination.name}".format(self=self)

    def toXML(self, root = None):
        xmlLink = super(UMLAggregation, self).toXML(root)
        xmlLink.set('type', 'aggregation')
        xmlLink.set('visibility', self.visibility)
        xmlLink.set('role', self.role)

        for attrName, xmlType in zip(('whole', 'part'), xmlLink.findall('datatype')):
            xmlType.set(attrName, 'yes')

        return xmlLink

######################################################################

class UMLGeneralization(UMLBinaryRelationship):
    def __init__(self, child, parent, visibility = '  '):
        self.visibility = visibility
        super(UMLGeneralization, self).__init__(child, parent)

    @property
    def child(self):
        return self.source

    @child.setter
    def child(self, child_class):
        self.source = child_class

    @property
    def parent(self):
        return self.destination

    @parent.setter
    def parent(self, parent_class):
        self.destination = parent_class

    def __str__(self):
        return "{self.parent.name}<-[{self.visibility}]-{self.child.name}".format(self=self)

    def toXML(self, root = None):
        xmlLink = super(UMLGeneralization, self).toXML(root)
        xmlLink.set('type', 'generalization')
        xmlLink.set('visibility', self.visibility)

        for attrName, xmlType in zip(('patent', 'child'), xmlLink.findall('datatype')):
            xmlType.set(attrName, 'yes')

        return xmlLink
