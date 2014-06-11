#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         brownieDoc.py
@author       Sergiy Gogolenko

This utility is intended to analyse C++ codes with asynchronous
calls and notifications.
######################################################################
"""
from __future__ import print_function

__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

def warning(*objs):
    import sys
    print("WARNING: ", *objs, file=sys.stderr)

def print_log(*objs):
    import sys
    print("INFO: ", *objs, file=sys.stdout)

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

def name2URLheader(className, file_list):
    import urlparse, urllib
    url = ""
    for filename in file_list:
        if filename.find("%s.hpp" % className) != -1:
            url = urlparse.urljoin('file:', urllib.pathname2url(filename))
            #url = "file://localhost/" + filename.replace("\\", "/")
            #url = urlparse.urlunparse(urlparse.urlparse(filename)._replace(scheme='file'))
            break
    return url
######################################################################

proj_dir  = r"."
headerSubdirs = ('',) #('src',)
default_styles = {"node" : {
        'class'     : {
            'default'   : {'style' : 'filled', 
                           'fillcolor' : 'gray',  'shape' : 'box'},
	    },
        'interface' : {'fontsize' : 10, 
                       'fontcolor' : 'black', 'shape' : 'plaintext'}
	},
                  "edge" : {
        "inherite" : {'label' : '', 'style' : 'dashed', 'dir' : 'back', 
                      'arrowtail' : 'empty', 'arrowhead' : 'none'},
        "require"  : {"label" : "", "dir" : "forward", 
                      "arrowtail" : "empty", "arrowhead" : "tee"},
        "provide"  : {"label" : "", "dir" : "both", 
                      "arrowtail" : "odot",  "arrowhead" : "none"}
	}
                  }

######################################################################
if __name__ == "__main__":
    # filename *.hpp-file with callback class

    options = {
        'subdirs'       : headerSubdirs, 
        'styles'        : default_styles,
        }
    
    import os    
    from optparse import OptionParser
    parser = OptionParser(version='Version: %prog-0.0.1-beta')
    parser.add_option("-d", "--proj-prefix", dest="proj_prefix", 
                      action="store", type="string", metavar="FOLDER",
                      help="project root directory", default=proj_dir)
    parser.add_option("-r", "--recursive", 
                      action="store_true", dest="recursive", default=False,
                      help="recursively search C++ headers for analysis")
    parser.add_option("-n", "--notifications", 
                      action="store_true", dest="notifications", default=False,
                      help="extract notifications")
    parser.add_option("-c", "--calls", 
                      action="store_true", dest="calls", default=False,
                      help="extract calls")
    parser.add_option("-o", "--output", dest="output",
                      action="store", type="string", metavar="FILE", 
                      help="name of output figure(s) with interconnection data", 
                      default='output.pdf')
    parser.add_option("-p", "--parts", 
                      action="store_true", dest="subgraphs", default=False,
                      help="store figures with subgraphs")
    parser.add_option("-j", "--json-options", dest="json_options",
                      action="store", type="string", 
                      help="JSON file with options \n"\
                          "(higher priority than command line)", default='')
    parser.add_option("-f", "--filter", dest="filter",
                      action="store", type="string", 
                      help="filter for headers", default='*.hpp')
    parser.add_option("-i", "--insert-classes", dest="insert_classes",
                      action="store", type="string", metavar="LIST", 
                      help="show diagram for the listed classes "\
                          "with its neighbours only", default='')
    parser.add_option("-e", "--exclude-classes", dest="exclude_classes",
                      action="store", type="string", metavar="LIST",
                      help="exclude the listed classes from the diagram", 
                      default='')
    parser.add_option("-l", "--load", dest="load",
                      action="store", type="string", metavar="FILE",
                      help="load BROWNIE call graph from tag file\n"\
                          " (Python pickles format)", 
                      default='')
    parser.add_option("-s", "--store", dest="store", 
                      action="store", type="string", metavar="FILE", 
                      help="generated and store tag file for BROWNIE call graph\n"\
                          "(Python pickles format)", 
                      default='')
    
    (cmd_options, args) = parser.parse_args()

    # Import command line options 
    for opt, val in cmd_options.__dict__.items():
        options[opt] =  val

    # Import options from JSON
    if len(cmd_options.json_options) > 0:
        import json, sys
        #print(json.dumps(default_styles), file=sys.stdout)
        with open(cmd_options.json_options) as f:
            optjson = json.loads("".join(f.readlines()))
            # object_hook = ascii_encode_dict
            for opt in optjson.keys():
                options[opt] = optjson[opt]

    # Analyse options
    if not options['notifications'] ^ options['calls']:
        defs_type = None
    elif options['notifications']: defs_type = 'notification'
    elif options['calls']:         defs_type = 'call'

    ######################################################################
    # Parse C++ files to Brownie call graph
    ######################################################################

    # Compute list of headers
    file_list = []
    if len(options['subdirs']) > 0:
        headerSubdirs = map(lambda folder:os.path.join(options['proj_prefix'], 
                                                       folder), options['subdirs'])
        if options['recursive']:
            import fnmatch, os
            for folder in headerSubdirs:
                for root, dirnames, filenames in os.walk(folder):
                    file_list.extend(
                        map(lambda filename: os.path.join(root, filename), 
                            fnmatch.filter(filenames, options['filter'])))
        else:
            import glob
            for folder in headerSubdirs:
                file_list.extend(glob.glob(\
                        os.path.join(options['proj_prefix'], 
                                     os.path.join(folder, options['filter']))))

        #print(len(file_list))

    # Load stored call graph and parse new headers
    from DoxyUML.brownie_doc import BrownieCallGraph

    if len(options['load']) > 0:
        import pickle
        with open(options['load']) as f: 
            graphBrownie = pickle.load(f)
    else:
        graphBrownie = BrownieCallGraph()

    for filename in file_list:
        with open(filename) as f:
            graphBrownie.parse(f)
    graphBrownie.auto_inheritances()

    ######################################################################
    # Manipulate with the call graph
    ######################################################################

    if len(options['store']) > 0:
        import pickle
        with open(options['store'], 'w') as f: 
            pickle.dump(graphBrownie, f)
    
    # Select important classes
    if len(options['insert_classes']) > 0:
        from sets import Set
        neighborhood = lambda node: Set(graphBrownie.predecessors(node) +
                                        graphBrownie.successors(node) + 
                                        [node])
        import re
        setNeighbors = Set()
        for className in options['insert_classes'].split(','):
            if re.search("^[a-zA-Z_][a-zA-Z0-9_]*$", className) is None:
                #warning("No support of RegEx: {0}.".format(className))
                for classNameSample in graphBrownie.nodes_iter():
                    if re.search("^" + className + "$", classNameSample):
                        print_log("RegEx({0}) -> {1}".\
                                      format(className,classNameSample))
                        setNeighbors |= neighborhood(classNameSample)
            else:
                if not graphBrownie.has_node(className):
                    warning("Ignor {0} in --insert-classes. \n"
                            "   Call graph does not have class {0}.".format(className))
                else:
                    setNeighbors |= neighborhood(className)
        graphBrownie = graphBrownie.subgraph(list(setNeighbors))

    # Remove classes that are not required
    if len(options['exclude_classes']) > 0:
        for className in options['exclude_classes'].split(','):
            if not graphBrownie.has_node(className):
                warning("Ignor {0} in --exclude-classes. \n"
                        "   Call graph does not have class {0}.".format(className))
            else:
                graphBrownie.remove_class(className)

    if len(graphBrownie) == 0:
        warning("Empty graph")

    ######################################################################
    # Store figures of call graph
    ######################################################################
  
    if options['output']:
        name2URL = lambda name: name2URLheader(name, file_list)

        # Draw the whole call graph
        A = graphBrownie.to_abigraph(options['styles'], 
                                     type=defs_type, max_label = 40,
                                     name2URL = name2URL)
        A.layout("dot")
        nameOut, extOut = os.path.splitext(options['output'])
        A.draw("%s%s" % (nameOut, extOut))

        # Draw subgraphs if needed
        if options['subgraphs']:
            from networkx import to_agraph, weakly_connected_component_subgraphs
            i = 0
            for subgraphBrownie in weakly_connected_component_subgraphs(\
                graphBrownie.clone(type=defs_type)):
                if len(subgraphBrownie.nodes()) > 1:
                    i += 1
                    # A = subgraphBrownie.to_agraph()
                    A = subgraphBrownie.to_abigraph(options['styles'], 
                                                    max_label = 40)
                    A.layout('dot')
                    A.draw("%s%i%s" % (nameOut, i, extOut))
