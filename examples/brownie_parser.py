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

    @classmethod
    def handle_attribute(cls, uml_class, **kwargs):
        # name = kwargs['name']
        # if name in ('onStatus',
        #             'onDenotification',
        #             'onErrorStatus',
        #             'handleDenotification',
        #             'handleNotification'): 
        #     pass
        # elif name in ('handleCall',
        #               'onError',
        #               'onResult'):
        #     pass
        # else:
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
            super(BrownieTextParser,cls).handle_class(None, **kwargs)


    @classmethod
    def handle_generalization(cls, uml_pool, **kwargs):
        parent = cls.TypeParser.parse(kwargs['parent'])
        child  = cls.TypeParser.parse(kwargs['child'])
        if parent.name == child.name:
            for prop in ('ServiceCallable', 'LocalCallable', 'LocalCallback'):
                if prop in parent.properties: 
                    print prop, child.name #uml_pool.classes[child.name].add_modifier(prop)
        else:
            super(BrownieTextParser,cls).handle_generalization(uml_pool,**kwargs)
        del parent, child
