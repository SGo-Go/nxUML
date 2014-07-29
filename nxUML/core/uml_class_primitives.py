#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_class_primitives.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

######################################################################
class UMLElementRelativeName(list):
    """Relative scope. 
    Used if the real scope is not known.
    """
    def __init__(self, init_values = []):
        if hasattr(init_values, '__iter__'):
            super(UMLElementRelativeName, self).__init__(init_values)
        else: super(UMLElementRelativeName, self).__init__((init_values,))

    # def __getitem__(self, key):
    #     try:
    #         return super(UMLElementRelativeName, self).__getitem__(key-1)
    #     except IndexError: return None

    @property
    def full_name(self):
        return '.'.join(self) if len(self) > 1 else self.name

    @property
    def name(self):
        return self[-1] if len(self) > 0 else None

    def __repr__(self):
        return str(self.full_name)

    def __eq__(self, scope):
        if self.name == '*': return True
        # print('++', self, scope)
        innerName = self.full_name
        outerName = scope.full_name

        if   innerName == outerName:
            return True
        elif len(innerName) < len(outerName):
            return False
        elif innerName == outerName[:-len(innerName)] and outerName[-len(innerName)-1] == '.':
            return True
        else: return False

    def join(self, rel_path):
        scope = rel_path
        path_ending = []
        while isinstance(scope, UMLNamedPackageableElement):
            path_ending.append(scope.name)
            scope = scope.scope
        self.extend(scope)
        while len(path_ending)>0:
            self.append(path_ending.pop())
        return self

    def embed(self, rel_path):
        if self.name == '*':
            return self.scope.join(rel_path)
        elif self.__eq__(rel_path):
            return UMLElementRelativeName(self[:])
        else: return None

    @property
    def scope(self):
        return UMLElementRelativeName(self[:-1]) if len(self) > 1 else UMLElementRelativeName()

    @property
    def id(self):
        return '.'.join(self) if len(self) > 1 else self.name

    def rel_id(self, scope):
        scope_id = scope.id
        return '.'.join([scope_id, self.id]) if len(scope_id) > 0 else self.id

######################################################################
class IUMLElement(object):
    @property
    def id(self):
        raise NotImplementedError('{0} elements are not identifiable'.format(type(self)))

######################################################################
class UMLNamedElement(IUMLElement):
    def __init__(self, name, **args):
        self.name = name

######################################################################
class IUMLDataType(UMLNamedElement): 
    def toXML(self, root = None, reference = False):
        from lxml import etree

        if root is None:
            xmlType = etree.Element("datatype")
        else: xmlType = etree.SubElement(root, "datatype")
        xmlType.text = self.name
        return xmlType

######################################################################
class UMLPrimitiveDataType(IUMLDataType):
    @property
    def id(self): return self.name
    def __repr__(self): return self.name

UMLInt       = UMLPrimitiveDataType('int')
UMLBoolean   = UMLPrimitiveDataType('boolean')
UMLNone      = UMLPrimitiveDataType('')
UMLChar      = UMLPrimitiveDataType('char')
UMLUndefined = UMLPrimitiveDataType('undefined')
UMLReal      = UMLPrimitiveDataType('real')

######################################################################
class UMLPackageableElement(IUMLElement):
    def __init__(self, scope, **args):
        if scope is not None \
                or (isinstance(scope, UMLElementRelativeName) and len(scope) !=0) \
                or isinstance(scope, UMLNamedElement):
            self._scope = scope
        super(UMLPackageableElement, self).__init__(**args)

    @property
    def scope(self):
        if self.__dict__.has_key('_scope') and self._scope is not None: 
            return self._scope
        else: return UMLElementRelativeName()

    @scope.setter
    def scope(self, new_scope):
        self._scope = new_scope

######################################################################
class UMLNamedPackageableElement(UMLPackageableElement, UMLNamedElement):
    def __init__(self, name, scope, subclasses = None, **args):
        self.packages    = []
        self.subclasses = [] if subclasses is None else subclasses
        # self.subclass = []
        super(UMLNamedPackageableElement, self).__init__(name=name, scope=scope, **args)

    def add_subclass(self, classId):
        self.subclasses.append(classId)

    def add_package(self, packageId):
        self.packages.append(packageId)

    @property
    def id(self):
        scopeId = self.scope.id
        return ".".join((scopeId, self.name)) if scopeId and len(scopeId) > 0 else self.name
        # return ".".join((self.scope.id, self.name)) 

    def rel_id(self, scope):
        scope_id = scope.id
        return '.'.join([scope_id, self.id]) if len(scope_id) > 0 else self.id

    @property
    def full_name(self):
        if self.__dict__.has_key('_scope') and self._scope.id is not None: 
            return self._scope.id + "." + self.name
        else: return self.name

    # def get(self, uml_relname):
    #     scope = max_scope
    #     scope_id, relname_id = scope.id, uml_relname.id
    #     item  = scope.get(uml_relname)
    #     if item:    return item
    #     else:       scope = scope.scope
    #     return None


######################################################################

class UMLPackage(UMLNamedPackageableElement): 
    def add_component(self, component):
        pass

    def __contains__(self, key):
        return False # @TODO implement check

    def __repr__(self):
        return str(self.full_name)

    def toXML(self, root = None, reference = False):
        from lxml import etree

        if root is None:
            xmlPackage = etree.Element("package")
        else: xmlPackage = etree.SubElement(root, "package")
        xmlPackage.set('name', self.full_name)
        xmlPackage.set('hrefId', self.id)
        return xmlPackage

######################################################################
class UMLTemplateableElement(UMLNamedPackageableElement):
    def __init__(self, name, scope, parameters, **args):
        if len(parameters) > 0: self._parameters = parameters
        super(UMLTemplateableElement, self).__init__(name = name, scope = scope)

    @property
    def parameters(self):
        if self.__dict__.has_key('_parameters') and self._parameters is not None: 
            return self._parameters
        else: return []

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


######################################################################
class UMLSimpleDataType(UMLTemplateableElement, IUMLDataType):
    def __init__(self, name, 
                 scope = None, 
                 parameters = [],):
        super(UMLSimpleDataType, self).__init__(name = name, 
                                                scope = scope, 
                                                parameters = parameters)

    def __repr__(self):
        parameters = ','.join(map(str,self.parameters))
        return '{self.full_name}{parameters}'.\
            format(self=self,
                   parameters = '' if len(parameters) == 0 else '<%s>' % parameters)

    def toXML(self, root = None, reference = False):

        from lxml import etree
        xmlType = IUMLDataType.toXML(self, root)
        if self.scope:
            xmlType.set("scope", self.scope.full_name)
        return xmlType

######################################################################
class UMLDataTypeDecorator(IUMLElement):
    def __init__(self, base, 
                 properties = [],
                 multiplicity = None):
        self.base         = base
        self.multiplicity = UMLMultiplicityStack() if multiplicity is None else multiplicity
        self._properties  = properties
        super(UMLDataTypeDecorator, self).__init__()

    @property
    def name(self): return self.base.name

    @property
    def scope(self): return self.base.scope

    def add_property(self, name):
        if not  self.__dict__.has_key('_properties') or self._properties is None: 
            self._properties = []
        self._properties.append(name)

    @property
    def properties(self):
        if self.__dict__.has_key('_properties') and self._properties is not None: 
            return self._properties
        else: return []

    def __repr__(self):
        strMulti = str(self.multiplicity)
        return r'{self.base}{multi}{properties}'.\
            format(self=self, multi = '[%s]' % strMulti if len(strMulti) > 0 else '',
                   properties = "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),)

    @property
    def composite(self):
        return len(self.multiplicity) == 0 or self.multiplicity[0].composite

    def toXML(self, root = None, reference = True):
        from lxml import etree
        if isinstance(self.base, UMLClass):
            xmlType = UMLSimpleDataType(self.base.name, self.base.scope).toXML(root)
            xmlType.set("hrefId", self.base.id)
        else: xmlType = self.base.toXML(root)

        if not self.composite:
            xmlType.set("multiplicity", str(self.multiplicity))

        return xmlType

######################################################################
class UMLClass(UMLNamedPackageableElement):
    """Unified (language independent) representation of class
    """
    def __init__(self, name, 
                 location = None, 
                 scope  = None,
                 methods  = [],
                 attribs  = [],
                 modifiers  = [],
                 subclasses = None,
                 parent   = None,):
        # Fill data
        self.location   = location

        self._modifiers = modifiers
        self.methods    = methods
        self.attributes = attribs

        # Fill dependencies 
        self.parent       = parent

        self.realizations = []
        self.usages       = []

        super(UMLClass, self).__init__(name = str(name), scope = scope, subclasses = subclasses)

    def add_attribute(self, attrib):
        self.attributes.append(attrib)
        # if attrib.is_utility: self._utility = False

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

    def add_realization(self, iface_id):
        self.realizations.append(iface_id)

    def add_usage(self, iface_id):
        self.usages.append(iface_id)

    # @property
    # def id(self):
    #     return self.name

    @property
    def modifiers(self):
        modifiers  = []
        if self.is_interface: modifiers.append('interface')
        if self.is_utility:   modifiers.append('utility')
        modifiers.extend(self._modifiers)
        return modifiers

    def has_modifiers(self):
        if self.is_interface:     return True
        if self.is_utility:       return True
        if len(self._modifiers): return True
        return False

    def add_modifier(self, modifier):
        self._modifiers.append(modifier)

    @property
    def is_interface(self):
        if len(self.attributes) > 0:
            return False
        for method in self.methods:
            if not method.is_destructor and not method.is_abstract: 
                return False
        return True

    @property
    def is_utility(self):
        for attrib in self.attributes:
            if not attrib.is_utility: return False
        for method in self.methods:
            if not method.is_destructor and not method.is_utility: return False
        
        return True

    def __str__(self):
        modifiers  = self.modifiers
        return "{line}\n{modifiers:^40}\n[{self.scope}]{self.name}\n{line}\n{attributes}\n{line}\n{methods}\n{line}".\
            format(self=self, line= chr(196)*40, #unicode('\x80abc', errors='replace')*
                   attributes = "\n".join(map(str,self.attributes)),
                   methods    = "\n".join(map(str,self.methods)),
                   modifiers  = "" if len(modifiers) == 0 else "<<%s>>"%",".join(modifiers))

    def methods_iter(self, visibility = '+'):
        """Iterate over the methods
        """
        for uml_method in self.methods:
            if uml_method.visibility[0] == visibility:
                yield (uml_method)

    def toXML(self, root = None, reference = False):
        if reference:
            xmlClass = UMLSimpleDataType(self.name, self.scope).toXML(root)
            xmlClass.set("hrefId", self.id)
        else:
            from lxml import etree

            modifiers  = self.modifiers

            if root is None:
                xmlClass = etree.Element("class")
            else: xmlClass = etree.SubElement(root, "class")
            xmlClass.text   = self.name
            xmlClass.set("utility", "yes" if self.is_utility else "no")
            if self.is_interface:
                xmlClass.set("interface", "yes")
            xmlModifs       = etree.SubElement(xmlClass, "modifiers")
            xmlModifs.text  = "" if len(modifiers) == 0 else ",".join(modifiers)

            if self.scope is not None:
                xmlClass.set("scope", self.scope.full_name)

            if len(self.location)>0:
                xmlClass.set("location", self.location)

            xmlAttribs      = etree.SubElement(xmlClass, "attributes")
            for attrib in self.attributes:
                xmlAttrib = attrib.toXML(xmlAttribs)

            xmlMethods      = etree.SubElement(xmlClass, "methods")
            for method in self.methods:
                xmlMethod = method.toXML(xmlMethods)

        return xmlClass

######################################################################
class UMLClassAttribute:
    def __init__(self, name, type, 
                 visibility, 
                 constant = False,
                 utility = False):
        self.name       = name
        self.type       = type
        self.visibility = visibility
        self._utility     = utility
        self.properties = []
        if constant: self.properties.append('readOnly') #friend, extern

    @property
    def is_utility(self):
        return self._utility

    def __str__(self):
        return " {utility}{self.visibility} {self.name}:{self.type}".\
            format(self=self, utility = 'u' if self._utility else ' ',)

    def toXML(self, root = None):
        from lxml import etree
        if root is None:
            createElem = lambda root, name: etree.Element(name)
        else: createElem = etree.SubElement

        xmlAttrib = createElem(root, "attribute",
                               visibility = self.visibility,)
        if self.is_utility:
            xmlAttrib.set("utility", "yes")
        if len(self.properties) > 0:
            xmlAttrib.set("properties", "{%s}"%",".join(self.properties))

        # @TODO move it to uml_diagram
        if self.__dict__.has_key('unfolding_level'):
            xmlAttrib.set('unfolding-level', str(self.unfolding_level))

        xmlAttrib.text  = self.name
        xmlType         = self.type.toXML(xmlAttrib)
        return xmlAttrib

######################################################################
class UMLClassMethod:
    def __init__(self, name, 
                 rtnType, parameters,
                 visibility,
                 abstract   = False,
                 utility    = False,
                 properties = []):
        self.name       = str(name)
        self.rtnType    = rtnType
        self.parameters = parameters
        self.visibility = visibility

        self.properties = properties

        self._abstract = abstract
        self._utility  = utility

    @property
    def is_constructor(self):
        return self.name == "<<create>>" 

    @property
    def is_destructor(self):
        return self.name == "<<destroy>>" 

    @property
    def is_abstract(self):
        return self._abstract


    @property
    def is_utility(self):
        return self._utility

    def __str__(self):
        return "{abstract}{utility}{self.visibility}{self.name}(){rtnType}{properties}".\
            format(self=self, 
                   abstract = 'a' if self._abstract else ' ',
                   utility  = 'u' if self._utility else ' ',
                   properties= "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),
                   rtnType  = "" if self.rtnType is None else ":%s" % self.rtnType)

    def toXML(self, root = None):
        from lxml import etree
        if root is None:
            createElem = lambda root, name: etree.Element(name)
        else: createElem = etree.SubElement

        xmlMethod = createElem(root, "method",
                               visibility = self.visibility,)
        if self.is_utility:
            xmlMethod.set("utility", "yes")
        if self.is_abstract:
            xmlMethod.set("abstract", "yes")

        xmlMethod.text  = self.name

        if len(self.properties) > 0:
            #print self.properties
            xmlMethod.set("properties", "{%s}"%",".join(self.properties))

        xmlRetType      = etree.SubElement(xmlMethod, 'datatype')
        xmlRetType.text = self.rtnType
        # if self.rtnType is not None:
        #     xmlRetType      = self.rtnType.toXML(xmlMethod)
        return xmlMethod

######################################################################
class UMLInterface(object):
    def __init__(self, name, 
                 scope    = None,
                 stereotypes = [],):
        # Extract data
        self.name     = str(name)
        self.scope    = scope
        self.stereotypes = stereotypes

    @property
    def id(self):
        return self.name

    def __str__(self):
        return r'{stereotypes}{self.scope}.{self.name}'.\
            format(self=self,
                   stereotypes = "<<%s>>"%",".join(self.stereotypes),)
