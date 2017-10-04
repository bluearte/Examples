import nuke
import nukescripts
import os
import re
import glob

from setupReadNodes import setupReadNodes

def setupAutopath():
    readNodes = nuke.allNodes('Read')
    oldpath = '<render_directory>/'
    new = '[value AutoPath.RenderFile]'
    for readNode in readNodes:
        file = readNode['file'].evaluate()
        suffixFile = file.split(oldpath)
        prefix = os.path.join(new,suffixFile[1]).replace('\\','/')
        newFile = readNode['file'].setValue(prefix)

def createDirectory():
    trgDir = os.path.dirname( nuke.filename( nuke.thisNode() ) )    # get the destination folder
    if not os.path.isdir( trgDir ):                                 # check if the destionation folder is not exist
        os.makedirs( trgDir )                                       # create the folder
        
def setupWriteNode():
    nuke.delete(nuke.toNode('Write2'))
    writeImport = nuke.scriptReadFile("<output_directory>\\WriteNode.nk")
    writeNode = nuke.toNode('Write_Img_Sequence')
    writeNode.knob('beforeRender').setValue("try:\n\tcreateDirectory()\nexcept Exception as e:\n\tprint(e)")
    destination = nuke.toNode('Image_Sequence')
    xPos = destination.xpos()
    yPos = destination.ypos()
    writeNode.connectInput(0, destination)
    writeNode.setXpos(xPos)
    writeNode.setYpos(yPos+100)

def getGlobalFrame():
    firstList = []
    lastList = []
    for each in nuke.allNodes('Read'):
        firstList.append(each.knob('first').value())
        lastList.append(each.knob('last').value())

    return min(firstList), max(lastList)

def nukescriptGlobalSetup(firstFrame, lastFrame):
    nuke.Root()['first_frame'].setValue(firstFrame)
    nuke.Root()['last_frame'].setValue(lastFrame)
    
def setupNukescripts():
    try:
        setupReadNodes()
    except Exception as e:
        print(e)
    finally:
        nukescriptGlobalSetup(getGlobalFrame()[0], getGlobalFrame()[1])
    
