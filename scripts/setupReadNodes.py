import nuke
import nukescripts
import os
import re
import glob

# Create a String Pattern that can match any <filename>.<ext>
SINGLE_NAME_PATTERN = re.compile("(?P<fileName>.+)\.(?P<ext>\D+)", re.IGNORECASE)

# Create a String Pattern that can match any <filename>.<framepadding>.<ext>
SEQ_NAME_PATTERN = re.compile("(?P<fileName>.+)\.(?P<frameNum>\d+)\.(?P<ext>\D+)", re.IGNORECASE)

# Create a String Pattern that can match any <filename>/<passname>.<framepadding>.<ext>
PASS_NAME_PATTERN = re.compile("(?P<fileName>.+)\.(?P<passName>\w+)\.(?P<frameNum>\d+)\.(?P<ext>\D+)", re.IGNORECASE)

def reloadReadNodes():
    """
    This function will execute reload knob from all available read nodes
    """
    try:
        readNode = nuke.allNodes('Read')    # query all of available read nodes in DAG
        for read in readNode:
            read['reload'].execute()        # this execute the reload knob
    except Exception as e:
        print e                             # if anything go wrong this will print the error value

def readGlobalSetup(file, firstFrame, lastFrame):
    """
    This function act as global setup first and last frame for read node
    """
    file['first'].setValue(firstFrame)         # set the first frame
    file['last'].setValue(lastFrame)           # set the last frame    
    file['origfirst'].setValue(firstFrame)     # set the original first frame
    file['origlast'].setValue(lastFrame)       # set the original last frame
    
def getFrameRange(globName):
    """
    This function is to get all the frame range from all Read Nodes
    """
    # Create an empty list to store all of the sequence image
    fileList = []                                                       
    
    # Create a loop to obtain all of the sequence name and append it to list
    for name in glob.glob(globName):
        fileList.append(name)
        fileList.sort()
    
    # Get first and last frame from the list and return it as a value
    firstFrame = int(re.findall(r'\d+', os.path.basename(fileList[0]))[-1])  
    lastFrame  = int(re.findall(r'\d+', os.path.basename(fileList[-1]))[-1]) 
    return firstFrame, lastFrame
        
def verifyNamePattern(file, nodeName):
    dirname = os.path.dirname(file)
    basename = os.path.basename(file)
    
    # verify the name pattern
    singleMatch = re.match(SINGLE_NAME_PATTERN, basename)
    seqMatch = re.match(SEQ_NAME_PATTERN, basename)
    passMatch = re.match(PASS_NAME_PATTERN, basename)
    
    # any name that match to the name pattern will divided
    if singleMatch is not None:
        # This image doesn't have any frame so it will return 1 first and last frame
        readGlobalSetup(nodeName, 1, 1)
        
    if seqMatch is not None:
        # This image has the frame number and will replace the padding name to ####
        sequence_pattern_padding = re.sub(SEQ_NAME_PATTERN,"\g<fileName>.####.\g<ext>", file)
        new_read = nodeName['file'].setValue(sequence_pattern_padding)
        
        # Get the frame number and replace it with a meta character (?) and get the framerange
        frame_padding = seqMatch.group("frameNum")
        metaChar = '?'*len(frame_padding)
        sequence_pattern_glob = re.sub(SEQ_NAME_PATTERN,"\g<fileName>."+metaChar+".\g<ext>", file)
        framerange = getFrameRange(sequence_pattern_glob)
        
        # Set all the read nodes frame range based on its image frame range
        readGlobalSetup(nodeName, framerange[0], framerange[-1])
        
    if passMatch is not None:
        # This image has the pass name and also the frame number, will replace the padding name to ####
        pass_pattern_padding = re.sub(PASS_NAME_PATTERN,"\g<fileName>.\g<passName>.####.\g<ext>", file)
        new_read = nodeName['file'].setValue(pass_pattern_padding)
        
        # Get the frame number and replace it with a meta character (?) and get the framerange
        frame_padding = seqMatch.group("frameNum")
        metaChar = '?'*len(frame_padding)
        pass_pattern_glob = re.sub(PASS_NAME_PATTERN,"\g<fileName>.\g<passName>."+metaChar+".\g<ext>", file)
        framerange = getFrameRange(pass_pattern_glob)
        
        # Set all the read nodes frame range based on its image frame range
        readGlobalSetup(nodeName, framerange[0], framerange[-1])

def readFromWrite():
    """
    This function will create a read node based on selected Write node
    """
    try:
        write = nuke.selectedNode()                                 
        if write.Class() == "Write":                                
            writeFile = write['file'].evaluate()
            if writeFile:
                xPos = write.xpos()                                     
                yPos = write.ypos()
                read = nuke.nodes.Read()
                readFile = read['file'].setValue(writeFile)
                verify_name = verifyNamePattern(writeFile, read)
                read.setXpos(xPos)                                      
                read.setYpos(yPos+100)                                  
        else:                                                       
            nuke.message("Please select the write node")            # it will give warning
    except ValueError as ve:
        nuke.message(str(ve)+" Please select the Write node")       # if there is no node selected, it will pop up a warning        
    
def setupReadNodes():
    """
    This function is to set all the frame range to all Read Nodes
    """
    for readNode in nuke.allNodes('Read'):
        try:
            readFile = readNode['file'].evaluate()                                     
            if readFile:
                verify_name = verifyNamePattern(readFile, readNode)                               
        except IndexError as ie:
            print(ie)
