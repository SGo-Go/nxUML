nxUML
--------------------------------
**Purpose:** 
nxUML is a simple and extensible Python package 
for easily tunable parsing source codes (and UML class diagrams)
into unified representation of collaborations between classes based on UML standard
for further analysis, as well as  automated creating and visualization of UML diagrams.

Currently only C++ sources are supported.
It can be easily used as an extension to Doxygen
for tunable generating collaboration diagrams.

Features:
* easily tunable parsing of C++ sources 
* extended mapping of classes collaborations into networkx.MultiGraph object
* tunable visualization of class diagrams with Graphviz

TODO list (urgent):
* avoid double-parsing of typedefs in C++
* extended support of qualifiers and templated classes
* parser for Python codes, as well as UFX and XMI files
* export to UFX and XMI

Copyright (C) 2014 nxUML 

Sergiy Gogolenko <sergiy.gogolenko@gmail.com>
