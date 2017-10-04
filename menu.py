import nuke
import nukescripts
import re
import os
import sys
import glob

from scripts import setupReadNodes
from scripts import setupSystem

NUKE_PATH = os.path.dirname(__file__)
NUKE_DIRECTORY = os.listdir(NUKE_PATH)
NUKE_GIZMOS = [x.split('.')[0] for x in os.listdir(NUKE_PATH+r'\gizmos') if x.endswith('gizmo')]

for eachDir in NUKE_DIRECTORY:
    nuke.pluginAddPath(os.path.join(NUKE_PATH,eachDir))
    
for eachGizmos in NUKE_GIZMOS:
        nuke.menu('Nodes').addMenu('EZ_Gizmos').addCommand(str(eachGizmos))

nuke.menu('Nuke').addCommand('EZ_Tools/Reload Read Nodes', 'setupReadNodes.reloadReadNodes()')
nuke.menu('Nuke').addCommand('EZ_Tools/Setup Read Nodes', 'setupReadNodes.setupReadNodes()')
nuke.menu('Nuke').addCommand('EZ_Tools/Create Read From Write', 'setupReadNodes.readFromWrite()')
# nuke.menu('Nuke').addCommand('EZ_Tools/Autopath Setup', 'setupSystem.setupAutopath()')
# nuke.menu('Nuke').addCommand('EZ_Tools/Setup Write Node', 'setupSystem.setupWriteNode()')
nuke.menu('Nuke').addCommand('EZ_Tools/Setup Nukescripts', 'setupSystem.setupNukescripts()')

nuke.menu('Nodes').addCommand('EZ_Tools/Node1', lambda:nuke.message('This is called from Node1'))