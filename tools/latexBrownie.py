#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
######################################################################
Project       DoxyUML
(c) copyright 2014
######################################################################
@file         latexBrownie.py
@author       Sergiy Gogolenko

Release data for DoxyUML.
######################################################################
"""

proj_dir  = r"D:/dev/NBT_Evo_sources_check"
file_list = (
    r"imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/CMapCommandBroker.hpp",
    r"imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/CMapCanvasHelper.hpp",
    r"imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/CPoiInfoCache.hpp",
    r"imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/IMapCommandBroker.hpp",
    r"imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/private/debug/CMapCtrlDebugInterface.hpp",
    # r"imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/",
    )

headerSubdirs = (
    r'imp/nav/ctrl/prj/nbt/map/mapctrl/core/src',
    r'imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/private/tasks',
    r'imp/nav/ctrl/prj/nbt/map/mapctrl/core/src/private/gesturestate',
    )

######################################################################
if __name__ == "__main__":
    # filename *.hpp-file with callback class
    
    import os
    from brownieDoc import findBrownieDefs,browniDefs2TeX
    
    from optparse import OptionParser
    parser = OptionParser(version='Version: %prog-0.0.1-beta')
    parser.add_option("-d", "--proj-prefix", dest="proj_dir",
                      action="store", type="string", 
                      help="project root directory", default=proj_dir)
    parser.add_option("-n", "--notifications", 
                      action="store_true", dest="bNotifications", default=False,
                      help="extract notifications")
    parser.add_option("-c", "--calls", 
                      action="store_true", dest="bCalls", default=True,
                      help="extract calls")
    (options, args) = parser.parse_args()

    defs_type = 'call'
    if options.bNotifications: defs_type = 'notification'
    elif options.bCalls:       defs_type = 'call'

    import glob
    file_list = []
    for folder in headerSubdirs:
        file_list.extend(glob.glob(\
                os.path.join(options.proj_dir, os.path.join(folder, '*.hpp'))))

    for filename in file_list:
        with open(os.path.join(options.proj_dir, filename)) as f:
            lines = f.readlines()
            lst_calls = findBrownieDefs(lines, defs_type = defs_type)
            if len(lst_calls) > 0:
                print browniDefs2TeX(lst_calls),
                print r"\hline\hline"

# assoc .py=Python.File
# ftype Python.File=C:\Path\to\pythonw.exe "%1" %*
