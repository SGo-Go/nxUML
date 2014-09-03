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
        while isinstance(scope, UMLNamespace):
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
    """Abstract root UML metaclass
    """
    @property
    def id(self):
        raise NotImplementedError('{0} objects are not identifiable'.format(type(self)))

    @property
    def tag(self):
        """Specifies XML tag for the serialized instance of the object 
        """
        raise NotImplementedError('{0} objects have no tag'.format(type(self)))

    def toXML(self, root = None, reference = False, **args):
        if   self.tag is None: 
            xmlElement = root
        elif reference:
            from nxUML.core.uml_datatype import UMLDataTypeStub

            xmlElement = UMLDataTypeStub(self.name, self.scope).toXML(root = root, reference = False)
            xmlElement.set("hrefId", self.id)
            xmlElement.set("type", self.tag)
            # if isinstance(self, UMLPackageableElement):
            #     from lxml import etree
            #     print '-', self.scope.full_name
            #     print '-', self.__dict__
            #     print '-', etree.tostring(xmlElement, pretty_print=True)
        else:
            from lxml import etree

            if root is None:
                xmlElement = etree.Element(self.tag)
            else: xmlElement = etree.SubElement(root, self.tag)

        return xmlElement

######################################################################
class UMLNamedElement(IUMLElement):
    """An abstract UML element that may have a name. 
    The name is used for identification of the named element 
    within the namespaces in which it is defined or accessible. 
    """
    def __init__(self, name, **args):
        self.name = name

    def toXML(self, root = None, reference = False, **args):
        xmlElement = super(UMLNamedElement, self).toXML(root = root, reference = reference, **args)
        xmlElement.text = self.name
        return xmlElement

######################################################################
class UMLRedefinableElement(UMLNamedElement):
    """An abstract named element that, 
    when defined in the context of generalization of a classifier, 
    can be redefined more specifically or differently 
    in the context of another classifier that specializes the context classifier. 
    """
    @property
    def isLeaf(self):
        """Indicates whether it is possible to redefine the element in subclasses. 
        
        If the value is true, then it is not possible to further redefine the element. 
        E.g., in *Java* language it corresponds to the `final` class, 
        in *C#* - to the `sealed` class.
        """
        return True

######################################################################
class UMLPackageableElement(IUMLElement):
    """An element that can be embedded into namespace.
    """
    def __init__(self, scope, **args):
        # if scope is not None \
        #         or (isinstance(scope, UMLElementRelativeName) and len(scope) !=0) \
        #         or (isinstance(scope, UMLNamespace)):
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

    def toXML(self, root = None, reference = False, **args):
        xmlElement = super(UMLPackageableElement, self).toXML(root = root, reference = reference, **args)
        # if isinstance(self, UMLPackageableElement):
        #     from lxml import etree
        #     print '!', self.scope.full_name
        #     print '-', etree.tostring(xmlElement, pretty_print=True)

        scope = self.scope
        if scope is not None and (isinstance(scope, UMLNamespace) and not scope.isRoot):
            xmlElement.set("scope", scope.full_name)
        return xmlElement

######################################################################
class UMLNamespace(UMLPackageableElement, UMLNamedElement):
    """Container for named elements.
    """
    def __init__(self, name, scope, named_elements = None, noname_elements = None, **args):
        self.named_elements  = {} if  named_elements is None else named_elements
        self.noname_elements = {} if noname_elements is None else noname_elements
        super(UMLNamespace, self).__init__(name=name, scope=scope, **args)

    @property
    def isRoot(self): return False

    def add(self, uml_packageable_element):
        if isinstance(uml_packageable_element, UMLNamedElement):
            self.named_elements[uml_packageable_element.name] = uml_packageable_element
        elif uml_packageable_element is not None:
            raise TypeError('Non-packagebla element {0} is added as packageable'.format(type(uml_packageable_element)))

    def __getitem__(self, name):
        return self.named_elements[name]

    def classes_iter(self, scope = ''):
        """Iterate over the classes from the given namespace.
        """
        from nxUML.core.uml_class import UMLClass

        for uml_class in self.named_elements.values():
            if isinstance(uml_class, UMLClass):
                yield (uml_class)

    def packages_iter(self, scope = ''):
        """Iterate over the packages from the given namespace.
        """
        from nxUML.core.uml_package import UMLPackage

        for uml_package in self.named_elements.values():
            if isinstance(uml_package, UMLPackage):
                yield (uml_package)

    def __iter__(self):
        """Iterate over the namespaces.
        """
        for uml_namespace in self.named_elements.values():
            if isinstance(uml_namespace, UMLNamespace):
                yield (uml_namespace)

    @property
    def id(self):
        scopeId = self.scope.id
        return ".".join((scopeId, self.name)) if scopeId and len(scopeId) > 0 else self.name

    def rel_id(self, scope):
        scope_id = scope.id
        return '.'.join([scope_id, self.id]) if len(scope_id) > 0 else self.id


    def get(self, uml_path):
        from nxUML.core.uml_datatype    import UMLDataTypeStub

        if isinstance(uml_path, UMLDataTypeStub):
            uml_type_path = list(uml_path.scope) + [uml_path.name]
            uml_anchor = self
            for name in uml_type_path:
                if uml_anchor.named_elements.has_key(name):
                    uml_anchor = uml_anchor.named_elements[name]
                else: return None
            return uml_anchor
        else:
            raise

    @property
    def full_name(self):
        if self.__dict__.has_key('_scope') and self._scope.id is not None: 
            return self._scope.id + "." + self.name
        else: return self.name

    def toXML(self, root = None, reference = False, **args):
        xmlElement = UMLNamedElement.toXML(self, root = root, reference = reference, **args)

        # xmlElement = super(UMLNamespace, self).toXML(root = root, reference = reference, **args)
        if not reference:
            if len(self.named_elements) > 0:
                from lxml import etree
                xmlNestedNames = etree.SubElement(xmlElement, "inner")
                for named_element in self.named_elements.values():
                    named_element.toXML(root = xmlNestedNames, reference = True)
        return xmlElement

######################################################################
class UMLTemplateableElement(UMLNamespace):
    """An element that can optionally be defined 
    as a template or bound to other templates.
    """
    def __init__(self, name, scope, parameters, **args):
        if len(parameters) > 0: self._parameters = parameters
        super(UMLTemplateableElement, self).__init__(name = name, scope = scope)

    @property
    def parameters(self):
        if self.__dict__.has_key('_parameters') and self._parameters is not None: 
            return self._parameters
        else: return []

######################################################################
class UMLRootNamespace(UMLNamespace):
    def __init__(self):
        super(UMLRootNamespace, self).__init__(name='', scope=UMLElementRelativeName([]))

    @property
    def isRoot(self): return True
