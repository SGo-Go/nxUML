#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         uml_stereotype.py
@author       Sergiy Gogolenko

This library is intended to parse codes into unified class model 
stored as networkx graph object.
######################################################################
"""
__author__ = """Sergiy Gogolenko (sgogolenko@luxoft.com)"""

from nxUML.core.uml_class_primitives    import IUMLElement

from nxUML.core.uml_classifier          import UMLClassifier
from nxUML.core.uml_property            import UMLMetaproperty

######################################################################
class UMLProfileClass(UMLClassifier):
    """Profile class 
    """
    pass

class UMLMetaclass(UMLProfileClass):
    """A profile class and a packageable element which may be extended through one or more stereotypes
    """
    pass

class UMLStereotype(UMLProfileClass):
    """Stereotype is a profile class which defines 
    how an existing metaclass may be extended as part of a profile. 
    It enables the use of a platform or domain specific terminology or notation in place of, 
    or in addition to, the ones used for the extended metaclass. 
    """
    def __init__(self, name, scope  = None,
                 metaproperties = [],):
        self.metaproperties = metaproperties
        super(UMLStereotype, self).__init__(name = str(name), scope = scope)

    def add_metaproperty(self, metaprop):
        self.metaproperties.append(metaprop)

    @property
    def metaclass(self):
        return 

    def __repr__(self):
        return "<<metaclass>>{0}".format(self.stereotype.name)

    @property
    def tag(self):
        """Specifies XML tag `stereotype' for the serialized instances of UML stereotype
        """
        return 'stereotype'

    def toXML(self, root = None, reference = False):
        xmlStereotype = super(UMLStereotype, self).toXML(root = root, reference = reference)
        return xmlStereotype

class UMLStereotype(UMLProfileClass):
    """Stereotype is a profile class which defines 
    how an existing metaclass may be extended as part of a profile. 
    It enables the use of a platform or domain specific terminology or notation in place of, 
    or in addition to, the ones used for the extended metaclass. 
    """
    def __init__(self, name, scope  = None,
                 metaproperties = [],):
        super(UMLStereotype, self).__init__(name = name, scope = scope)
        self.metaproperties = metaproperties
        self.unparametrized_application = UMLStereotypeApplication(self)

    def add_metaproperty(self, metaprop):
        self.metaproperties.append(metaprop)

    @property
    def metaclass(self):
        return 

    def __repr__(self):
        return self.name

    @property
    def tag(self):
        """Specifies XML tag `stereotype' for the serialized instances of UML stereotype
        """
        return 'stereotype'

    def application(self, *values, **kwvalues):
        if len(self.metaproperties) == 0 or len(values) == 0:
            return self.unparametrized_application
        else:
            return UMLStereotypeApplication(self, *values, **kwvalues)

    def toXML(self, root = None, reference = False):
        xmlStereotype = super(UMLStereotype, self).toXML(root = root, reference = reference)
        return xmlStereotype

class UMLStereotypeApplication(IUMLElement):
    """Stereotype is a profile class which defines 
    how an existing metaclass may be extended as part of a profile. 
    It enables the use of a platform or domain specific terminology or notation in place of, 
    or in addition to, the ones used for the extended metaclass. 
    """
    def __init__(self, stereotype, *values, **kwvalues):
        self.stereotype = stereotype
        self.values = values
        super(UMLStereotypeApplication, self).__init__()

    @property
    def name(self):
        return self.stereotype.name

    def __repr__(self):
        return "<<stereotype>>{0}".format(self.stereotype.name)

class UMLStereotypeStack(list, IUMLElement):
    focus = UMLStereotype('focus', scope = None)
    """Focus is class that defines the core logic or control flow 
    for one or more supporting classes.
    Focus classes are typically used for specifying the core business logic 
    or control flow of components during design phase."""

    auxiliary = UMLStereotype('auxiliary', scope = None)
    """Auxiliary is a class that supports another more central or fundamental class, 
    typically by implementing secondary logic or control flow."""

    Type     = UMLStereotype('type', scope = None)
    """Type is class that specifies a domain of objects 
    together with the operations applicable to the objects, 
    without defining the physical implementation of those objects.
    Type may have attributes and associations."""

    utility  = UMLStereotype('utility', scope = None)
    """Utility is class that has only class scoped static attributes and operations. 
    Utility class usually has no instances."""

    boundary = UMLStereotype('boundary', scope = None)
    """Boundary is a stereotyped class or object that represents some system boundary, 
    e.g. a user interface screen, system interface or device interface object. 
    It is often used in sequence diagrams which demonstrate user interactions with the system."""

    control  = UMLStereotype('control', scope = None)
    """Control is a stereotyped class or object that is used to 
    model flow of control or some coordination in behavior. 
    It usually describes some "business logic"."""

    entity   = UMLStereotype('Entity', scope = None)
    """Entity is a stereotyped class or object that represents 
    some information or data, usually but not necessarily persistent."""

    def __init__(self, uml_stereo = []):
        super(UMLStereotypeStack,self).__init__(uml_stereo)

    def add(self, stereo, *values, **kwvalues):
        if isinstance(stereo, UMLStereotypeApplication):
            self.append(stereo)
        elif isinstance(stereo, UMLStereotype):
            self.append(stereo.application(*values, **kwvalues))
        else:
            self.append(UMLStereotypeApplication(name))

    def __repr__(self):
        return "<<{0}>>".format(','.join(map(lambda stereo: stereo.name, self))) \
            if len(self) > 0 else ''

    def toXML(self, root, reference = False):
        pass
        # for stereo in self:
        #     xmlMulti = multi.toXML(root)
