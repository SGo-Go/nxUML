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
        raise NotImplementedError('{0} elements are not identifiable'.format(type(self)))

######################################################################
class UMLNamedElement(IUMLElement):
    """An abstract UML element that may have a name. 
    The name is used for identification of the named element 
    within the namespaces in which it is defined or accessible. 
    """
    def __init__(self, name, **args):
        self.name = name

######################################################################
class UMLRedefinableElement(UMLNamedElement):
    """An abstract named element that, 
    when defined in the context of generalization of a classifier, 
    can be redefined more specifically or differently 
    in the context of another classifier that specializes the context classifier. 
    """
    @property
    def isLeaf(self):
        return True

######################################################################
class UMLPackageableElement(IUMLElement):
    """Container for named elements.
    """
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
class UMLNamespace(UMLPackageableElement, UMLNamedElement):
    """
    """
    def __init__(self, name, scope, subclasses = None, **args):
        self.packages    = []
        self.subclasses = [] if subclasses is None else subclasses
        # self.subclass = []
        super(UMLNamespace, self).__init__(name=name, scope=scope, **args)

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
