#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_pool.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

class UMLQualifier:
    def __init__(self, bind, key = 'int'):
        self.bind = [bind]
        self.key  = [key]

    def extend(self, bind, key =  'int'):
        self.bind.append(bind)
        self.bind.append(key)

    def __str__(self):
        if len(self.key) == 1 and self.key[0] == 'int':
            return '*'
        else:
            return "bind={bind}, key={key}".\
                format(bind="<<%s>>" % ",".join(self.bind),
                       key="%s"%",".join(map(lambda x: ':' + (x if type(x) is str else x.name), self.key)))

class UMLType(object):
    def __init__(self, name, 
                 scope = None, 
                 properties = [],
                 parameters = [],
                 composite = True,
                 #qualifier  = None,
                 multiplicity = 1,):
        self.name = name
        if scope is not None and scope !="":
            self._scope = scope
        if multiplicity is not None and multiplicity != 1:
            # if len(multiplicity) == 2:
            self._multiplicity = multiplicity
            # else:
            #     raise ValueError('Unexpected multiplicity type')
        if len(properties) > 0:
            self._properties = properties
        if len(parameters) > 0:
            self._parameters = parameters
        self.composite = composite


    def add_qualifier(self, bind, key = 'int'):
        if not  self.__dict__.has_key('_qualifier') or self._qualifier is None: 
            self._qualifier = UMLQualifier(bind, key)
        else:
            self._qualifier.extend(bind, key)

    @property
    def qualifier(self):
        if self.__dict__.has_key('_qualifier') and self._qualifier is not None: 
            return str(self._qualifier)
        else: return ''

    def add_property(self, name):
        if not  self.__dict__.has_key('_properties') or self._properties is None: 
            self._properties = []
        self._properties.append(name)

    @property
    def properties(self):
        if self.__dict__.has_key('_properties') and self._properties is not None: 
            return self._properties
        else: return []

    @property
    def parameters(self):
        if self.__dict__.has_key('_parameters') and self._parameters is not None: 
            return self._parameters
        else: return []

    @property
    def reference(self):
        if self.__dict__.has_key('_qualifier') and self._qualifier is not None: 
            return False
        else: 
            if not self.composite and self.__dict__.has_key('_multiplicity') and self._multiplicity == 1:
                return True
            else: return False

    @reference.setter
    def reference(self, is_ref = True):
        if is_ref:
            if self.__dict__.has_key('_qualifier') and self._qualifier is not None: 
                pass
            else: 
                self._multiplicity = 1
                self.composite     = False

    @property
    def pointer(self):
        if self.__dict__.has_key('_qualifier') and self._qualifier is not None: 
            return False
        else: 
            if not self.composite and self.__dict__.has_key('_multiplicity') and self._multiplicity == (0,1):
                return True
            else: return False

    @pointer.setter
    def pointer(self, is_ptr = True):
        if is_ptr:
            if self.__dict__.has_key('_qualifier') and self._qualifier is not None: 
                pass
            else:
                self._multiplicity = (0,1)
                self.composite     = False

    @property
    def full_name(self):
        if self.__dict__.has_key('_scope') and self._scope is not None: 
            return self._scope + "::" + self.name
        else: return self.name

    @property
    def scope(self):
        if self.__dict__.has_key('_scope') and self._scope is not None: 
            return self._scope + "::"
        else: return ''

    @property
    def multiplicity(self):
        if self.__dict__.has_key('_multiplicity') and self._multiplicity is not None: 
            if type(self._multiplicity) is int:
                return str(self._multiplicity)
            else: 
                return '{mult[0]}..{mult[1]}'.format(mult=self._multiplicity)
        else: return '1'

    def __str__(self):
        #return r'{self.scope}{self.name} {parameters} {properties} {self.multiplicity}'.
        return r'{self.name} {parameters} {properties} {self.multiplicity} {self.qualifier}'.\
            format(self=self,
                   parameters= "" if len(self.parameters) == 0 else map(str, self.parameters),
                   properties= "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),)

######################################################################

class UMLClass:
    """
    Unified (language independent) representation of class
    """
    def __init__(self, name, 
                 location = None, 
                 package  = None,
                 methods  = [],
                 attribs  = [],
                 modifiers = [],
                 parent   = None,):
        # Extract data
        self.name       = name
        self.package    = package
        self.location   = location

        self.modifiers  = modifiers
        self.add_methods(methods)
        self.add_attributes(attribs)

        # Extract dependencies between 
        self.parent    = parent
        self.provides  = []
        self.requires  = []
        # self.associations = []
        # self.aggregations = []
        self.compositions = []

    def add_attribute(self, attrib):
        self.attributes.append(attrib)
        #if attrib.isUtility: self._utility = False

    def add_attributes(self, attribs):
        if not self.__dict__.has_key("attributes") or self.attributes is None:
            self.attributes = attribs
        else: self.attributes.extend(attribs)

    def add_method(self, method):
        self.methods.append(method)

    def add_methods(self, methods):
        if not self.__dict__.has_key("methods") or self.methods is None:
            self.methods = methods
        else: self.methods.extend(methods)

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    @property
    def full_name(self):
        if self.__dict__.has_key('package') and self.package is not None: 
            return self.package + "::" + self.name
        else: return self.name

    @property
    def isInterface(self):
        if len(self.attributes) > 0:
            return False
        for method in self.methods:
            if not method.isAbstract: return False
        return True

    @property
    def isUtility(self):
        for attrib in self.attributes:
            if not attrib.isUtility: return False
        for method in self.methods:
            if not method.isUtility: return False
        
        return True

    def __str__(self):
        modifiers  = []
        if self.isInterface: modifiers.append('interface')
        if self.isUtility:   modifiers.append('utility')
        modifiers.extend(self.modifiers)
        return "{line}\n{modifiers:^40}\n[{self.package}]{self.name}\n{line}\n{attributes}\n{line}\n{methods}\n{line}".\
            format(self=self, line= chr(196)*40, #unicode('\x80abc', errors='replace')*
                   attributes = "\n".join(map(str,self.attributes)),
                   methods    = "\n".join(map(str,self.methods)),
                   modifiers  = "" if len(modifiers) == 0 else "<<%s>>"%",".join(modifiers))

class UMLClassAttribute:
    def __init__(self, name, type, 
                 visibility, 
                 constant = False,
                 utility = False):
        self.name       = name
        self.type       = type
        self.visibility = visibility
        self._utility     = utility
        # self.properties = []
        # if kwargs['constant']: self.properties.append('readOnly') #friend, extern

    @property
    def isUtility(self):
        return self._utility

    def __str__(self):
        return " {utility}{self.visibility} {self.name}:{self.type}".\
            format(self=self, utility = 'u' if self._utility else ' ',
                   # properties= "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),
                   )

class UMLClassMethod:
    def __init__(self, name, 
                 rtnType, parameters,
                 visibility,
                 abstract   = False,
                 utility    = False,
                 properties = []):
        self.name       = name
        self.rtnType    = rtnType
        self.parameters = parameters
        self.visibility = visibility

        self.properties = properties

        self._abstract = abstract
        self._utility  = utility

    @property
    def isAbstract(self):
        if self.name == "<<destroy>>":
            return True
        else: return self._abstract

    @property
    def isUtility(self):
        if self.name == "<<destroy>>":
            return True
        else: return self._utility

    def __str__(self):
        return "{abstract}{utility}{self.visibility}{self.name}(){rtnType}{properties}".\
            format(self=self, 
                   abstract = 'a' if self._abstract else ' ',
                   utility  = 'u' if self._utility else ' ',
                   properties= "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),
                   rtnType  = "" if self.rtnType is None else ":%s" % self.rtnType)

######################################################################

class UMLGeneralization:
    def __init__(self, parent, child, visibility = '+ '):
        self.parent     = parent
        self.child      = child
        self.visibility = visibility

    def __str__(self):
        return "{self.parent.name}<-[{self.visibility}]-{self.child.name}".format(self=self)

