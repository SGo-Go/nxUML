#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
 Project       DoxyUML
 (c) copyright 2014
######################################################################
 @file         nxuml_agraph.py
 @author       Sergiy Gogolenko

 Note: lxml from http://www.lfd.uci.edu/~gohlke/pythonlibs/
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

######################################################################
#  
######################################################################

from networkx import DiGraph, MultiDiGraph, MultiGraph
from networkx.exception import NetworkXException, NetworkXError
# import networkx.convert as convert
# from copy import deepcopy
from sets import Set

from nxUML.core import *

class AGraphWriter(object):

    default_styles = {"node" : {
            'class'     : {
                'default'   : {'style' : 'filled', 
                               'fillcolor' : 'gray',  'shape' : 'box'},
                },
            'interface' : {'fontsize' : 10, 
                           'fontcolor' : 'black', 'shape' : 'plaintext'}
            },
                      "edge" : {
            "inherite" : {'style' : 'dashed', 'dir' : 'back', 
                          'arrowtail' : 'empty', 'arrowhead' : 'none'},
            "require"  : {"dir" : "forward", 
                          "arrowtail" : "empty", "arrowhead" : "tee"},
            "provide"  : {"dir" : "both", 
                          "arrowtail" : "odot",  "arrowhead" : "none"}
            }
                      }

    @classmethod
    def to_abigraph(self, uml_diag, styles = default_styles, type=None, max_label = 4, name2URL = None):
        """
        Converts graph to the graphvis format
        """
        graph = UMLAGraph(uml_diag, styles, # name2URL = name2URL, max_label = max_label,
                          )
        # for classCaller, classCallee, attribs in graph.edges_iter(data=True):
        #     if attribs['type'] == 'inheritance': mgraph.add_inheritance(classCaller, classCallee)
        #     elif attribs['type'] == 'brownie'  :
        #         mgraph.add_calls(classCaller, classCallee, 
        #                          graph[classCaller][classCallee]['call'] | \
        #                              graph[classCaller][classCallee]['notification'])

        from networkx import to_agraph
        return to_agraph(graph)

class UMLAGraph(MultiDiGraph):
    """
    Class of the graph
    """
    def __init__(self, uml_diag, styles, 
                 data=None, name='', file=None, **attr):
        """
        Constructor 
        """
        self.uml_diag   = uml_diag
        self.styles     = styles
        super(UMLAGraph, self).__init__(data=data,name=name,**attr)

        for uml_class in self.uml_diag:
            self.add_class(uml_class)

        for rel_name in self.uml_diag._relationships:
            self.add_relationship(rel_name)

    @classmethod
    def class2HTMLlabel(cls, uml_class, level = 3):
        """
        Convert UML class to a dictionary with node settings for graphviz
        @param uml_class   UML class to convert
        @param level       detalization level
        |     level     | Description                   |
        |-----------------------------------------------|
        |       0       | hide class                    |
        |       1       | details suppressed            |
        |       2       | analysis level details        |
        |       3       | implementation level details  |
        |       4       | maximum details               |
        @return dictionary with node settings for graphviz
        """
        from lxml import etree
        import os

        rawXmlClass = uml_class.toXML()
        xslt = etree.parse(os.path.join(os.path.dirname(__file__), 'styles' , "graphviz.xsl"))
        rawXmlClass.set('detalization-level', str(level))
        transform = etree.XSLT(xslt)
        xmlLabel  = transform(rawXmlClass)
        del rawXmlClass, transform
        return "<\n%s>" % etree.tostring(xmlLabel, pretty_print=True)

    def add_class(self, name):
        """
        Append node for the class involved in brownie interactions to the graph.
        """
        if name is not None: 
            if not self.has_node(name): 
                styles = dict(self.styles['node']['class']['default'])
                if self.styles['node']['class'].has_key('regex'):
                    for regexp,sty_re in \
                            self.styles['node']['class']['regex'].items():
                        if re.search(regexp.encode('ascii'), name) is not None:
                            styles.update(sty_re)
                self.add_node(name, label = self.class2HTMLlabel(self.uml_diag._classes[name]), shape="plaintext")
        return name

    def add_relationship(self, uml_relationship):
        """
        Append relationship between 2 classes to the graph.
        """
        if isinstance(uml_relationship, UMLGeneralization):
            style = self.styles['edge']['inherite']
            if uml_relationship.child.qualifier is not None:
                label = str(uml_relationship.child.qualifier)
            else: label = ''
            self.add_edge(uml_relationship.parent.name, 
                          uml_relationship.child.name, 
                          label = label, **style)
