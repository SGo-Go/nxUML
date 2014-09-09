#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       nxUML
(c) copyright 2014
######################################################################
@file         __iniy__.py
@author       Sergiy Gogolenko

Init-file for folder with core nxUML classes.
Majority of class hierarchy elements follows instructions presented in
http://www.uml-diagrams.org/uml-core.html
######################################################################
"""
from nxUML.core.debug import debug,warning,error

# Primitives
from nxUML.core.uml_class_primitives    import *
from nxUML.core.uml_multiplicity        import *
from nxUML.core.uml_modifier            import *

# Features
from nxUML.core.uml_feature             import *
from nxUML.core.uml_property            import *
from nxUML.core.uml_operation           import *

# Stereotypes
from nxUML.core.uml_stereotype          import *

# Class diag elements: classifiers, packages
from nxUML.core.uml_package             import *
from nxUML.core.uml_classifier          import *
from nxUML.core.uml_datatype            import *
from nxUML.core.uml_class               import *

# Relationships
from nxUML.core.uml_class_relationships import *
from nxUML.core.uml_dependency          import *

# Artifacts
from nxUML.core.uml_artifacts           import *


from nxUML.core.uml_pool                import *
from nxUML.core.uml_class_graph         import UMLClassRelationsGraph

# try:
#     from nxUML.core.uml_class_diag import UMLClassDiagram, UMLClassRelationsGraph
#     from nxUML.core.uml_class_diag import UMLClassDiagram
# except:
#     pass

