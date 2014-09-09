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
from nxUML.core   import UMLClass
from brownie_uml  import *

class BrownieTypeParser(CppTypeParser): pass
#     specifier_types = {
#         # brownie::asynch::
#         'ServiceCallable'       : 'ServiceCallable',
#         'LocalCallable'         : 'LocalCallable',
#         'LocalCallback'         : 'LocalCallback',
#         }

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
    def parse(cls, filename, uml_pool = None, **kwargs):
        return super(BrownieTextParser,cls).parse(filename, uml_pool, **kwargs)

    @classmethod
    def handle_attribute(cls, uml_class, **kwargs):
        super(BrownieTextParser,cls).handle_attribute(uml_class, **kwargs)

    @classmethod
    def handle_operation(cls, uml_class, **kwargs):
        name = kwargs['name']
        if name in ('onStatus',
                    'onDenotification',
                    'onErrorStatus',
                    'handleDenotification',
                    'handleNotification',
                    'onStatus',
                    ): 
            pass
        elif name in (
                      'handleSessionNotification',
                      'handleNotificationStatus',
                      ): 
            # if 'ServiceCallable' in uml_class.stereotypes:
            #     print uml_class.name, name
            pass
        elif name in ('handleCall',
                      'onError',
                      'onResult'):
            pass
        else:
            return super(BrownieTextParser,cls).handle_operation(uml_class, **kwargs)

    # @classmethod
    # def handle_class(cls, uml_pool, **data):
    #     for iface in uml_pool.Interface.values():
    #         if iface.use_type(data['name'], data['parent']):
    #             return None

    @classmethod
    def handle_generalization(cls, uml_pool, child, parent, **kwargs):
        if parent.name in ('ServiceCallable', 'LocalCallable', 'LocalCallback') \
                and len(parent.parameters) > 0 \
                and parent.parameters[0].base.name == child.name:
            # print parent.name, parent.parameters[0].base
            child.add_stereotype(BrownieProfile[parent.name].application(target=parent.parameters[0]))
            return None
        else:
            return super(BrownieTextParser,cls).handle_generalization(uml_pool, child, parent,**kwargs)

    @classmethod
    def handle_typedef(cls, uml_pool, uml_namespace, **data):
        if isinstance(uml_namespace, UMLClass): #data['visibility'] == 'public' and 
            uml_type = cls.TypeParser.parse(data['type']).base
            if uml_type.name in ('ConcreteNotification', 'ConcreteOperationCall'):
                cls.handle_brownie_usage(uml_pool, uml_namespace, 
                                         uml_iface = uml_type.parameters[0].base,
                                         type      = uml_type.name,
                                         data_type = uml_type.parameters[1].base.id \
                                             if len(uml_type.parameters) > 1 else UMLNone,
                                         visibility = data['visibility'])
            elif uml_type.name in ('FormalNotification', 'FormalOperationCall'):
                if uml_type.name == 'FormalNotification':
                    uml_iface = cls.handle_brownie_notification \
                        (uml_pool, uml_namespace, 
                         value_type    = uml_type.parameters[0],
                         argument_type = uml_type.parameters[1] \
                             if len(uml_type.parameters) > 1 else UMLNone, **data)
                elif uml_type.name == 'FormalOperationCall':
                    uml_iface = cls.handle_brownie_call \
                        (uml_pool, uml_namespace, 
                         argument_type = uml_type.parameters[0],
                         result_type = uml_type.parameters[1] \
                             if len(uml_type.parameters) > 1 else UMLNone,
                         error_type = uml_type.parameters[2] \
                             if len(uml_type.parameters) > 2 else UMLNone, **data)

                if uml_iface is not None:
                    cls.handle_brownie_realization(uml_pool, uml_namespace, uml_iface,
                                                   type      = uml_type.name, 
                                                   visibility = data['visibility'])
            else:
                return super(BrownieTextParser,cls).handle_typedef(uml_pool, uml_namespace, **data)
            del uml_type
        else:
            return super(BrownieTextParser,cls).handle_typedef(uml_pool, uml_namespace, **data)

    @classmethod
    def handle_brownie_notification(cls, uml_pool, uml_namespace, name = '', 
                                    value_type = UMLNone, argument_type = UMLNone, **data):
        uml_iface = UMLBrownieNotification(name, uml_namespace, 
                                           value_type    = value_type,
                                           argument_type = argument_type,
                                           visibility = cls.visibility_types[data['visibility']], #data['visibility'], #
                                           )
        uml_namespace.add(uml_iface)
        return uml_iface

    @classmethod
    def handle_brownie_call(cls, uml_pool, uml_namespace, name = '', 
                            argument_type = UMLNone, result_type = UMLNone, 
                            error_type = UMLNone, **data):
        uml_iface = UMLBrownieCall(name, uml_namespace, 
                                   argument_type = argument_type, 
                                   result_type   = result_type,
                                   error_type    = error_type,
                                   visibility    = cls.visibility_types[data['visibility']], #data['visibility'], #
                                   )
        uml_namespace.add(uml_iface)
        return uml_iface

    @classmethod
    def handle_brownie_realization(cls, uml_pool, uml_classifier, uml_iface, **data):
        uml_relationship = UMLBrownieRealization(uml_classifier, uml_iface, 
                                                 visibility = cls.visibility_types[data['visibility']], #data['visibility'], #
                                                 type       = data['type'])
        uml_classifier.add_relationship(uml_relationship)
        return uml_relationship

    @classmethod
    def handle_brownie_usage(cls, uml_pool, uml_classifier, uml_iface, **data):
        uml_relationship = UMLBrownieUsage(uml_classifier, uml_iface, 
                                           visibility = cls.visibility_types[data['visibility']], #data['visibility'], #
                                           type = data['type'])
        uml_classifier.add_relationship(uml_relationship)
        return uml_relationship
