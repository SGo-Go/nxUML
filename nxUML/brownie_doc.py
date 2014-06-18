#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
 Project       DoxyUML
 (c) copyright 2014
######################################################################
 @file         brownie_doc.py
 @author       Sergiy Gogolenko

 This library is intended to analyse C++ codes with asynchronous
 calls and notifications.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

import re, os

######################################################################

reCppId         = "[a-zA-Z_][a-zA-Z0-9_]*"
reCppType       = r"{reId}\s*(&|\*)?".format(reId=reCppId)
reOperationCall = r"ConcreteOperationCall"
reNotification  = r"ConcreteNotification"

formatTeXitem   = r"\itemBrowny{{{call}}}{{{callback}}}{{{callable}}}{{{namespace}}}{{}}"

######################################################################

def findBrownieDefs(lines, defs_type = 'call'):
    """
    Parses and extract definitions for *brownie* 
    calls and notifications from the C++ header.
    @comment Deprivated function
    
    @param lines      C++ codes with callback classes (LocalCallback)
    @param defs_type  Type of definitions ('call' or 'notification')
    @return list of definitions
    """
    reTemplate = {'call'         : reOperationCall,
                  'notification' : reNotification
                  }[defs_type]
    reCallbackDef   = re.compile(\
        r"brownie::asynch::LocalCallback<({reCppId})>".format(reCppId=reCppId))
    reBrownieTypedefs = \
        r"{reTemplate}<(({reCppId}::\s*)*)({reCppId})::\s*({reCppId})\s*(, {reCppType}\s*)?\s*>"\
        .format(reTemplate = reTemplate,
                reCppId    = reCppId,
                reCppType  = reCppType)
    reCallDef = re.compile(reBrownieTypedefs)

    lstMatches = []
    callbackName = ""
    for i in xrange(len(lines)):
        line = lines[i]
        mCallbackName = re.search(reCallbackDef, line) 
        if mCallbackName is not None: callbackName = mCallbackName.group(1)
        if re.search(reTemplate, line) is not None:
            if i+1 < len(lines) : line += lines[i+1] # for multiline (2 lines only supported)
            line = line.replace("\n",' ')
            m = reCallDef.search(line)
            if m is not None:
                callNamespace, callableName, callName = m.group(1), m.group(3), m.group(4)
                callName = callName[:-len(defs_type)]
                lstMatches.append((callbackName, callableName, callName, callNamespace))
    return lstMatches

def browniDefs2TeX(lst_defs):
    """
    Prints definitions for *brownie* calls and notifications in TeX format.
    @comment Deprivated function

    @param lst_defs   list of definitions
    @return string with definitions list in TeX format
    """
    result = ""
    for callbackName, callableName, callName, callNamespace in lst_defs:
        result += formatTeXitem.format(
            call      = callName, 
            callback  = callbackName, 
            callable  = callableName,
            namespace = callNamespace) + "\n"
    return result


######################################################################
#  RegEx list for brownie
######################################################################
reBrownieConcreteTemplate = r"Concrete(OperationCall|Notification)"
reBrownieFormalTemplate   = r"Formal(OperationCall|Notification)"
template2callType = lambda defs_type: {'OperationCall': 'call',
                                       'Notification' : 'notification'
                                       }[defs_type]

reBrownieConcreteDefs = \
    r"{reTemplate}<(({reCppId}::\s*)*)({reCppId})::\s*({reCppId})\s*(, {reCppType}\s*)?\s*>"\
    .format(reTemplate = reBrownieConcreteTemplate,
            reCppId    = reCppId,
            reCppType  = reCppType)
def sortDefConcrete(mtch, cls): 
    return mtch.group(1), mtch.group(5), "", cls, mtch.group(2), mtch.group(4)
#sortDefConcrete = lambda mtch: mtch.group(1), mtch.group(4), mtch.group(5), "", mtch.group(2)
reCallbackDef   = re.compile(\
    r"brownie::asynch::LocalCallback<({reCppId})>".format(reCppId=reCppId))

######################################################################
#  Parsing codes
######################################################################

def parseBrownieDefs(graph, f):
    """
    Parses definitions for *brownie* interactions
    (calls and notifications) from the C++ header
    and extracts this information into the graph.
    
    @param graph  Graph class
    @param f      handle of file with C++ codes that have *brownie* definetions (LocalCallback/LocalCallable)
    @return list of definitions
    """
    code_lines = f.readlines()
    reCallDef = re.compile(reBrownieConcreteDefs)

    lstMatches = []
    callbackName = ""
    for i in xrange(len(code_lines)):
        line = code_lines[i]
        mCallbackName = re.search(reCallbackDef, line)
        if mCallbackName is not None: callbackName = mCallbackName.group(1)
        if re.search(reBrownieConcreteTemplate, line) is not None:
            if i+1 < len(code_lines) : line += code_lines[i+1] # for multiline (2 lines only supported)
            line = line.replace("\n",' ')
            m = reCallDef.search(line)
            if m is not None:
                callType, callName, \
                    namespaceCaller, classCaller, \
                    namespaceCallee, classCallee = sortDefConcrete(m, callbackName)
                callType = template2callType(callType)
                callName = callName[:-len(callType)]
                graph.add_call(classCaller, classCallee, callName, callType)
    return 

######################################################################
#  
######################################################################

from networkx import DiGraph
from networkx.exception import NetworkXException, NetworkXError
# import networkx.convert as convert
# from copy import deepcopy
from sets import Set

class BrownieCallGraph(DiGraph):
    """
    Class of the graph with information about asynchronous calls and notifications.
    """

    def __init__(self, data=None, name='', file=None, **attr):
        """
        Constructor 
        """
        DiGraph.__init__(self, data=data,name=name,**attr)
        # DiGraph.add_node('Interface')

    @staticmethod
    def classAutoType(name):
        if   name.find('Service') != -1: return 'service'
        elif name[0] == 'I':             return 'interface'
        else:                            return 'class'

    def remove_class(self, name=None):
        """
        Remove node for the class
        """
        self.remove_node(name)

    def add_class(self, name=None, type = None):
        """
        Append node for the class involved in brownie interactions to the graph.
        """
        if name is not None: 
            if not self.has_node(name): 
                self.add_node(name)#'oval'
                if type is None:self.node[name]['type'] = self.classAutoType(name)
                else:           self.node[name]['type'] = type
            return name
        else: return 'Interface'

    def add_inheritance(self, classParent, classChild):
        self.add_class(classParent)
        self.add_class(classChild)
        self.add_edge(classParent, classChild, type = 'inheritance')
        
    def add_call(self, classCaller, classCallee, callName = None, callType='call'):
        """
        Append revieled brownie interaction (call/notification) to the graph.
        """
        nodeFrom = self.add_class(classCaller)
        nodeTo   = self.add_class(classCallee)
        if not self.has_edge(nodeFrom, nodeTo):
            self.add_edge(nodeFrom, nodeTo, type = 'brownie', call=Set(), notification=Set())
        if callName is not None:
            self[nodeFrom][nodeTo][callType].add(callName)

    def parse(self, f):
        """
        Parses definitions for *brownie* interactions
        (calls and notifications) from the C++ header
        and extracts this information into the graph.
    
        @param f      handle of file with C++ codes that have *brownie* definetions (LocalCallback/LocalCallable)
        @return list of definitions
        """
        parseBrownieDefs(self, f)

    def clone(self, type=None):
        """
        Extracts interactions of specific type 
        @param type   type of the interaction 
        | Type          | Action        |
        |-------------------------------|
        |None           | no filtering  |
        |'call'         | calls         | 
        |'notification' | notifications |
        """
        import copy
        graph = copy.deepcopy(self)
        if type is not None: # remove everythig unnecessary
            graph = BrownieCallGraph()
            for classCaller, classCallee, attribs in self.edges_iter(data=True):
                if attribs['type'] == 'brownie' and len(attribs[type]) > 0:
                    graph.add_call(classCaller, classCallee)
                    graph[classCaller][classCallee][type] = copy.deepcopy(self[classCaller][classCallee][type])
                elif attribs['type'] == 'inheritance':
                    graph.add_inheritance(classCaller, classCallee)
        return graph

    def auto_inheritances(self):
        for clsParent in self.nodes_iter():
            if self.node[clsParent]['type'] == 'interface':
                clsChild = 'C' + clsParent[1:]
                if self.has_node(clsChild) and self.node[clsChild]['type'] == 'class':
                    self.add_inheritance(clsParent, clsChild)

    def to_agraph(self, type=None, max_label = 4):
        """
        Converts graph to the graphvis format
        """
        graph = self.clone(type)
        for classCaller, classCallee, attribs in self.edges_iter(data=True):
            #graph[classCaller][classCallee]['arrowhead'] = 'vee' # 'diamond' #
            if graph[classCaller][classCallee]['type'] == 'brownie':
                graph[classCaller][classCallee]['fontsize'] = 10
                all_calls = list(graph[classCaller][classCallee]['call'] | \
                                     graph[classCaller][classCallee]['notification'])
                if len(all_calls) > max_label: 
                    all_calls = all_calls[:max_label-2] + ['. . .'] + [all_calls[-1]]
                graph[classCaller][classCallee]['label'] = '\n'.join(all_calls)
                graph[classCaller][classCallee]['fontcolor'] = 'gray50'

                if len(attribs['call']) > 0 and len(attribs['notification']) > 0:
                    graph[classCaller][classCallee]['color'] = 'green'
                elif len(attribs['call']) > 0:
                    graph[classCaller][classCallee]['color'] = 'blue'
                elif len(attribs['notification']) > 0:
                    graph[classCaller][classCallee]['color'] = 'red'

                
        for clsName in graph.nodes_iter():
            graph.node[clsName]['label'] = clsName #"{%s | | }" % clsName
            graph.node[clsName]['style']='filled'
            if clsName.find('Service') != -1:
                style = {'fillcolor' : 'white', 'shape' : 'tab'}
            else:
                style = {'fillcolor':'gray', 'shape':'box'}
            for styleName, styleVal in style.iteritems():
                graph.node[clsName][styleName] = styleVal

        from networkx import to_agraph
        return to_agraph(graph)

    def to_abigraph(self, styles, type=None, max_label = 4, name2URL = None):
        """
        Converts graph to the graphvis format
        """
        graph  = self.clone(type)
        mgraph = BrownieCallBiGraph(styles, 
                                    max_label = max_label,
                                    name2URL = name2URL)
        for classCaller, classCallee, attribs in graph.edges_iter(data=True):
            if attribs['type'] == 'inheritance': mgraph.add_inheritance(classCaller, classCallee)
            elif attribs['type'] == 'brownie'  :
                mgraph.add_calls(classCaller, classCallee, 
                                 graph[classCaller][classCallee]['call'] | \
                                     graph[classCaller][classCallee]['notification'])

        from networkx import to_agraph
        return to_agraph(mgraph)

class BrownieCallBiGraph(DiGraph):
    """
    Class of the graph with information about asynchronous calls and notifications.
    """
    
    def __init__(self, styles, max_label = 4, name2URL = None,
                 data=None, name='', file=None, **attr):
        """
        Constructor 
        """
        self.styles    = styles
        self.max_label = max_label
        self.name2URL = name2URL
        DiGraph.__init__(self, data=data,name=name,**attr)

    def add_class(self, name=None, type = None):
        """
        Append node for the class involved in brownie interactions to the graph.
        """
        if type is None: type = BrownieCallGraph.classAutoType(name)
        if name is not None: 
            # style = {
            #     'service'   : {'style' : 'filled', 'fillcolor' : 'white', 'shape' : 'tab'},
            #     'interface' : {'style' : 'filled,dashed,rounded', 'fillcolor' : 'gray',  'shape' : 'box', },
            #     'class'     : {'style' : 'filled', 'fillcolor' : 'gray',  'shape' : 'box'},
            #     }.get(type, {})
            if not self.has_node(name): 
                styles = dict(self.styles['node']['class']['default'])
                if self.styles['node']['class'].has_key('regex'):
                    for regexp,sty_re in \
                            self.styles['node']['class']['regex'].items():
                        if re.search(regexp.encode('ascii'), name) is not None:
                            styles.update(sty_re)
                            #break
                if self.name2URL is not None:
                    styles['URL'] = self.name2URL(name) 
                self.add_node(name, type = type, **styles)
            return name
        else: return 'Interface'

    def add_calls(self, classCaller, classCallee, calls):
        """
        Append the list of brownie interactions between 2 classes to the graph.
        """
        self.add_class(classCaller)
        self.add_class(classCallee)

        # style_label = {'fontsize' : 10, #'fontcolor' : 'gray50', 
        #          'shape' : 'plaintext'} #'point'
        style_label = self.styles['node']['interface']
        calls_list = list(calls)
        if len(calls_list) > self.max_label:
            calls_list = (calls_list[:self.max_label-2] + 
                          ['. . .', calls_list[-1]])
        calls_label = '\n'.join(calls_list)
        if not self.has_node(calls_label): 
            self.add_node(calls_label, type = type, **style_label)
        # style_caller = {'label' : '', 'dir' : 'forward', 'arrowtail' : 'empty', 'arrowhead' : 'tee', }#curve,oinv, crow
        # style_callee = {'label' : '', 'dir' : 'both',    'arrowtail' : 'odot',  'arrowhead' : 'none', }#back, normal
        style_caller = self.styles['edge']['require']
        style_callee = self.styles['edge']['provide']
        self.add_edge(classCaller, calls_label, **style_caller)
        self.add_edge(calls_label, classCallee, **style_callee)

    def add_inheritance(self, classParent, classChild):
        """
        Append inheritance between 2 classes to the graph.
        """
        style = self.styles['edge']['inherite']
        self.add_class(classParent)
        self.add_class(classChild)
        self.add_edge(classParent, classChild, type = 'inheritance', **style)
