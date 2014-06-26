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

    default_styles = {
        "node" : {
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
            "aggregate" : {'style' : 'dashed', 'dir' : 'back', 
                           'arrowtail' : 'empty', 'arrowhead' : 'none'},
            "require"  : {"dir" : "forward", 
                          "arrowtail" : "empty", "arrowhead" : "tee"},
            "provide"  : {"dir" : "both", 
                          "arrowtail" : "odot",  "arrowhead" : "none"}
            }
        }

    default_styles = {
        "edge" : {
            UMLGeneralization : {'style' : 'dashed', 'dir' : 'back', 
                                 'arrowtail' : 'empty', 'arrowhead' : 'none'},
            UMLAggregation : {'style' : 'solid', 'dir' : 'back', 
                              'arrowtail' : 'diamond', 'arrowhead' : 'none'},
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

        from lxml import etree
        import os
        xslt = etree.parse(os.path.join(os.path.dirname(__file__), 'styles' , "graphviz.xsl"))
        self.transform = etree.XSLT(xslt)

        xmlDiag = self.uml_diag.toXML()
        for uml_class in self.uml_diag:
            self.add_class(uml_class, xmlDiag)

        for classFrom, classTo, data in self.uml_diag.edges_iter(data=True):
            uml_rel = data['data']
            self.add_relationship(uml_rel)

    def add_class(self, name, xmlDiag):
        """
        Append node for the class involved in brownie interactions to the graph.
        Convert UML class to a dictionary with node settings for graphviz
        @param uml_class   UML class to convert
        """
        if name is not None: 
            if not self.has_node(name): 
                from lxml import etree

                rawXmlClass = xmlDiag.xpath('//diagram/classes/class[text()="%s"]' % name)[0]
                xmlLabel  = self.transform(rawXmlClass)
                #if name == 'CMapCtrlCoding':print etree.tostring(rawXmlClass, pretty_print=True)
                label = "<\n%s>" % etree.tostring(xmlLabel, pretty_print=True)
                del rawXmlClass, xmlLabel
                self.add_node(name, label = label, shape="plaintext")
        return name

    def add_relationship(self, uml_relationship):
        """
        Append relationship between 2 classes to the graph.
        """
        style = dict(self.styles['edge'][type(uml_relationship)].items())
        if isinstance(uml_relationship, UMLGeneralization):
            if uml_relationship.child.qualifier is not None:
                style['label'] = str(uml_relationship.child.qualifier)
            else: style['label'] = ''
        elif isinstance(uml_relationship, UMLAggregation):
            style['label'] = uml_relationship.full_role
            style['taillabel'] = '  1'
            style['headlabel'] = uml_relationship.part_detalization.multiplicity
            if uml_relationship.shared: 
                style['arrowtail'] = 'o' + style['arrowtail']
        self.add_edge(uml_relationship.source.id, 
                      uml_relationship.destination.id, 
                      **style)
