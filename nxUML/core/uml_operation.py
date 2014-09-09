#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_operation.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import UMLRedefinableElement, IUMLElement

from nxUML.core.uml_modifier            import UMLModifierStack
from nxUML.core.uml_feature             import UMLBehavioralFeature

######################################################################
class UMLOperationParameter(UMLRedefinableElement): 
    """Parameter of an UML operation 
    """
    def __init__(self, name, type):
        self.type    = type
        super(UMLOperationParameter, self).__init__(name)

    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object 
        """
        return 'parameter'

    def __repr__(self):
        return '{self.name}:{self.type}'.format(self=self)

    def toXML(self, root = None):
        xmlParam = super(UMLOperationParameter, self).toXML(root = root, reference = False)
        self.type.toXML(xmlParam)
        return xmlParam

######################################################################
class UMLOperationParameterStack(list, IUMLElement): 
    """List of UML operation parameters 
    """
    def __init__(self, uml_params = []):
        super(UMLOperationParameterStack, self).__init__(uml_params)

    def add(self, name, type):
        self.append(UMLOperationParameter(name, type))

    def __repr__(self):
        return '({0})'.format(', '.join(map(str,self)))

    def toXML(self, root, reference = False):
        for paramId, parameter in zip(xrange(len(self)), self):
            xmlParam = parameter.toXML(root)
            # xmlParam.set('no', str(paramId))
        # return xmlParam

######################################################################
#
######################################################################
class UMLClassOperation(UMLBehavioralFeature):
    def __init__(self, name, 
                 rtnType, parameters,
                 visibility,
                 abstract   = False,
                 utility    = False,
                 errors     = None, 
                 modifiers = UMLModifierStack()):
        self.abstract = abstract
        super(UMLClassOperation, self).__init__(str(name), rtnType, parameters,
                                                visibility,
                                                utility    = utility,
                                                modifiers = modifiers)

    @property
    def is_constructor(self):
        return self.name == "<<create>>" 

    @property
    def is_destructor(self):
        return self.name == "<<destroy>>" 

    @property
    def is_abstract(self):
        return self.abstract

    def __repr__(self):
        return "{abstract}{utility}{self.visibility}{self.name}(){rtnType}{modifiers}".\
            format(self=self, 
                   abstract = 'a' if self.is_abstract else ' ',
                   utility  = 'u' if self.is_utility else ' ',
                   modifiers= str(self.modifiers),
                   rtnType  = str(self.rtnType))#"" if self.rtnType is None else ":%s" % self.rtnType)

    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object
        """
        return "operation"

    def toXML(self, root = None):
        xmlOperation = super(UMLClassOperation, self).toXML(root)

        if self.is_abstract:
            xmlOperation.set("abstract", "yes")

        # if self.rtnType is not None:
        #     xmlRetType      = self.rtnType.toXML(xmlOperation)
        return xmlOperation
