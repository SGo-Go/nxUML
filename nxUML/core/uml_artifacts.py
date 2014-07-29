#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_artifacts.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.

http://www.uml-diagrams.org/deployment-diagrams.html
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

import os

class UMLArtifact(object):
    def __init__(self, name, stereotype = None):
        self.name = name
        self.stereotype = stereotype

    def __str__(self):
        return "<<{self.stereotype}>> {self.name}".format(self=self)

    @property
    def id(self):
        return self.name

class UMLFile(UMLArtifact):
    def __init__(self, name, ext = '', folder = '', stereotype = None):
        self.ext    = ext
        self.folder = folder
        super(UMLFile, self).__init__(name, stereotype = 'file')

    @property
    def id(self):
        return self.full_name

    def remove_prefix(self, prefix):
        try:
            self.folder = os.path.relpath(self.folder, prefix)
        except: 
            self.local = False
            pass

    @property
    def full_name(self):
        return os.path.join(self.folder, self.name + self.ext)

class UMLSourceFile(UMLFile):
    def __init__(self, name, ext = '', folder = '', 
                 stereotype = 'source', local = False,
                 open_names = None):
        self.local = local
        self.open_names = [] if open_names is None else open_names
        super(UMLSourceFile, self).__init__(name, ext = ext, 
                                            folder = folder, stereotype = stereotype)

    

class UMLScriptFile(UMLSourceFile):
    def __init__(self, name, ext = '', folder = '', stereotype = 'script'):
        super(UMLScriptFile, self).__init__(name, ext = ext, 
                                            folder = folder, stereotype = stereotype)
class UMLFileReference(UMLFile): pass

class UMLSourceReference(UMLSourceFile): pass

from networkx import DiGraph
class UMLSourceFilesGraph(DiGraph):
    def __init__(self, source_prefix = ''):
        self.source_prefix = source_prefix
        self.source = {}

        super(UMLSourceFilesGraph, self).__init__()

    def make_id(self, uml_source):
        return uml_source.full_name

    # def make_id(self, filename):
    #     name = os.path.relpath(filename, self.source_prefix)

    def abspath(self, sourceId):
        return os.path.join(self.source_prefix, 
                            self.source[sourceId].full_name)

    # def successors(self, sourceId):
    #     if sourceId not in self:
    #         sourceId = os.path.relpath(sourceId, self.source_prefix)
    #     return super(UMLSourceFilesGraph, self).successors(sourceId)
        
    def add(self, uml_source, forced=False):
        idSource = self.make_id(uml_source)
        if forced or (idSource not in self):
            self.source[idSource] = uml_source
            self.add_node(idSource)
        return idSource

    # def add_link

    # def __getitem__(self, idSource):
    #     if isinstance(idSource, int):
    #         return self.sources[idSource]
    #     else:
    #         raise ValueError('Indexing type error: id = %s, type(id) = %s' % (idSource, type(idSource)))
