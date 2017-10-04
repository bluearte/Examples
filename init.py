import nuke
import nukescripts
# import re
# import os
# import sys
# import glob

# from scripts import setupReadNodes
# from scripts import setupSystem

# gizmos_dir = os.listdir(r'C:\PrivateFolder\_plugins\nuke\gizmos')
# gizmo_list = [x.split('.')[0] for x in gizmos_dir if x.endswith('.gizmo')]
# for each_gizmo in gizmo_list:
    # toolbar = nuke.menu('Nodes').addMenu('Custom Gizmo').addCommand(str(each_gizmo))

# nuke.menu('Nuke').addCommand('EZ_Tools/Reload Read Nodes', 'setupReadNodes.reloadReadNodes()')
# nuke.menu('Nuke').addCommand('EZ_Tools/Setup Read Nodes', 'setupReadNodes.setupReadNodes()')
# nuke.menu('Nuke').addCommand('EZ_Tools/Create Read From Write', 'setupReadNodes.readFromWrite()')
# nuke.menu('Nuke').addCommand('EZ_Tools/Autopath Setup', 'setupSystem.setupAutopath()')
# nuke.menu('Nuke').addCommand('EZ_Tools/Setup Write Node', 'setupSystem.setupWriteNode()')
# nuke.menu('Nuke').addCommand('EZ_Tools/Setup Nukescripts', 'setupSystem.setupNukescripts()')

# nuke.menu('Nodes').addCommand('EZ_Tools/Node1', lambda:nuke.message('This is called from Node1'))
# nuke.menu('Nodes').addCommand('EZ_Gizmos/alpha Edge', 'nuke.createNode("alphaEdge.gizmo")')