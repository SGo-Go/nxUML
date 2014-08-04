#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_multiplicity.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import IUMLElement

######################################################################
class UMLMultiplicity(IUMLElement):
    star = float('inf')

    def __init__(self, multiplicity = None, 
                 pointer = False, reference = False):
        if   multiplicity is not None and multiplicity != 1:
            self._range = multiplicity
        elif pointer   : self.pointer   = True
        elif reference : self.reference = True
        super(UMLMultiplicity, self).__init__()

    @property
    def max(self):
        if hasattr(self._range, '__iter__'):
            return self._range[1]
        else: return self._range

    @property
    def min(self):
        if hasattr(self._range, '__iter__'):
            return self._range[0]
        else: return self._range

    @property
    def value(self):
        return self.max

    @property
    def reference(self):
        return self.value == 0

    @property
    def composite(self):
        return self.min == 1 #and self.max == 1

    @reference.setter
    def reference(self, is_ref = True):
        self._range = 0

    @property
    def pointer(self):
        return self.min == 0 and self.max == 1

    @pointer.setter
    def pointer(self, is_ptr = True):
        self._range = (0,1)

    def __repr__(self):
        m1 = self.min
        m2 = self.max
        if m2 == UMLMultiplicity.star: m2 = '*'
        if m1 == 0: 
            if   m2 ==  0 : return '&'
            elif m2 == '*': return '*'
        if m1 == m2: 
            return '' if m1 == 1 else m1
        else: return '{0}..{1}'.format(m1,m2)

    def toXML(self, root, reference = False):
        from lxml import etree
        xmlMulti = etree.SubElement(root, "multiplicity")

        if self.reference: xmlMulti.set('type', 'reference')
        elif self.pointer: xmlMulti.set('type',   'pointer')
        else: xmlMulti.set('type',   'arbitrary')

        xmlMulti.text = str(self)
        return xmlMulti

######################################################################
# @TODO Make transition UMLMultiplicity -> UMLQualifier
class UMLQualifier(IUMLElement):
    def __init__(self, bind, key = 'Id'):
        self.bind = bind
        self.key  = key

    @property
    def composite(self):
        return True

    def __repr__(self):
        return "*(<<bind>>{self.bind}<key={self.key}>)".format(self=self)
        # return "bind=<<{self.bind}>>, key={:self.key}".format(self=self)
        # return '*'

    def toXML(self, root, reference = False):
        from lxml import etree

        xmlMulti = etree.SubElement(root, "multiplicity")
        xmlMulti.set('type', 'quantifier')
        xmlMulti.set('bind', self.bind)
        xmlMulti.set('key',  str(self.key))

        xmlMulti.text = str(self)
        return xmlMulti

######################################################################
class UMLMultiplicityStack(list, IUMLElement):
    reference = UMLMultiplicity(reference = True)
    pointer   = UMLMultiplicity(pointer = True)

    def __init__(self, uml_multy = []):
        super(UMLMultiplicityStack,self).__init__(uml_multy)

    # def extend(self, uml_multi):
    #     self.append(uml_multi)

    def add_reference(self):
        self.append(UMLMultiplicityStack.reference)

    def add_pointer(self):
        self.append(UMLMultiplicityStack.pointer)

    def add_qualifier(self, bind, key = 'int'):
        self.append(UMLQualifier(bind, key))
        
    def __repr__(self):
        return ' '.join(map(str,self))
    # return "bind={bind}, key={key}".format(bind="<<%s>>" % ",".join(self.bind),
    #        key="%s"%",".join(map(lambda x: 'id:' + (x if type(x) is str else x.name), self.key)))

    def toXML(self, root, reference = False):
        for multi in self:
            xmlMulti = multi.toXML(root)
