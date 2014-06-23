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
    def to_abigraph(self, uml_pool, styles = default_styles, type=None, max_label = 4, name2URL = None):
        """
        Converts graph to the graphvis format
        """
        graph = UMLAGraph(uml_pool, styles, # name2URL = name2URL, max_label = max_label,
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
    def __init__(self, uml_pool, styles, # max_label = 4, name2URL = None,
                 data=None, name='', file=None, **attr):
        """
        Constructor 
        """
        self.uml_pool   = uml_pool
        self.styles     = styles
        # self.max_label  = max_label
        # self.name2URL   = name2URL
        #super(UMLAGraph, self)
        super(UMLAGraph, self).__init__(data=data,name=name,**attr)

        for uml_class in self.uml_pool:
            self.add_class(uml_class)

        for rel_name in self.uml_pool._relationships:
            self.add_relationship(rel_name)

    @classmethod
    def attribute2XMLlabel(cls, xml_root, uml_attrib, level = 1):
        from lxml import etree

        xmlAttrib = xml_root
        if uml_attrib.is_utility:
            xmlAttrib = etree.SubElement(xmlAttrib, "u")
        xmlAttrib.text = str(uml_attrib)

        if level ==2: fmtLabel = " {self.visibility} {self.name}:{self.type}"
        else: fmtLabel = " {self.visibility} {self.name}"
        xmlAttrib.text = fmtLabel.format(self=uml_attrib)

    @classmethod
    def method2XMLlabel(cls, xml_root, uml_method, level = 1):
        from lxml import etree

        xmlMethod = xml_root
        if uml_method.is_abstract:
            xmlMethod = etree.SubElement(xmlMethod, "i")
        if uml_method.is_utility:
            xmlMethod = etree.SubElement(xmlMethod, "u")

        if level ==2: fmtLabel = "{self.visibility}{self.name}(){rtnType}{properties}"
        else: fmtLabel = "{self.visibility}{self.name}()"
        xmlMethod.text = fmtLabel.\
            format(self=uml_method, 
                   properties= "" if len(uml_method.properties) == 0 \
                       else "{%s}"%",".join(uml_method.properties),
                   rtnType  = "" if uml_method.rtnType is None else ":%s" % uml_method.rtnType)

    @classmethod
    def class2HTMLlabel(cls, uml_class, level = 1):
        """
        Convert UML class to a dictionary with node settings for graphviz
        @param uml_class   UML class to convert
        @param level       detalization level
        |     level     | Description                   |
        |-----------------------------------------------|
        |       0       | details suppressed            |
        |       1       | analysis level details        |
        |       2       | implementation level details  |
        @return dictionary with node settings for graphviz
        """
        name = uml_class.name
        modifiers = ",".join(uml_class.modifiers)

        from lxml import etree

        # xmlRoot = etree.Element("font")
        # xmlRoot.set('point-size', '10.0')
        #xmlClass = etree.SubElement(xmlRoot, "table", border='0', cellborder='1', cellspacing='0', color = 'gray')
        xmlClass = etree.Element("table", border='0', cellborder='1', cellspacing='0', 
                                 title="herez",
                                 bgcolor = 'lightgray', # bgcolor = 'cyan:#ffff88', color = 'blue', #
                                 )
        xmlRow   = etree.SubElement(xmlClass, "tr")
        xmlSpot  = etree.SubElement(xmlRow, "td")
        if len(modifiers) > 0:
            xmlSpot.text = '<<%s>>'% modifiers
            br = etree.SubElement(xmlSpot, "br")
            # br.tail = name
        xmlName = etree.SubElement(xmlSpot, "b")
        xmlName = etree.SubElement(xmlName, "font")#, face="verdana", size='3', color='red'
        xmlName.text = name

        # if   level == 0:
        #     label = r"{modifiers}{name}".\
        #         format(name = name, modifiers = "" if len(modifiers) == 0 \
        #                    else r"<<%s>>\n"% modifiers)
        if level == 1:
            xmlRow   = etree.SubElement(xmlClass, "tr")
            # xmlRow   = etree.SubElement(xmlRow, "font")
            # xmlRow.set('point-size', '10.0')
            xmlSpot  = etree.SubElement(xmlRow, "td", align="left")

            for attrib in uml_class.attributes:
                xmlName = etree.SubElement(xmlSpot, "font")
                UMLAGraph.attribute2XMLlabel(xmlName, attrib)
                br = etree.SubElement(xmlSpot, "br", align="left")

            xmlSpot.text = ""

            xmlRow   = etree.SubElement(xmlClass, "tr")
            # xmlRow   = etree.SubElement(xmlRow, "font")
            # xmlRow.set('point-size', '10.0')
            xmlSpot  = etree.SubElement(xmlRow, "td", align="left")

            for method in uml_class.methods:
                xmlName = etree.SubElement(xmlSpot, "font")
                UMLAGraph.method2XMLlabel(xmlName, method)
                # xmlName.text = cls.attribute2HTMLlabel(method)
                br = etree.SubElement(xmlSpot, "br", align="left")

            xmlSpot.text = ""

        return "<\n%s>" % etree.tostring(xmlClass, pretty_print=True)

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
                            #break
                # if self.name2URL is not None:
                #     styles['URL'] = self.name2URL(name)
                self.add_node(name, label = self.class2HTMLlabel(self.uml_pool.Class[name]), shape="plaintext")#, **styles)
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
            self.add_edge(uml_relationship.parent.name, uml_relationship.child.name, 
                          label = label, **style)
