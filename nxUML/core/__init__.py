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
######################################################################
"""
from nxUML.core.debug import debug,warning,error

from nxUML.core.uml_class_primitives    import *
from nxUML.core.uml_multiplicity        import *
from nxUML.core.uml_classifier          import *
from nxUML.core.uml_datatype            import *
from nxUML.core.uml_package             import *
from nxUML.core.uml_class               import *
from nxUML.core.uml_class_relationships import *
from nxUML.core.uml_artifacts           import *
from nxUML.core.uml_pool                import *

from nxUML.core.uml_class_diag import UMLClassDiagram, UMLClassRelationsGraph

# try:
#     from nxUML.core.uml_class_diag import UMLClassDiagram
# except:
#     pass

