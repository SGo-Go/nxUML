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


from nxUML.core import UMLPool
from nxUML.core import UMLQualifier, UMLType
from nxUML.core import UMLClass, UMLClassMethod, UMLClassAttribute
from nxUML.core import UMLGeneralization
from nxUML.core import UMLInterface
from nxUML.core import UMLSourceFile

import re, os, math

def debug(*args):
    print(args)

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

    builtin_functions = {
        "std::sin"      : math.sin,
        "std::sqrt"     : math.sqrt,
        }# eval(str,{"__builtins__":None},builtin_functions)

    specifier_types = {}

    cpp_specifiers = {
        'const'  : 'readOnly',
        'static' : None,
        'mutable': 'mutable'
        }

    reId        = r"[a-zA-Z_][a-zA-Z0-9_]*"
    reNumeric   = r"(0x[0-9a-fA-F]+|0[0-7]+|[-+]?\d*\.?\d+([eE][-+]?\d+)?)"
    reString    = r'\"([^"]|\\")*\"'
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
    reFindConstSuffix   = re.compile(r"^\s*const\s*".\
                                         format(reSpecifier=r"|".join(cpp_specifiers.keys())))
    reFindValue         = re.compile(r"^\s*({reNumeric}|{reString})\s*".\
                                         format(reNumeric = reNumeric, reString = reString))

    @classmethod
    def cname2umlId(cls, name):
        return name.replace('::', '.')

    @classmethod
    def parse(cls, strType):
        parsedType, ptr, delim = cls.parse_from_pointer(str(strType), 0)
        if len(strType) > ptr: 
            raise ValueError('Type parsing error: check "%s" at [%s]' % (strType, ptr))
        #debug('"%s"' %delim)
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

        m = cls.reFindValue.search(strType[currPointer:]) # @TODO
        if m is not None: print eval(m.group(0))
        
        m = cls.reFindPrimitive.search(strType[currPointer:])
        if m is not None:
            currPointer += len(m.group(0))
            name, scope = m.group(3), m.group(1)
            if(len(scope) > 0): scope = scope[:-2].replace('::', '.')
            del m
        else:
            raise ValueError('Type parsing error: cannot be used as a typename "%s" [%s]' % (strType, currPointer))

        if name in cls.cpp_specifiers.keys(): 
            raise ValueError('Type parsing error: keyword "%s" cannot be used as a typename "%s" [%s]' % (name, strType, currPointer))

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
                raise ValueError('Type parsing error: close parameters list in a typename "%s" [%s]' % (strType, currPointer))

            if cls.containers_single_param.has_key(name):
                #debug('!!!!', parameters[0])
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

        m = cls.reFindConstSuffix.search(strType[currPointer:])
        if m is not None:
            currPointer += len(m.group(0))
            del m

        m = cls.reFindDelimiter.search(strType[currPointer:])
        if m is not None:
            delim = m.group(1)
            currPointer += len(m.group(0))
            del m

        #debug(ptr, name, scope, delim, properties)
        return uml_type, currPointer, delim

######################################################################

class CppTextParser(object):
    TypeParser = CppTypeParser

    header_ext = ('.hpp', '.hxx', '.h', '.h++')

    visibility_types = {
        'private'       : '-', 
        'protected'     : '#', 
        'public'        : '+',
        }


    @classmethod
    def parse(cls, filename, uml_pool = None, include_paths= []):
        if uml_pool is None: uml_pool = UMLPool()

        import CppHeaderParser
        try: cppHeader = CppHeaderParser.CppHeader(filename)
        except CppHeaderParser.CppParseError as e: raise e

        uml_source = cls.create_source_artifact(uml_pool, cppHeader.headerFileName, local = True)
        uml_pool.deployment.sources.add(uml_source, forced = True)
        sourceId = uml_source.id
        
        source_folder = os.path.join(uml_pool.deployment.sources.source_prefix, 
                                     uml_source.folder)

        all_include_paths = [source_folder] + list(include_paths)
        for sourceFile in cppHeader.includes:
            cls.handle_include(uml_pool, sourceId = sourceId, include_name=sourceFile, 
                               include_paths = all_include_paths)

        for className in cppHeader.classes:
            classData = cppHeader.classes[className]
            if classData['parent'] is None:
                subclasses = dict([(name,data) \
                                       for name, data in cppHeader.classes.items() \
                                       if data['parent'] == className])
                cls.handle_class(uml_pool, 
                                 location = sourceId,
                                 subclasses  = subclasses,
                                 **cppHeader.classes[className])
                del subclasses

        del cppHeader
        return uml_pool

    @classmethod
    def create_class(cls, uml_pool, **data):
        # Extract data
        uml_class = UMLClass(str(data['name']),
                             package   = str(data['namespace']).replace('::', '.'),
                             location  = data['location'], #cls.location2url(data['location']), @TODO url 
                             methods   = [],
                             attribs   = [],
                             modifiers = [],
                             parent    = data['parent'],)
        #debug('!!!', uml_class.__dict__)

        # Work around inheritances of class
        # Caution: it includes hack for improper 
        #        handling of templated inheritances in CppHeaderParser
        new_generalization  = True
        for gener_link in data['inherits']:
            if new_generalization:
                parent_name = ''
                gener_link_data = gener_link
                new_generalization = False
                pass
            parent_name += (',' if len(parent_name) > 0 and \
                                gener_link['class'] != '>' else '') + gener_link['class']
            if parent_name.count('<') == parent_name.count('>'):
                new_generalization = True
                cls.handle_generalization(uml_pool, 
                                          parent = cls.TypeParser.parse(parent_name), 
                                          child  = uml_class,
                                          **gener_link_data)

        # Work around class attributes
        for visibility in cls.visibility_types.keys():
            for attrib in data['properties'][visibility]:
                cls.handle_attribute(uml_class, visibility = visibility, **attrib)

        # Work around class methods
        for visibility in cls.visibility_types.keys():
            for method in data['methods'][visibility]:
                cls.handle_method(uml_class, visibility = visibility, **method)

        
        # Register parsed class as a component of source
        uml_source = uml_pool.deployment.source(uml_class.location)
        if uml_source.__dict__.has_key('classes'):
            uml_source.classes.append(uml_class.id)
        else: uml_source.classes = [uml_class.id]


        # Work around class typedefs 
        # @TODO improve performance 
        # Reason: so far the code below is just a dirty hack 
        #         covering lack of typedef parsing in CppHeaderParser
        reTypedef = r"(\s|;|\}})typedef\s+([a-zA-Z0-9_:<>,\*&\s]+(>|\s)+){0};"

        filename = uml_pool.deployment.sources.abspath(data['location'])
        with open (filename, "r") as myfile:
            strFile = myfile.read().replace('\n', ' ')
            for visibility in cls.visibility_types.keys():
                for typedef in data['typedefs'][visibility]:
                    # fix for "dirty" typedef name representation in CppHeaderParser 
                    # if type-name follows closing template parameters without spacing
                    if typedef[0] == '>': typedef = typedef[1:] 

                    m = re.search(reTypedef.format(typedef), strFile)
                    if m is not None:
                        cls.handle_typedef(uml_pool, uml_class, name = typedef, 
                                           type = m.group(2),
                                           visibility = visibility,)
                    else: 
                        raise ValueError('Parsing error: cannot parse typedef "%s"' % typedef)
            del strFile


        return uml_class
    
    @classmethod
    def create_attribute(cls, **kwargs):
        # {'line_number':, 'constant': , 'name': , 'reference': , 'type': , 'static': , 'pointer': }
        type       = cls.TypeParser.parse(kwargs['type'])
        visibility = cls.visibility_types.get(kwargs['visibility'], ' ')
        uml_attrib = UMLClassAttribute(str(kwargs['name']), 
                                       type       = type, 
                                       visibility = visibility,
                                       constant   = kwargs['constant'],
                                       utility    = kwargs['static'])
        return uml_attrib

    @classmethod
    def create_method(cls, **kwargs):
        if kwargs['constructor']: 
            name   = "<<create>>"
        elif kwargs['destructor']: 
            name   = "<<destroy>>"
        else:
            name   = str(kwargs['name'])

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
    def create_generalization(cls, parent, child, **kwargs):
        visibility = cls.visibility_types.get(kwargs['access'], ' ')
        visibility+= '/' if kwargs['virtual'] else ' '
        uml_generalization = UMLGeneralization(parent  = parent,
                                               child   = child,
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
    def handle_typedef(cls, uml_pool, uml_holder, **kwargs):
        pass

    @classmethod
    def handle_subclass(cls, uml_pool, **data):
        cls.handle_class(uml_pool, **data)

    @classmethod
    def handle_class(cls, uml_pool, **data):
        uml_class = cls.create_class(uml_pool, **data)
        uml_pool.add_class(uml_class)

        # Work around subclasses
        if data.has_key('subclasses') and len(data['subclasses']) > 0:
            for className, classData in data['subclasses'].items():
                cls.handle_subclass(uml_pool, location = data['location'], **classData)


    @classmethod
    def handle_generalization(cls, uml_pool, parent, child, **kwargs):
        uml_generalization = cls.create_generalization(parent, child, **kwargs)
        uml_pool.add_relationship(uml_generalization)

    @classmethod
    def location2url(cls, localpath):
        import urlparse, urllib
        url = urlparse.urljoin('file:', urllib.pathname2url(localpath))
        # url = "file://localhost/" + filename.replace("\\", "/")
        # url = urlparse.urlunparse(urlparse.urlparse(filename)._replace(scheme='file'))
        return url

    @classmethod
    def handle_include(cls, uml_pool, sourceId = None, include_name = '""', 
                       include_paths = [], **data):
        filename = include_name[1:-1]

        folder = os.path.dirname(filename)
        name, ext = os.path.splitext(os.path.basename(filename))
        found = False
        if include_name[0] == '"' and include_name[-1] == '"':
            for include_folder in include_paths:
                full_name = os.path.join(include_folder, filename)
                if os.path.isfile(full_name):
                    folder = os.path.dirname(full_name)
                    found = True
                    break
        else:
            full_name = filename
            local = False

        uml_source = cls.create_source_artifact(uml_pool, full_name, local = found)
        uml_pool.deployment.sources.add(uml_source, forced = False)
        uml_pool.deployment.sources.add_edge(sourceId, uml_source.id)
        #exit()


    @classmethod
    def create_source_artifact(cls, uml_pool, filename, **data):
        folder = os.path.dirname(filename)
        name, ext = os.path.splitext(os.path.basename(filename))
        uml_source = UMLSourceFile(name, ext=ext, folder=folder,
                                   stereotype = 'source',
                                   local = data['local'])
        uml_source.remove_prefix(uml_pool.deployment.sources.source_prefix)
        return uml_source
