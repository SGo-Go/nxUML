#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         class_filter.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.

http://www.uml-diagrams.org/class-reference.html
http://support.objecteering.com/objecteering6.1/help/us/cxx_developer/tour/code_model_equivalence.htm
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""


from nxUML.core import UMLQualifier, UMLType
from nxUML.core import UMLClass, UMLClassMethod, UMLClassAttribute
from nxUML.core import UMLGeneralization

import re 

class CppTypeParser(object):
    primitive_types = {
        'char'      : 'char',
        'bool'      : 'boolean',
        'short'     : 'int',
        'signed'    : 'int',
        'unsigned'  : 'int',
        'unsigned short'    : 'int',
        'unsigned char'     : 'int',
        'char'      : 'int',
        'float'     : 'real',
        'double'    : 'real',
        'void*'     : 'undefined',
        'void'      : None,
        }
    containers_single_param = {
        'vector' : 'vector',
        'list'   : 'list',
        'stack'  : 'stack',
        'queue'  : 'queue',
        'deque'  : 'deque', #priority queue
        'set'    : 'set',
        'multiset': 'set',
        'unordered_set': 'set',
        'unordered_multiset': 'set',
        }
    containers_double_param = {
        'map'    : 'map',
        'multimap': 'map',
        'unordered_map': 'map',
        'unordered_multimap': 'map',
        'THBMap'    : 'THBMap',
        }
    specifier_types = {}

    cpp_specifiers = {
        'const'  : 'readOnly',
        'static' : None,
        'mutual' : 'mutable'
        }

    reId        = r"[a-zA-Z_][a-zA-Z0-9_]*"
    reScope     = r"({reId}::)*".format(reId=reId)
    reDelimiter = r"<|>|,"
    reRefPtr    = r"(const)?\s*(\*|&)"
    reFindPrimitive     = re.compile(r"^\s*({reScope})({reId})\s*".\
                                         format(reScope=reScope, reId=reId, reDelimiter=reDelimiter))
    reFindRefPtr        = re.compile(r"^\s*{reRefPtr}\s*".\
                                         format(reScope=reScope, reId=reId, reRefPtr=reRefPtr))
    reFindDelimiter     = re.compile(r"^\s*({reDelimiter})\s*".\
                                         format(reScope=reScope, reId=reId, reDelimiter=reDelimiter))
    reFindSpecifier     = re.compile(r"^\s*({reSpecifier})\s".\
                                         format(reSpecifier=r"|".join(cpp_specifiers.keys())))

    @classmethod
    def parse(cls, strType):
        parsedType, ptr, delim = cls.parse_from_pointer(strType, 0)
        if len(strType) > ptr: 
            raise ValueError('Type parsing error: check "%s" at [%s]' % (strType[ptr:], ptr))
        #print '"%s"' %delim
        return parsedType

    @classmethod
    def parse_from_pointer(cls, strType, ptr):
        currPointer = ptr
        properties  = []
        parameters  = []

        while True:
            m = cls.reFindSpecifier.search(strType[currPointer:])
            if m is None: break
            else: 
                prop = cls.cpp_specifiers[m.group(1)]
                if prop is not None: properties.append(prop)
                currPointer += len(m.group(0))
        del m

        m = cls.reFindPrimitive.search(strType[currPointer:])
        name, scope = m.group(3), m.group(1)
        if(len(scope) > 0): scope = scope[:-2]
        currPointer += len(m.group(0))
        del m
        if name in cls.cpp_specifiers.keys(): 
            raise ValueError('Type parsing error: keyword "%s" cannot be used as a typename [%s]' % (name, currPointer))

        delim = None

        m = cls.reFindDelimiter.search(strType[currPointer:])
        if m is not None and m.group(1) == '<':
            delim = m.group(1)
            currPointer += len(m.group(0))
            del m
            delim = ','
            while delim == ',':
                parsedType, currPointer, delim = cls.parse_from_pointer(strType, currPointer)
                parameters.append(parsedType)
            if delim != '>' : 
                raise ValueError('Type parsing error: close parameters list [%s]' % currPointer)

            if cls.containers_single_param.has_key(name):
                uml_type = parameters[0]
                uml_type.add_qualifier(cls.containers_single_param[name])
            elif cls.containers_double_param.has_key(name):
                uml_type = parameters[1]
                uml_type.add_qualifier(cls.containers_double_param[name], key = parameters[0])
            elif cls.specifier_types.has_key(name):
                uml_type = parameters[0]
                uml_type.add_property(cls.specifier_types[name])
            else:
                uml_type = UMLType(name, scope=scope, properties=properties, parameters = parameters)
        else:
            # if not cls.primitive_types.has_key('Int32'):
            #     raise ValueError(strType)
            uml_type = UMLType(cls.primitive_types.get(name, name), scope=scope, properties=properties)

        m = cls.reFindRefPtr.search(strType[currPointer:])
        if m is not None:
            ptr_modif, ptr_type = m.group(1), m.group(2)
            currPointer += len(m.group(0))
            del m

            if   ptr_type == '&': uml_type.reference    = True
            elif ptr_type == '*': uml_type.pointer      = True

        m = cls.reFindDelimiter.search(strType[currPointer:])
        if m is not None:
            delim = m.group(1)
            currPointer += len(m.group(0))
            del m

        #print ptr, name, scope, delim, properties
        return uml_type, currPointer, delim

######################################################################

class CppTextParser(object):
    TypeParser = CppTypeParser

    visibility_types = {
        'private'       : '#', 
        'protected'     : '-', 
        'public'        : '+',
        }


    @classmethod
    def parse(cls, filename):
        import CppHeaderParser
        try: cppHeader = CppHeaderParser.CppHeader(filename)
        except CppHeaderParser.CppParseError as e: raise e

        for className in cppHeader.classes:
            cls.handle_class(None, location = cppHeader.headerFileName, **cppHeader.classes[className])

        del cppHeader


    @classmethod
    def create_class(cls, **data):
        # Extract data
        uml_class = UMLClass(data['name'],
                             package  = data['namespace'],
                             location = data['location'],
                             parent   = data['parent'],)

        # Work around class attributes
        for visibility in cls.visibility_types.keys():
            for attrib in data['properties'][visibility]:
                cls.handle_attribute(uml_class, visibility = visibility, **attrib)

        # Work around class methods
        for visibility in cls.visibility_types.keys():
            for method in data['methods'][visibility]:
                cls.handle_method(uml_class, visibility = visibility, **method)

        return uml_class
    
    @classmethod
    def create_attribute(cls, **kwargs):
        # {'line_number':, 'constant': , 'name': , 'reference': , 'type': , 'static': , 'pointer': }
        type       = cls.TypeParser.parse(kwargs['type'])
        visibility = cls.visibility_types.get(kwargs['visibility'], ' ')
        uml_attrib = UMLClassAttribute(kwargs['name'], 
                                       type       = type, 
                                       visibility = visibility,
                                       utility    = kwargs['static'])
        return uml_attrib

    @classmethod
    def create_method(cls, **kwargs):
        if kwargs['constructor']: 
            name   = "<<create>>"
        elif kwargs['destructor']: 
            name   = "<<destroy>>"
        else:
            name   = kwargs['name']

        abstract   = kwargs['pure_virtual']
        static     = kwargs['static']

        visibility = cls.visibility_types.get(kwargs['visibility'], ' ')
        visibility+= {True:'/', False: ' '}[kwargs['virtual'] and not abstract]

        rtnType    = cls.TypeParser.primitive_types.get(kwargs['rtnType'], kwargs['rtnType'])
        parameters = [(param['name'], param['type']) for param in kwargs['parameters']]

        properties = []
        if kwargs['const']: properties.append('query') #friend, extern

        uml_method = UMLClassMethod(name, rtnType, parameters,
                                    visibility = visibility,
                                    abstract   = abstract,
                                    utility    = static,
                                    properties = properties)
        return uml_method

    @classmethod
    def create_generalization(cls, **kwargs):
        visibility = cls.visibility_types.get(kwargs['access'], ' ')
        visibility+= '/' if kwargs['virtual'] else ' '
        uml_generalization = UMLGeneralization(parent  = cls.TypeParser.parse(kwargs['parent']),
                                               child   = cls.TypeParser.parse(kwargs['child']),
                                               visibility = visibility,)
        return uml_generalization

    @classmethod
    def handle_attribute(cls, uml_class, **kwargs):
        uml_attrib = cls.create_attribute(**kwargs)
        uml_class.add_attribute(uml_attrib)

    @classmethod
    def handle_method(cls, uml_class, **kwargs):
        uml_method = cls.create_method(**kwargs)
        uml_class.add_method(uml_method)

    @classmethod
    def handle_class(cls, uml_pool, **data):
        uml_class = cls.create_class(**data)

        # Work around inheritances of class
        for gener_link in data['inherits']:
            cls.handle_generalization(uml_pool, child = uml_class.full_name, parent = gener_link['class'], **gener_link)

        print uml_class

    @classmethod
    def handle_generalization(cls, uml_pool, **kwargs):
        uml_generalization = cls.create_generalization(**kwargs)
        print uml_generalization
