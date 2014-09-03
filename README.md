nxUML
--------------------------------
**Purpose:** 
nxUML is a Python package for user driven 

easily tunable parsing source codes
into unified representation of collaborations between classes based on UML standard. 
for further analysis, as well as  automated creating and visualization of UML diagrams.

Currently only C++ sources are supported.
It can be easily used as an extension to Doxygen
for tunable generating collaboration diagrams.

Features:
* easily tunable parsing of C++ sources 
* extended mapping of classes collaborations into networkx.MultiGraph object
* tunable visualization of class diagrams with Graphviz

TODO list:
- urgent
  * avoid double-parsing in C++ due to relying on CppHeaderParser
    with poor implementation of parsing facilities
  * extended support of qualifiers and templated classes
  * support of Markdown and XML in Doxy-comments
  * export to UFX and XMI

- conceptual
  * complete system of classes for representation of parsed objects that utilizes UML standard
  * unified representation of Artifacts and Classifiers in UML pool
  * parser for Python codes, as well as UFX and XMI files
  * efficient caching of parsed data
  * broad support for middleware classes which can intervene at 
    various stages of source code processing by parsers and carry out custom functions,
    dispatcher system for parsers
  * a diverse and deep serialization system which 
    can produce and read XML and/or JSON representations of UML element instances
  * a template system for document outputs
  * an interface to Django framework and Jinja2
  * integration with numba for faster parsing and output

Copyright (C) 2014 nxUML, All Right Reserved
License: GPL

Sergiy Gogolenko <sergiy.gogolenko@gmail.com>
