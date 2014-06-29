#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         brownie_parser.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.parser import CppTextParser, CppTypeParser
from nxUML.core import UMLClass, UMLInterface

class UMLBrownieInterface(UMLInterface):
    def __init__(self, name, 
                 scope    = None,
                 stereotypes = [],):
        # if len(stereotypes) == 1:
        #     name = name[:-len(stereotypes[0])]
        super(UMLBrownieInterface, self).__init__(name, scope, stereotypes)

    @classmethod
    def make_id(self, name, scope, stereotypes):
        return name if scope is None else scope + '.' + name

    @property
    def id(self):
        return self.make_id(self.name, self.scope, self.stereotypes)

    def __str__(self):
        stereotype = self.stereotypes[0]
        name = self.name[:-len(stereotype)]
        return "<<{stereotype}>>{name}".\
            format(self=self, 
                   stereotype = stereotype, name = name)

class UMLBrownieCall(UMLBrownieInterface):
    def __init__(self, name, 
                 scope         = None,
                 stereotypes   = [],
                 argument_type = None,
                 result_type   = None,
                 error_type    = None,
                 value_type    = None,
                 **kwargs):
        # if len(stereotypes) == 1:
        #     name = name[:-len(stereotypes[0])]
        self.argument_type = argument_type
        self.result_type   = result_type
        self.error_type    = error_type
        self.value_type    = value_type
        super(UMLBrownieInterface, self).__init__(name, scope, stereotypes)

    def __str__(self):
        stereotype = self.stereotypes[0]
        name = self.name[:-len(stereotype)]
        return "<<{stereotype}>>{name}({self.argument_type}):{self.result_type}/err:{self.error_type}/".\
            format(self=self, 
                   stereotype = stereotype, name = name)

class BrownieTypeParser(CppTypeParser):
    specifier_types = {
        # brownie::asynch::
        'ServiceCallable'       : 'ServiceCallable',
        'LocalCallable'         : 'LocalCallable',
        'LocalCallback'         : 'LocalCallback',
        }

    # @classmethod
    # def parse_from_pointer(cls, strType, ptr):

class BrownieTextParser(CppTextParser):
    TypeParser = BrownieTypeParser

    brownie_interface_stereotypes = {
        'ConcreteNotification'  : 'brownie.notification',
        'ConcreteOperationCall' : 'brownie.call',
        'FormalNotification'    : 'brownie.notification',
        'FormalOperationCall'   : 'brownie.call',
        }

    @classmethod
    def parse(cls, filename, uml_pool = None):
        return super(BrownieTextParser,cls).parse(filename, uml_pool)

    @classmethod
    def handle_attribute(cls, uml_class, **kwargs):
        super(BrownieTextParser,cls).handle_attribute(uml_class, **kwargs)

    @classmethod
    def handle_method(cls, uml_class, **kwargs):
        name = kwargs['name']
        if name in ('onStatus',
                    'onDenotification',
                    'onErrorStatus',
                    'handleDenotification',
                    'handleNotification'): 
            pass
        elif name in ('handleCall',
                      'onError',
                      'onResult'):
            pass
        else:
            super(BrownieTextParser,cls).handle_method(uml_class, **kwargs)

    @classmethod
    def handle_class(cls, uml_pool, **kwargs):
        if kwargs['parent'] is None:
            super(BrownieTextParser,cls).handle_class(uml_pool, **kwargs)

    @classmethod
    def handle_generalization(cls, uml_pool, **kwargs):
        parent = cls.TypeParser.parse(kwargs['parent'])
        child  = cls.TypeParser.parse(kwargs['child'])
        if parent.name == child.name:
            for prop in ('ServiceCallable', 'LocalCallable', 'LocalCallback'):
                if prop in parent.properties: 
                    uml_pool.Class[child.name].add_modifier(prop)
        else:
            super(BrownieTextParser,cls).handle_generalization(uml_pool,**kwargs)
        del parent, child

    @classmethod
    def handle_typedef(cls, uml_pool, uml_holder, **kwargs):
        if kwargs['visibility'] == 'public' and isinstance(uml_holder, UMLClass):
            # print kwargs['name'], kwargs['visibility']
            uml_type = cls.TypeParser.parse(kwargs['type'])
            if uml_type.name in ('ConcreteNotification', 'ConcreteOperationCall'):
                if len(uml_type.parameters) > 1:
                    data = uml_type.parameters[1].id
                else: data = None
                provider = uml_type.parameters[0].scope
                if '.' in provider:
                    provider = provider.split('.')[-1]
                cls.handle_brownie_usage(uml_pool, uml_holder, 
                                         name = uml_type.parameters[0].name, 
                                         provider = provider, 
                                         stereotype = cls.brownie_interface_stereotypes[uml_type.name],
                                         local_id = kwargs['name'], 
                                         data = data)
            elif uml_type.name in ('FormalNotification', 'FormalOperationCall'):
                if   uml_type.name == 'FormalNotification':
                    result_type  = None
                    error_type   = None

                    value_type   = uml_type.parameters[0].id
                    if len(uml_type.parameters) > 1:
                        argument_type = uml_type.parameters[1].id
                    else: argument_type = 'Void'
                elif uml_type.name == 'FormalOperationCall':
                    value_type    = None

                    argument_type = uml_type.parameters[0].id
                    result_type = uml_type.parameters[1].id \
                        if len(uml_type.parameters) > 1 else None
                    error_type = uml_type.parameters[2].id \
                        if len(uml_type.parameters) > 2 else None

                stereotype = cls.brownie_interface_stereotypes[uml_type.name]
                cls.handle_brownie_realization(uml_pool, uml_holder, 
                                               name = kwargs['name'], 
                                               stereotype = stereotype,
                                               argument_type = argument_type,
                                               result_type   = result_type,
                                               error_type    = error_type,
                                               value_type    = value_type,
                                             )
            else:
                super(BrownieTextParser,cls).handle_typedef(uml_pool, uml_holder, **kwargs)
            del uml_type
        else:
            super(BrownieTextParser,cls).handle_typedef(uml_pool, uml_holder, **kwargs)

    @classmethod
    def create_brownie_interface(cls, name = None, scope = None, stereotype = None, **kwargs):
        if stereotype == 'call':
            uml_iface = UMLBrownieCall(name, scope = scope, stereotypes = (stereotype,),
                                       **kwargs)
        else:
            uml_iface = UMLBrownieInterface(name, 
                                            scope = scope,
                                            stereotypes = (stereotype,))
        return uml_iface
        

    @classmethod
    def handle_brownie_realization(cls, uml_pool, uml_class, **kwargs):
        uml_iface = cls.create_brownie_interface(scope = uml_class.id, **kwargs)
        uml_pool.add_interface(uml_iface)
        uml_realization = uml_iface.id
        # print uml_class.id, uml_realization, uml_iface
        uml_class.add_realization(uml_realization)

    @classmethod
    def handle_brownie_usage(cls, uml_pool, uml_class, **kwargs):
        uml_usage = UMLBrownieInterface.make_id(kwargs['name'], kwargs['provider'], kwargs['stereotype'])
        # print uml_class.id, uml_usage
        uml_class.add_usage(uml_usage)

