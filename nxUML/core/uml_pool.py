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
        # if len(self.key) == 1 and self.key[0] == 'int':
        #     return '*'
        # else:
        return "bind={bind}, key={key}".\
            format(bind="<<%s>>" % ",".join(self.bind),
                   key="%s"%",".join(map(lambda x: 'id:' + (x if type(x) is str else x.name), self.key)))

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
    def id(self):
        return self.name

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
            return self._scope + "." + self.name
        else: return self.name

    @property
    def scope(self):
        if self.__dict__.has_key('_scope') and self._scope is not None: 
            return self._scope #+ "."
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
        return r'{self.name}{parameters}{multiplicity} {properties} {self.qualifier}'.\
            format(self=self,
                   multiplicity = '' if self.composite else "[%s]" % self.multiplicity,
                   parameters= "" if len(self.parameters) == 0 else map(str, self.parameters),
                   properties= "" if len(self.properties) == 0 else "{%s}"%",".join(self.properties),)


    def toXML(self, root = None):
        from lxml import etree

        if root is None:
            xmlType = etree.Element("type")
        else: xmlType = etree.SubElement(root, "type")
        if not self.composite:
            xmlType.set("multiplicity", "[%s]" % self.multiplicity)
        xmlType.text = self.name
        return xmlType

######################################################################

class UMLClass(object):
    """
    Unified (language independent) representation of class
    """
    def __init__(self, name, 
                 location = None, 
                 package  = None,
                 methods  = [],
                 attribs  = [],
                 modifiers  = [],
                 subclasses = [],
                 parent   = None,):
        # Fill data
        self.name       = str(name)
        self.package    = package
        self.location   = location

        self._modifiers = modifiers
        self.methods    = methods
        self.attributes = attribs

        # Fill dependencies 
        self.parent       = parent
        self.subclasses   = []

        self.realizations = []
        self.usages       = []

    def add_subclass(self, name):
        self.subclasses.append(name)

    def add_attribute(self, attrib):
        self.attributes.append(attrib)
        #if attrib.is_utility: self._utility = False

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

    @property
    def id(self):
        return self.name

    @property
    def full_name(self):
        if self.__dict__.has_key('package') and self.package is not None: 
            return self.package + "." + self.name
        else: return self.name

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
        return "{line}\n{modifiers:^40}\n[{self.package}]{self.name}\n{line}\n{attributes}\n{line}\n{methods}\n{line}".\
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

    def toXML(self, root = None):
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

        if len(self.package)>0:
            xmlClass.set("package", self.package)

        if len(self.location)>0:
            xmlClass.set("location", self.location)

        xmlAttribs      = etree.SubElement(xmlClass, "attributes")
        for attrib in self.attributes:
            xmlAttrib = attrib.toXML(xmlAttribs)

        xmlMethods      = etree.SubElement(xmlClass, "methods")
        for method in self.methods:
            xmlMethod = method.toXML(xmlMethods)

        return xmlClass

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

        xmlRetType      = etree.SubElement(xmlMethod, 'type')
        xmlRetType.text = self.rtnType
        # if self.rtnType is not None:
        #     xmlRetType      = rtnType.toXML(xmlMethod)
        return xmlMethod

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

# class UMLRealizationPort:
#     def __init__(self, interface):
#         self.name       = str(name)
#         self.stereotypes= stereotypes

# class UMLUsagePort:
#     def __init__(self, name, 
#                  stereotypes = [],
#                  provider = None):
#         self.name       = str(name)
#         self.stereotypes= stereotypes
#         self.provider   = None

######################################################################
# Relationships
######################################################################

class UMLRelationship(object):
    def __init__(self):
        pass

class UMLBinaryRelationship(UMLRelationship):
    def __init__(self, source, destination):
        self.source      = source
        self.destination = destination

    def __str__(self):
        return "{self.source.name}->{self.destination.name}".format(self=self)

class UMLNaryRelationship(UMLRelationship):
    def __init__(self, *classifiers):
        self.classifiers = classifiers

    def __str__(self):
        return "{{{0}}}".format(
            ','.join(map(lambda x: x.name, self.classifiers)))


######################################################################
class UMLRealization(UMLBinaryRelationship):
    def __init__(self, cls, iface):
        super(UMLRealization, self).__init__(iface, cls)

    def __str__(self):
        return "{self.source.name}-(){self.destination.name}".format(self=self)

class UMLUsage(UMLBinaryRelationship):
    def __init__(self, iface, cls):
        super(UMLUsage, self).__init__(cls, iface)

    def __str__(self):
        return "{self.source.name})-{self.destination.name}".format(self=self)

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
    def __init__(self, multiplicity = '', properties = [], qualifier = None):
        self.multiplicity = multiplicity
        self.properties   = properties
        #self.qualifier    = qualifier

class UMLAggregation(UMLBinaryRelationship):
    def __init__(self, whole, part, attribute = None, visibility = '  '):
        if attribute is not None:
            self.visibility = attribute.visibility
            self.role = attribute.name
            self.composite = attribute.type.composite
            self.qualifier = attribute.type.qualifier
            properties   = attribute.type.properties
            if len(self.qualifier) > 0:
                multiplicity =  '*'
                if attribute.type.reference:
                    properties = ['&'] + properties
                elif attribute.type.pointer:
                    properties = ['*'] + properties
            else:
                multiplicity = attribute.type.multiplicity
            self.part_detalization = UMLDetalization(
                multiplicity = multiplicity, 
                #, qualifier = qualifier
                properties = properties)
        super(UMLAggregation, self).__init__(whole, part)

    @property
    def full_role(self):
        return "{self.visibility}{self.role}\n{self.qualifier}".format(self=self)

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

######################################################################

class UMLGeneralization(UMLBinaryRelationship):
    def __init__(self, parent, child, visibility = '  '):
        self.visibility = visibility
        super(UMLGeneralization, self).__init__(parent, child)

    @property
    def child(self):
        return self.destination

    @child.setter
    def child(self, child_class):
        self.destination = child_class

    @property
    def parent(self):
        return self.source

    @parent.setter
    def parent(self, parent_class):
        self.source = parent_class

    def __str__(self):
        return "{self.parent.name}<-[{self.visibility}]-{self.child.name}".format(self=self)

######################################################################

class UMLPool(object):
    """
    Pool of classes with relationships between them
    """
    def __init__(self, data=None, name='', file=None, **attr):
        """
        Constructor 
        """
        self.Class           = {}
        self.Interface       = {}
        self._relationships  = []

    def add_class(self, uml_class):
        self.Class[uml_class.id] = uml_class

    def add_interface(self, uml_iface):
        self.Interface[uml_iface.id] = uml_iface

    def add_relationship(self, uml_relationship):
        self._relationships.append(uml_relationship)

    def __str__(self):
        """String representation of information about the pool.

        @return The list of the classes in the pool with count of relationship.
        """
        #return 'Pool of {nclasses} classes with {nrelations} relationships: {classes}'.
        return 'Pool of {nclasses} class(es) with {nrelations} relationship(s)'.\
            format(nrelations = len(self._relationships), 
                   nclasses = len(self.Class.keys()),
                   classes = ', '.join(self.Class.keys()))

    def __contains__(self, cls):
        """Check if the given name is a name of class from pool
        Use the expression 'cls in uml_pool'.
        
        @param cls name of class to check
        @return True if cls is a class from pool, False otherwise.
        """
        return self.Class.has_key(cls)

    def __len__(self):
        """Number of classes in pool.
        Use the expression `len(pool)`

        @return the number of classes.
        """
        return len(self.Class)

    def __iter__(self):
        """Iterate over the classes.
        """
        return iter(self.Class)

    def classes_iter(self, package = ''):
        """Iterate over the classes from the given package.
        """
        for cls_name, uml_class in self.Classes.items():
            if len(package) == 0:
                yield (uml_class)
            elif uml_class.package == package:
                yield (uml_class)

    def relationships_iter(self):
        return iter(self._relationships)

    def generalizations_iter(self, parents = None, childs = None):
        for relationship in self.relationships_iter():
            if isinstance(relationship, UMLGeneralization): 
                yield (relationship)
