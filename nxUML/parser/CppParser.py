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

from nxUML.core import debug,warning

from nxUML.core import UMLPool
from nxUML.core import UMLQualifier, UMLMultiplicity
from nxUML.core import UMLElementRelativeName, UMLDataTypeDecorator
from nxUML.core import UMLPackage, UMLClass, UMLNamespace
from nxUML.core import UMLPrimitiveDataType, UMLDataTypeStub
from nxUML.core import UMLClassMethod, UMLClassAttribute
from nxUML.core import UMLGeneralization
from nxUML.core import UMLInterface
from nxUML.core import UMLSourceFile,UMLSourceReference
from nxUML.core import UMLInt,UMLBoolean,UMLNone,UMLChar,UMLUndefined,UMLReal

import re, os, math


class CppTypeParser(object):
    primitive_types = {
        'char'      : UMLChar,
        'bool'      : UMLBoolean,
        'short'     : UMLInt,
        'signed'    : UMLInt,
        'unsigned'  : UMLInt,
        'unsigned short'    : UMLInt,
        'unsigned char'     : UMLInt,
        'char'      : UMLInt,
        'float'     : UMLReal,
        'double'    : UMLReal,
        'void*'     : UMLUndefined,
        'void'      : UMLNone,
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

    expression_functions = {
        "sin"      : math.sin,
        "sqrt"     : math.sqrt,
        }

    specifier_types = {}

    cpp_specifiers = {
        'const'   : 'readOnly',
        'static'  : None,
        'mutable' : 'mutable',
        'volatile': 'volatile',
        'typename': 'typename',

        # Only functions 
        # @TODO  fix this bug in CppParseHeader
        'inline'  : 'inline',

        'union'   : 'union',
        }


    expr_open_parent   = list(r"<{[(")
    expr_close_parent  = list(r">}])")
    close_open_pairing = dict(zip(expr_close_parent, expr_open_parent))

    reId        = r"[a-zA-Z_][a-zA-Z0-9_]*"
    reNumeric   = r"(0x[0-9a-fA-F]+|0[0-7]+|[-+]?\d*\.?\d+([eE][-+]?\d+)?)"
    reString    = r'\"([^"]|\\")*\"'
    reScope     = r"({reId}(<.*>)?::)*".format(reId=reId)
    reDelimiter = r"<|>|,"
    reRefPtr    = r"(\*(\s*const)?|&)"

    # Compiled regexps in use
    reFindId                  = re.compile(r"^\s*(template\s+)?({reId})\s*".format(reId=reId))
    reFindNamespaceSeparator  = re.compile(r"^\s*::\s*")
    reFindSuffixSpecifier     = re.compile(r"^\s*(const)\s*".\
                                               format(reSpecifier=r"|".join(cpp_specifiers.keys())))
    reFindPrefixSpecifier     = re.compile(r"^\s*({reSpecifier})\s+".\
                                               format(reSpecifier=r"|".join(cpp_specifiers.keys())))
    reFindRefPtr              = re.compile(r"^\s*{reRefPtr}\s*".\
                                               format(reScope=reScope, reId=reId, reRefPtr=reRefPtr))
    reCheckEmpty              = re.compile(r"^\s*$")

    # Deprivated regexps
    reFindPrimitive     = re.compile(r"^\s*({reScope})({reId})\s*".\
                                         format(reScope=reScope, reId=reId, reDelimiter=reDelimiter))
    reFindDelimiter     = re.compile(r"^\s*({reDelimiter})\s*".\
                                         format(reScope=reScope, reId=reId, reDelimiter=reDelimiter))
    reFindValue         = re.compile(r"^\s*({reNumeric}|{reString})\s*".\
                                         format(reNumeric = reNumeric, reString = reString))

    # @classmethod
    # def cname2umlId(cls, name):
    #     return name.replace('::', '.')

    @classmethod
    def eval(cls, expr):
        """
        @TODO exclude syntaxis in Python but unavailable in C++
        E.g. double-star operator for powering
        """
        return eval(expr, {"__builtins__":None}, cls.expression_functions)

    @classmethod
    def is_expression(cls, expr):
        try: 
            cls.eval(expr)
            return True
        except SyntaxError: return False
        except: return False

    @classmethod
    def parse_simple_scope(cls, strType):
        # scope_pieces = strType.split('::')
        # if len(scope_pieces) == 1:
        uml_scope = UMLElementRelativeName(strType.split('::'))
        return uml_scope

    @classmethod
    def split_name(cls, cpp_name):
        """Splits C++ full name on name and namespace
        """
        cpp_name_parts = cpp_name.rsplit('::', 1)
        if(len(cpp_name_parts) > 1):
            return cpp_name_parts[1], cpp_name_parts[0]
        else: return cpp_name_parts[0], None

    @classmethod
    def parse(cls, strType):
        parsedType, ptr = cls.parse_from_pointer(str(strType), 0)
        if not cls.reCheckEmpty.match(strType[ptr:]) : 
            raise ValueError('Type parsing error: End of type "%s" is expected at [%s]' % (strType, ptr))
        return parsedType

    @classmethod
    def get_template_parameters(cls, strType, ptr):
        # Caution: This function fails if parameters list contains expressions with << and >> operators.
        #         It requires somewhat more sophisticated algorithm for <> parens analysis
        #         Similarly, if there are escape '\"' in string litrals, it might cause parsing problems
        # @TODO add safe recognition of  << and >> operators and strings literals
        if len(strType) > ptr + 1 and strType[ptr] == '<':
            params = []
            unclosed_parens = []
            ptrCurr = ptr+1
            treat_string_literal = False
            for i in xrange(ptrCurr, len(strType)):
                ch = strType[i]
                if ch == r'"':
                    treat_string_literal = not treat_string_literal
                if not treat_string_literal:
                    if ch in cls.expr_close_parent:
                        if ch == '>' and len(unclosed_parens) == 0:
                            params.append(strType[ptrCurr:i])
                            return i+1, params
                        if cls.close_open_pairing[ch] != unclosed_parens.pop():
                            raise ValueError('Type parsing error: unbalances parens in "%s" at [%s]' % (strType, i))
                    elif ch in cls.expr_open_parent:
                        unclosed_parens.append(ch)
                    elif ch == ',' and len(unclosed_parens) == 0:
                        params.append(strType[ptrCurr:i])
                        ptrCurr = i+1
            if treat_string_literal:
                raise ValueError('Type parsing error: string literal is not closed in "%s" at [%s]' % (strType, i))
            else:
                raise ValueError('Type parsing error: close paren for < is not found in "%s" at [%s]' % (strType, i))
        else: return ptr, None

    @classmethod
    def parse_from_pointer(cls, strType, ptr):
        currPointer = ptr
        properties  = []
        parameters  = []

        # Expressions are saved as constrant string literals
        if cls.is_expression(strType):
            return strType, len(strType)


        while True:
            m = cls.reFindPrefixSpecifier.search(strType[currPointer:])
            if m is None: break
            else: 
                prop = cls.cpp_specifiers[m.group(1)]
                if prop is not None: properties.append(prop)
                currPointer += len(m.group(0))
        del m

        scope = UMLElementRelativeName()
        while True:
            m = cls.reFindId.search(strType[currPointer:])
            if m is not None:
                currPointer += len(m.group(0))

                if m.group(1) is not None: keywordTemplate = True
                else: keywordTemplate = False

                name = m.group(2)
                del m
            else:
                raise ValueError('Type parsing error: cannot be used as a typename "%s" [%s]' % (strType, currPointer))

            if name in cls.cpp_specifiers.keys(): 
                raise ValueError('Type parsing error: keyword "%s" cannot be used as a typename "%s" [%s]' % (name, strType, currPointer))

            currPointer, params = cls.get_template_parameters(strType, currPointer)
            if keywordTemplate and params is None:
                raise ValueError('Type parsing error: Templated scope has no parameters in a typename "%s" [%s]' % (name, strType, currPointer))
                

            m = cls.reFindNamespaceSeparator.search(strType[currPointer:])
            if m is None: break # part of name, not scope
            else: 
                currPointer += len(m.group(0))
                del m
                # @TODO here one may add some code for propper namespaces treatment
                scope.append(name)

        if params is not None and len(params) > 0:
            for param in params:
                parsedType = cls.parse(param)
                parameters.append(parsedType)

            if cls.containers_single_param.has_key(name) \
                    and len(parameters)==1 and isinstance(parameters[0], UMLDataTypeDecorator):
                uml_type = parameters[0]
                uml_type.multiplicity.add_qualifier(cls.containers_single_param[name])
            elif cls.containers_double_param.has_key(name) \
                    and len(parameters)==2 and isinstance(parameters[1], UMLDataTypeDecorator):
                uml_type = parameters[1]
                uml_type.multiplicity.add_qualifier(cls.containers_double_param[name], key = parameters[0])
            elif cls.specifier_types.has_key(name):
                uml_type = parameters[0]
                uml_type.add_property(cls.specifier_types[name])
            else:
                uml_base = UMLDataTypeStub(name, scope=scope, parameters = parameters)
                uml_type = UMLDataTypeDecorator(uml_base, properties = properties)
        else:
            if name in cls.primitive_types.keys():
                uml_base = cls.primitive_types[name]
            else:
                uml_base = UMLDataTypeStub(cls.primitive_types.get(name, name), scope=scope)
            uml_type = UMLDataTypeDecorator(uml_base, properties = properties)

        m = cls.reFindSuffixSpecifier.search(strType[currPointer:])
        if m is not None:
            currPointer += len(m.group(0))
            uml_type.add_property(cls.cpp_specifiers[m.group(1)])
            del m

        while True:
            m = cls.reFindRefPtr.search(strType[currPointer:])
            if m is not None:
                ptr_type, ptr_modif = m.group(1)[0], m.group(2)
                currPointer += len(m.group(0))
                del m

                if   ptr_type == '&': uml_type.multiplicity.add_reference()
                elif ptr_type == '*': uml_type.multiplicity.add_pointer()
            else: break

        return uml_type, currPointer

######################################################################

class CppTextParser(object):
    PointerMultiplicity   = UMLMultiplicity(pointer = True)
    ReferenceMultiplicity = UMLMultiplicity(reference = True)

    TypeParser = CppTypeParser

    header_ext = ('.hpp', '.hxx', '.h', '.h++')

    visibility_types = {
        'private'       : '-', 
        'protected'     : '#', 
        'public'        : '+',
        }

    reGetAllCStyleComments = re.compile("/\*.*?\*/",re.DOTALL)
    reGetCppStyleComments  = re.compile("//.*?\n")
    reTypedef      = r"(\s|;|\}})typedef\s+([a-zA-Z0-9_:<>,\*&\s]+(>|\s)+){0};"
    reGetAllUsings = re.compile(r"(\s|;|\}})using\s+(namespace)?\s+(({0}\s*::\s*)*{0})\s*;".format(TypeParser.reId), re.DOTALL)

    reIfdefIf   = re.compile(r"^\s*#\s*(if(n)?def|if\s+defined)\s+({0})\s*".format(TypeParser.reId))
    reIfdefElse = re.compile(r"^#\s*else\s*")
    # reIfdefEnd  = re.compile(r"^#\s*endif\s*".format(TypeParser.reId))
    reIfdefEnd  = re.compile(r"^\s*#endif")

    @classmethod
    def parse(cls, filename, 
              uml_pool = None, 
              include_paths = [], 
              hash_type = None, 
              defined_macros = None): 
        if uml_pool is None: uml_pool = UMLPool()

        ########################################
        # Parse codes
        ########################################

        strCppCode = ""
        typedefs_table = {} # Create typedefs table regardless of succes in filename opening
        with open(filename, "r") as fileToAnalyse:
            strCppCode = fileToAnalyse.read()
            # if strCppCode.find('#ifndef OMAP') > 0:
            #     print filename

            strCppCode = cls.preprocessor_remove_conditionals(strCppCode, defined_macros)

            # Pre-parsing by external package CppHeaderParser
            try: 
                import CppHeaderParser
                cppHeader = CppHeaderParser.CppHeader(strCppCode, argType="string",)
            except CppHeaderParser.CppParseError as e: raise e


            # Fill up classes table
            classes_table = {}
            for className, classData in cppHeader.classes.items():
                if classData['namespace'] is None: name = classData['name']
                else: name = '::'.join((classData['namespace'], classData['name']))
                classes_table[name] = classData

            # Fill up packages (C++ namespaces) table
            packages_table = {}
            for namespace in cppHeader.namespaces:
                name, holder = cls.TypeParser.split_name(namespace)
                packages_table[namespace] = {'name': name, 'namespace': holder}


            # Parse codes which are not processed by CppHeaderParser
            # @TODO improve performance 
            # Reason: so far the code below is just a dirty hack 
            #         covering lack of typedef parsing in CppHeaderParser
            # I.e. brute search and analysis of elements which are not pparsed by CppHeaderParser

            # Remove C++ and C style comments and convert file in a single string
            strCppCode = cls.reGetAllCStyleComments.sub \
                ("", cls.reGetCppStyleComments.sub \
                     ("", strCppCode)).replace('\n', ' ')

            #     Use find_open_scopes to find all usings 
            #     (usings are not supported by CppParseHeader)
            usings = cls.find_open_scopes(strCppCode)

            # Work around class typedefs : compute typedefs table
            for className, data in classes_table.items():
                for visibility in cls.visibility_types.keys():
                    for typedef in data['typedefs'][visibility]:
                        # @Dirty hack:
                        #   Fix for "dirty" typedef representation by names 
                        #   without specification of content in CppHeaderParser 
                        #   if type-name follows closing template parameters without spacing
                        if typedef[0] == '>': typedef = typedef[1:] 

                        # Filter out typedefs for function pointers
                        # @TODO implement proper work arount typedefs for pointers 
                        if cls.TypeParser.reFindId.search(typedef) is not None:
                            m = re.search(cls.reTypedef.format(typedef), strCppCode)
                            if m is not None:
                                typedefs_table['::'.join((className, typedef))] = {\
                                    'name' : typedef,
                                    'namespace': className,
                                    'type' : m.group(2),
                                    'visibility': visibility, 
                                    }
                            else: 
                                raise ValueError('Parsing error: cannot parse typedef "%s"' % typedef)
                        else:
                            warning('Parser ignore typedef for function pointer "%s" in "%s"' % (typedef, filename))


            # for className, classData in classes_table.items():
            #     classData['classes'] = \
            #         [name for name, data in classes_table.items() if data['namespace'] == className]

        parse_table = {'typedefs' : typedefs_table, 
                       'packages' : packages_table,
                       'classes'  : classes_table}

        ########################################
        # Fill-up artifact for the header file 
        ########################################
        uml_source = cls.create_source_artifact(uml_pool, filename# cppHeader.headerFileName
                                                , constructor = UMLSourceFile
                                                , local = True)
        uml_pool.deployment.sources.add(uml_source, forced = True)
        sourceId = uml_source.id
        
        # Add hash to artifact if required
        if hash_type is not None:
            import hashlib
            uml_source.hash = (hash_type,
                               eval("hashlib.{0}(open(filename, 'r').read()).digest()".format(hash_type)))

        # Use artifact as manifestation anchor for classes and packages
        for className, classData in classes_table.items():
            classData['sourceId'] = sourceId
        for packageName, packageData in packages_table.items():
            packageData['sourceId'] = sourceId

        ########################################
        # Walk through definitions in the header
        ########################################

        # Handle usings 
        for using in usings:
            cls.handle_using(uml_pool, name = using, 
                             sourceId = sourceId)

        # Handle includes
        source_folder = os.path.join(uml_pool.deployment.sources.source_prefix, 
                                     uml_source.folder)
        all_include_paths = [source_folder] + list(include_paths)
        for sourceFile in cppHeader.includes:
            cls.handle_include(uml_pool, sourceId = sourceId, include_name=sourceFile, 
                               include_paths = all_include_paths)

        # Run recursive namespace tree building from global namespace
        # Handle global namespace as root package
        cls.handle_packageables(uml_pool, uml_pool.root, None, parse_table)

        # # Handle classes
        # for className in classes_table:
        #     classData = classes_table[className]
        #     if classData['parent'] is None:
        #         # print '@@', className, classData['namespace']
        #         subclasses = dict([(name,data) \
        #                                for name, data in classes_table.items() \
        #                                if  data['parent'] == className])
        #         cls.handle_class(uml_pool, 
        #                          location       = sourceId,
        #                          subclasses     = subclasses,
        #                          cpp_code       = strCppCode,
        #                          typedefs_table = typedefs_table,
        #                          parsed_header  = cppHeader,
        #                          **classes_table[className])
        #         del subclasses

        # Free memory and return reference on include artifact
        del cppHeader
        del strCppCode
        return uml_source

    @classmethod
    def find_open_scopes(cls, strCppCode, uml_pool = None, include_paths = []):
        # filename = uml_pool.deployment.sources.abspath(data['manifestation'])
        usings = []
        for m in cls.reGetAllUsings.finditer(strCppCode):
            using = m.group(3)
            if m.group(2) is not None: using += '::*'
            usings.append(using)
        return usings

    @classmethod
    def preprocessor_remove_conditionals(cls, strCppCode, defined_macros):
        """Replaces by empty strings the code inside ifdef's 
        depending on whether macros are defined or not

        Behaviour:
        defined_macros specifies the dict of macro with 
        True value if is supposed to be defined, and
        False value if is supposed to be undefined.
        If macro is not in the list we make if open for the first occurance
        i.e. defined for ifdef and undefined for ifndef
        """
        if defined_macros and len(defined_macros) > 0:
            strCppReduced = ""   # preprocessed C++-code 
            stackIfdefNames = [] # stack of names for macro used in conditionals
            # Stack of regimes for each macro (True if insert)
            # If there is at least one False, we use no insertion mode
            stackIfdefModes = [] 
            insertionMode = True
            for line in strCppCode.split("\n"):
                m = cls.reIfdefIf.search(line)
                if m:
                    nameMacro  = m.group(3)
                    insertionModeMacro = (nameMacro not in defined_macros.keys()) \
                        or (not(m.group(2) == 'n') == defined_macros[nameMacro])
                    stackIfdefNames.append(nameMacro)
                    stackIfdefModes.append(insertionModeMacro)
                    insertionMode = insertionMode and insertionModeMacro
                elif cls.reIfdefElse.search(line): 
                    stackIfdefModes[-1] = not stackIfdefModes[-1]
                    insertionMode = not(False in stackIfdefModes)
                elif cls.reIfdefEnd.search(line): 
                    stackIfdefNames.pop()
                    stackIfdefModes.pop()
                    insertionMode = not(False in stackIfdefModes)
                else: 
                    if insertionMode: strCppReduced += line
                strCppReduced += '\n'
            if len(stackIfdefNames) > 0: print [len(stackIfdefNames)]*10
        else: strCppReduced = strCppCode
        return strCppReduced

    @classmethod
    def handle_packageables(cls, uml_pool, uml_namespace, cpp_fullname, parse_table, **data):
        """Recursively walk throung components of namespace and register them if required.
        Order: classes > packages > typedefs.
        """
        for className, classData in parse_table['classes'].items():
            if classData['namespace'] == cpp_fullname:
                uml_class = cls.handle_class(uml_pool, uml_namespace, className, parse_table, **classData)
                if uml_class: uml_namespace.add(uml_class)

        for packageName, packageData in parse_table['packages'].items():
            if packageData['namespace'] == cpp_fullname:
                uml_package = cls.handle_package(uml_pool, uml_namespace, packageName, parse_table, **packageData)
                if uml_package: uml_namespace.add(uml_package)

        # Work around class typedefs 
        for typeName, typeData in parse_table['typedefs'].items():
            if typeData['namespace'] == cpp_fullname:
                # debug(typeData['name'], cpp_fullname)
                uml_type = cls.handle_typedef(uml_pool, uml_namespace, **typeData)
                if uml_type: uml_namespace.add(uml_type)

    @classmethod
    def create_package(cls, uml_pool, uml_namespace, parse_table, **data):
        uml_package  = UMLPackage(name = data['name'], scope = uml_namespace)
        return uml_package

    @classmethod
    def create_class(cls, uml_pool, uml_namespace, parse_table, **data):
        # Extract data
        uml_class = UMLClass(str(data['name']),
                             scope     = uml_namespace, 
                             manifestation = data['sourceId'], 
                             methods   = [],
                             attribs   = [],
                             modifiers = [],
                             parent    = data['parent'],)

        # Work around inheritances of class
        # @TODO: Move it to a propper place
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
                cls.handle_generalization(uml_pool, uml_class, cls.TypeParser.parse(parent_name).base, 
                                          **gener_link_data)

        # Work around class attributes
        for visibility in cls.visibility_types.keys():
            for attrib in data['properties'][visibility]:
                # Hack for incorrent processing of  usings and friends in CppHeaderParser:
                #   CppHeaderParser recognizes usings and friend types inside classes as attributes.
                #   Thus we simply ignore attributes which types contain keywords using or friend
                if attrib['type'].find('using ') != 0 and attrib['type'].find('friend ') != 0: 
                    cls.handle_attribute(uml_class, visibility = visibility, **attrib)

        # Work around class methods
        for visibility in cls.visibility_types.keys():
            for method in data['methods'][visibility]:
                cls.handle_method(uml_class, visibility = visibility, **method)

        
        # Register parsed class as a component of source
        uml_source = uml_pool.deployment.source(uml_class.manifestation)
        if uml_source.__dict__.has_key('classes'):
            uml_source.classes.append(uml_class.id)
        else: uml_source.classes = [uml_class.id]

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

        rtnType    = kwargs['rtnType'] #cls.TypeParser.primitive_types.get(kwargs['rtnType'], kwargs['rtnType'])
        # rtnType    = cls.TypeParser.parse(kwargs['rtnType'])
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
    def create_generalization(cls, child, parent, **kwargs):
        visibility = cls.visibility_types.get(kwargs['access'], ' ')
        visibility+= '/' if kwargs['virtual'] else ' '
        uml_generalization = UMLGeneralization(parent     = parent,
                                               child      = child,
                                               visibility = visibility,)
        return uml_generalization

    ############################################################
    # Handles for class components
    ############################################################

    @classmethod
    def handle_attribute(cls, uml_class, **kwargs):
        uml_attrib = cls.create_attribute(**kwargs)
        uml_class.add_attribute(uml_attrib)

    @classmethod
    def handle_method(cls, uml_class, **kwargs):
        uml_method = cls.create_method(**kwargs)
        uml_class.add_method(uml_method)

    ############################################################
    # Handles for packageable elements 
    ############################################################

    @classmethod
    def handle_class(cls, uml_pool, uml_namespace, cpp_fullname, parse_table, **data):
        # debug(cpp_fullname)
        uml_class = cls.create_class(uml_pool, uml_namespace, parse_table, **data)
        # uml_pool.add_class(uml_class) #@TODO
        uml_namespace.add(uml_class)

        # Handle internal classes and types
        cls.handle_packageables(uml_pool, uml_class, cpp_fullname, parse_table, **data)
        return uml_class

    @classmethod
    def handle_package(cls, uml_pool, uml_namespace, cpp_fullname, parse_table, **data):
        # debug(cpp_fullname)
        uml_package = cls.create_package(uml_pool, uml_namespace, parse_table, **data)

        # Register package in the pool if required
        # Note: in C++ package can be defined independently in multiple places
        #     even inside a single file, not saying several files
        if uml_namespace.name == uml_package.name: raise
        if uml_namespace.named_elements.has_key(uml_package.name):
            uml_package = uml_namespace.named_elements[uml_package.name] 
        else: uml_namespace.add(uml_package)
        # if uml_pool.package.has_key(uml_package.id):
        #     uml_package = uml_pool.package[uml_package.id]
        # else: uml_pool.add_package(uml_package)  #@TODO

        # Handle internal classes and types
        cls.handle_packageables(uml_pool, uml_package, cpp_fullname, parse_table, **data)
        return uml_package

    @classmethod
    def handle_typedef(cls, uml_pool, uml_namespace, **data):
        return None

    ############################################################
    # Handles for relationships
    ############################################################

    @classmethod
    def handle_generalization(cls, uml_pool, child, parent, **kwargs):
        uml_generalization = cls.create_generalization(child, parent, **kwargs)
        # uml_pool.add_relationship(uml_generalization)
        child.add_relationship(uml_generalization)
        return uml_generalization

    @classmethod
    def location2url(cls, localpath):
        import urlparse, urllib
        url = urlparse.urljoin('file:', urllib.pathname2url(localpath))
        # url = "file://localhost/" + filename.replace("\\", "/")
        # url = urlparse.urlunparse(urlparse.urlparse(filename)._replace(scheme='file'))
        return url

    ############################################################
    # Artifacts filling 
    ############################################################

    @classmethod
    def create_source_artifact(cls, uml_pool, filename, constructor = UMLSourceFile, **data):
        folder = os.path.dirname(filename)
        name, ext = os.path.splitext(os.path.basename(filename))
        uml_source = constructor(name, ext=ext, folder=folder,
                                 # stereotype = 'C++ header',
                                 local = data['local'])
        uml_source.remove_prefix(uml_pool.deployment.sources.source_prefix)
        return uml_source

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

        uml_source = cls.create_source_artifact(uml_pool, full_name, constructor = UMLSourceReference, local = found)
        uml_pool.deployment.sources.add(uml_source, forced = False)
        uml_pool.deployment.sources.add_edge(sourceId, uml_source.id)

    @classmethod
    def handle_using(cls, uml_pool, name, sourceId = None, **data):
        if sourceId is not None:
            uml_relname = cls.TypeParser.parse_simple_scope(name)
            uml_pool.deployment.source(sourceId).open_names.append(uml_relname)


    @classmethod
    def resolve_names(cls, uml_pool):
        # idTypes = dict(map(lambda name: (name,'package'), uml_pool.package.keys()) +
        #                map(lambda name: (name,'Class'), uml_pool.Class.keys()))
        # getElementById = lambda uml_pool, idType: \
        #     eval('uml_pool.{0}[idType]'.format(idTypes[idType]))
        # hasElementWithId = lambda idType: idTypes.has_key(idType)

        # # Loop over packages
        # for pckgId, pckgItem in uml_pool.package.items():
        #     pckgScopeId = pckgItem.scope.id
        #     if hasElementWithId(pckgScopeId) :
        #         pckgItem.scope = getElementById(uml_pool, pckgScopeId)

        # Loop over classes
        for uml_class in uml_pool.namespaces_dfs():
            if not isinstance(uml_class, UMLClass): continue
            classScopeId = uml_class.scope.id
            
            # Reviel relevant usings for name resolution 
            name_openings = cls.get_name_openings(uml_pool, uml_class.manifestation)

            # Resolve names for attributes taking into account usings
            for attrib in uml_class.attributes:
                attrib.type.base = cls.resolve_simple_type(uml_pool, attrib.type.base, 
                                                           uml_class, name_openings)
                # print type(attrib.type.base)

            # Loop over relationships
            # uml_source  = uml_relationship.source
            # print len(uml_class.relationships)
            for uml_relationship in uml_class.relationships_iter():
                uml_destination = uml_relationship.destination
                uml_relationship.destination = cls.resolve_simple_type(uml_pool, uml_relationship.destination, 
                                                                       uml_class, # Similarly: uml_relationship.source.scope, 
                                                                       name_openings)
                # if isinstance(uml_relationship.destination, UMLDataTypeStub):
                #     print type(uml_relationship.destination), type(uml_destination), type(uml_relationship.source)
                #     print uml_relationship.destination.id, uml_relationship.source.id

    @classmethod
    def resolve_simple_type(cls, uml_pool, uml_type_base, 
                            embracing_scope, name_openings):
        """Resolve single name
        """
        if isinstance(uml_type_base, UMLDataTypeStub):
            path_to_try = [uml_type_base]
            for relpath in name_openings:
                new_path = relpath.embed(uml_type_base)
                if new_path:
                    path_to_try.append(new_path)
                    # if embracing_scope.name == 'CMapCommandBroker' and uml_type_base.name == 'IPersistenceService':
                    #     debug(new_path) #relpath, uml_type_base, 

            # @TODO Implement correct scope resolution order
            for new_path in path_to_try:
                scope = embracing_scope
                while scope:
                    uml_classifier = scope.get(uml_type_base)
                    if uml_classifier: return uml_classifier
                    else: scope = scope.scope
        return uml_type_base

    @classmethod
    def get_name_openings(cls, uml_pool, sourceId,):
        """Get usings from headers (upto 1 level of depth in hierarchy) 
        for further name resolution 
        """
        name_openings = []
        if sourceId:
            uml_source = uml_pool.deployment.source(sourceId)
            headers = [uml_source]
            for sourceId in uml_pool.deployment.sources.succ[uml_source.id]:
                headers.append(uml_pool.deployment.source(sourceId))

            for uml_source in headers:
                name_openings.extend(uml_source.open_names)
            # debug(name_openings)
        return name_openings
