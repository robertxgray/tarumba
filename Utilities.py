# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Utilities.py
# Purpose:      Set of useful functions.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Utilities.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# Some functions must be always available, we define them before imports

# Ok, some imports are really needed by those functions
import Globals

import sys
import re

# Debug levels
# Are the same used by the ColorLogCtrl
INFO = 1 
WARN = 2 
ERRO = 3
SPAM = 4

def Debug(message):
    "Shows a message in the error output"
    if Globals.VERBOSE:
        sys.stderr.write((message+'\n').encode(
            sys.getfilesystemencoding(),'replace'))
            
def Log(message,level):
    "Shows a message in the GUI console"
    if len(message) > 0 and message[-1] != '\n':
        message += '\n'
    txtLevel = ''
    if level == INFO:
        txtLevel = _(u'INFO') + ': '
    elif level == WARN:
        txtLevel = _(u'WARNING') + ': '
    elif level == ERRO:
        txtLevel = _(u'ERROR') + ': '
    if Globals.OUTPUT_LOG:
        Globals.OUTPUT_LOG.Log(txtLevel+message,level)
    # If the GUI console is unavailable, use the error output
    else:
        sys.stderr.write((txtLevel+message).encode(sys.getfilesystemencoding(),'replace'))
        
def StandartOutput(message):
    "Show the message in the standart output"
    sys.stdout.write((message+'\n').encode(
        sys.getfilesystemencoding(),'replace'))

import Executor

import os
import wx
import getpass
import stat
import pexpect
import shutil
import subprocess
import stat

def processOutputInTreeListCtrlAux (output, filenamePos, treeListCtrl, 
    root, function = lambda x,y:None):
    '''
    Fills the TreeListCtrl with the info from the external program.
    output -> List with the output lines from the compressor
    filenamePos -> Position where the filenames start
    treeListCtrl -> TreeListCtrl where to show the information
    raiz -> Tree's root
    function -> function to process the coumns but the main
    '''
    # Reset the number of elements in the file
    Globals.file_num_elements = 0
    # Must be imported after the wxApp exists
    if not Globals.NOGUI:
        import MimeIcons
        # Start the file icon manager
        itclFolder, itclFolderExp = MimeIcons.Begin()
    else:
        itclFolder = None
        itclFolderExp = None
    # Dictionaries to record nodes and element repetitions
    nodes = {}
    repetitions = {}
    # For every line in the output
    for line in output:
        # Ignore empty lines
        if not line:
            continue
        try:
            # Increase the number of elements counter
            Globals.file_num_elements += 1
            # Split file attributes
            items = line.split(None, filenamePos)
            # Get the name of the content
            fullPath = items[filenamePos]
            # Remove the reference in symlinks
            arrowPosition = fullPath.find('->')
            if arrowPosition > 0:
                # Usually there is an space after the arrow, hence the -1
                fullPath = fullPath[:arrowPosition-1]
            # Split the route by directories
            fullPathAux = fullPath.split('/')
            # Delete empty chunks (i.e. double slash)
            for k in range(len(fullPathAux)-1,-1,-1):
                if fullPathAux[k] == '':
                    del(fullPathAux[k])
            for j in range(len(fullPathAux)):
                i = j+1
                # Get parent node
                if (i == 1):
                    parent = root
                else:
                    parent = nodes['/'.join(fullPathAux[:(j)])]
                # While folders, add them to the tree
                if ((i < len(fullPathAux)) or (fullPath[-1] == '/')):
                    relaPath = '/'.join(fullPathAux[:i])
                    if relaPath not in nodes:
                        # Add the folder to the TreeListCtrl and the nodes
                        elemAdded = treeListCtrl.AppendItem(parent, fullPathAux[j], itclFolder, itclFolderExp)
                        nodes[relaPath] = elemAdded
                        # Folders work fine with repetitions = 0
                        treeListCtrl.SetPyData(elemAdded, (relaPath+'/', 0, False))
                # Files are added managing the repetitions
                else:
                    if fullPath in repetitions:
                        numberRep = repetitions[fullPath] + 1
                    else:
                        numberRep = 1
                    repetitions[fullPath] = numberRep
                    # Add the file to the TreeListCtrl
                    if not Globals.NOGUI:
                        icon = MimeIcons.Icon(fullPath)
                    else:
                        icon = None
                    elemAdded = treeListCtrl.AppendItem(parent, fullPathAux[j], icon)
                    treeListCtrl.SetPyData(elemAdded, (fullPath, numberRep, True))
            # If it's an already generated folder, the elemAdded variable
            # will contain an old value, I try to avoid it
            if (fullPath[-1] == '/'):
                elemAdded = nodes[fullPath[:-1]]
                # Mark the folder as existent
                treeListCtrl.SetPyData(elemAdded, (relaPath+'/', 0, True))
            # Call the function that process the other colums
            function(items, elemAdded)
        # Handle unexpected errors
        except Exception, e:
            raise Exception(_('Unexpected archive content ->')+' '+line)
    # Load the information for the root element
    root = treeListCtrl.GetRootItem()
    treeListCtrl.SetPyData(root, ('', 0, False))
    # Load the icons in the TreeListCtrl
    if not Globals.NOGUI:
        MimeIcons.End(treeListCtrl)

def RecursiveSelection(treeCtrl, id):
    "Recursively selects the contents of a tree (by following depth)"
    # Auxiliary recursive function
    selection = []
    def _recursive(treeCtrl, id):
        selection.append(treeCtrl.GetPyData(id))
        numSons = treeCtrl.GetChildrenCount(id, False)
        cookie = None
        for i in range(numSons):
            if i == 0:
                son, cookie = treeCtrl.GetFirstChild(id)
            else:
                son, cookie = treeCtrl.GetNextChild(id, cookie)
            _recursive(treeCtrl, son)
    _recursive(treeCtrl, id)
    return selection

def RecursiveSelectionInFileSys(top):
    "Similar to the previous by it works over the file system"
    output = []
    if os.path.isfile(top) or os.path.islink(top):
        output.append(top)
    else:
        output.append(top)
        for root, dirs, files in os.walk(top, topdown=True):
            for name in files:
                output.append(os.path.join(root, name))
            for name in dirs:
                output.append(os.path.join(root, name))
    return output

def ConfirmOverwriteFilesLocal(contents, path, firstCall):
    "Checks if any file exists in the destination path and asks to overwrite"
    # Variables to control the dialog with the user
    # Declare them global to retain the value
    global COFL_ask
    global COFL_answer
    global COFL_firstQuestion
    global COFL_secondQuestion
    # Initialize them in the first execution
    if firstCall:
        COFL_ask = (not Globals.NO_CONFIRM_OVERWRITE)
        if Globals.NO_CONFIRM_OVERWRITE:
            COFL_answer = wx.ID_YES
        else:
            COFL_answer = wx.ID_NO
        COFL_firstQuestion = True
        COFL_secondQuestion = False
    # Get the prefix that will be removed from the files
    prefixAux = contents[0][0]
    if prefixAux and (prefixAux[-1] == '/'):
        prefixAux = prefixAux[:-1]
    prefix = os.path.dirname(prefixAux)
    if prefix:
        prefix = prefix + '/'
    lenPrefix = len(prefix)
    # Process every content
    deleteList = []
    end = len(contents)
    i = 0
    while (i < end):
        # Bypass the root of the compressed file
        if contents[i][0]:
            deleteContent = False
            redundantFolder = False
            # Get final path for the file
            finalPath = os.path.join(path, contents[i][0][lenPrefix:])
            # If it's a folder that already exists, mark as redundant
            if (contents[i][0][-1] == '/'):
                if os.path.lexists(finalPath):
                    deleteContent = True
                    if os.path.isdir(finalPath):
                        redundantFolder = True
                    # Show a warning if it exists as a file
                    elif COFL_ask:
                        WarningDialog(_(u'There is a file with the same name \n' \
                            u'as the folder that is being created.'))
            # If it's a file and exists, ask to delete
            elif os.path.lexists(finalPath):
                deleteContent = True
                # Show a warning if it's a folder
                if COFL_ask and os.path.isdir(finalPath):
                    WarningDialog(_(u'There is a folder with the same name as\n' \
                        u'the file that is being created.'))
            if deleteContent:
                # Redundant folders can be removed from the list safely
                if redundantFolder:
                    deleteList.append(i)
                else:
                    # The second time we give the option to overwrite 
                    # everything or nothing
                    if COFL_ask and COFL_secondQuestion:
                        if (COFL_answer == wx.ID_YES):
                            answerAux = YesNoCancelDialog(_(u'Do you ' \
                                u'want to overwrite everything?'))
                        else:
                            answerAux = YesNoCancelDialog(_(u'Do you ' \
                                u'want nothing to be overwrited?'))
                        # If canceled we don't extract anything
                        if (answerAux == wx.ID_CANCEL):
                            return None
                        # If yes selected, disable the user prompt
                        if (answerAux == wx.ID_YES):
                            COFL_ask = False
                        COFL_secondQuestion = False
                    # Ugly but it works
                    if COFL_ask and COFL_firstQuestion:
                        COFL_firstQuestion = False
                        COFL_secondQuestion = True
                    # Prompt the user for confirmation
                    if COFL_ask:
                        COFL_answer = YesNoCancelDialog(_(u'%s already exists.' \
                            u'\nDo you want to overwrite it?') % finalPath)
                        # If canceled we don't extract anything
                        if (COFL_answer == wx.ID_CANCEL):
                            return None
                        elif (COFL_answer != wx.ID_YES):
                            deleteList.append(i)
                        # Ok, we will overwrite it
                        else:
                            DeleteFile(finalPath)
                    # If not asking and no-overwrite mode, delete everything
                    elif (COFL_answer != wx.ID_YES):
                        deleteList.append(i)
                    # OR overwrite everything
                    else:
                        DeleteFile(finalPath)
        # Increase the index
        i += 1
    # Reverse the deleteList and delete them from the files list
    deleteList.reverse()
    for item in deleteList:
        del contents[item]
    return contents

def CheckFileExistsOnTree(file, treeCtrl, ocurrence=None):
    "Checks if a file exists into a treeCtrl"
    # Remove slashes at the end of the path
    if file[-1] == '/':
        file = file[:-1]
    # Get the subpaths for the file
    subPathChunks = file.split('/')
    # Get the root of the tree
    root = treeCtrl.GetRootItem()
    treeCurr = root
    # Process the file by the folders in it's path
    j = 0
    pathLenght = len(subPathChunks)
    found = None
    varContinue = True
    while ((varContinue) and (j < pathLenght)):
        j += 1
        subPath = '/'.join(subPathChunks[:j])
        # Check the items in the current level
        numSons = treeCtrl.GetChildrenCount(treeCurr, False)
        cookie = None
        found = False
        i = 0
        found = None
        while ((i < numSons) and (not found)):
            if i == 0:
                son, cookie = treeCtrl.GetFirstChild(treeCurr)
            else:
                son, cookie = treeCtrl.GetNextChild(treeCurr, cookie)
            # Get the content of the item
            # Returns a tuple (path, ocurrences, exists)
            data = treeCtrl.GetPyData(son)
            # Check if the data fits the current file's path
            # AS a file
            if ((data[0] == subPath) and ((not ocurrence) or (ocurrence == data[1]))):
                treeCurr = son
                found = 'f'
            # Or as a folder
            elif data[0] == subPath + '/':
                treeCurr = son
                found = 'd'
            i += 1
        # Stop if the subPath could not be found
        if found == None:
            varContinue = False
    # Return if the file/dir was found and it's id
    if varContinue:
        return (found, treeCurr)
    else:
        return (None, None)

def ConfirmOverwriteFilesArchive(files, path, treeCtrl, allowBoth):
    "Checks if any file exists in the archive and asks to overwrite"
    # allowBoth param sets if the format allows a file and a folder to
    # coexists with the same name
    
    # If the NO_CONFIRM_OVERWRITE is enabled, just overwrite all
    if Globals.NO_CONFIRM_OVERWRITE:
        return files
    # Else check for the files for being overwritten
    ask = True
    firstQuestion = True
    secondQuestion = False
    deleteList = []
    # Relative current path
    dirActualRel = path
    # Process every file
    i=-1
    j=-1
    for fileSet in files:
        j += 1
        for file in fileSet:
            i += 1
            deleteContent = False
            # Check if the file exists in the tree
            fileRoot = os.path.dirname(fileSet[0])
            fileRelAux = file[len(fileRoot)+1:]
            fileRel = os.path.join(path,fileRelAux)
            exists, nodeId = CheckFileExistsOnTree(fileRel, treeCtrl)
            # If we are processing a file
            if os.path.isfile(file):
                # If exists as a file
                if exists == 'f':
                    deleteContent = True
                # If exists as a folder
                elif (exists == 'd') and (not allowBoth):
                    WarningDialog(_(u'There is a folder with the same name\n' \
                        u'as the file that is being compressed.'))
                    deleteContent = True
            # If we are processing a folder
            else:
                # If exists as a file
                if (exists == 'f') and (not allowBoth):
                    WarningDialog(_(u'There is a file in with the same name\n' \
                        u'as the folder that is being compressed.'))
                    deleteContent = True
            if deleteContent:
                # The second time we give the option to overwrite 
                # everything or nothing
                if secondQuestion:
                    if (answer == wx.ID_YES):
                        answerAux = YesNoCancelDialog(_(u'Do you ' \
                            u'want to overwrite everything?'))
                    else:
                        answerAux = YesNoCancelDialog(_(u'Do you ' \
                            u'want nothing to be overwrited?'))
                    # If canceled we don't extract anything
                    if (answerAux == wx.ID_CANCEL):
                        files = []
                        return files
                    if (answerAux == wx.ID_YES):
                        ask = False
                        # If everything will be overwrited dont check again
                        if (answer == wx.ID_YES):
                            return files
                    secondQuestion = False
                # Ugly but it works
                if firstQuestion:
                    firstQuestion = False
                    secondQuestion = True
                # If we get "no" as answer we delete the file from the list
                if ask:
                    fileName = os.path.join(path,BasenameMod(file))
                    answer = YesNoCancelDialog(_(u'The file %s ' \
                        u'already exists in the archive.\nDo you want to ' \
                        u'overwrite it?') % fileName)
                    # If canceled we don't extract anything
                    if (answer == wx.ID_CANCEL):
                        files = []
                        return files
                    if (answer != wx.ID_YES):
                        deleteList.append((j,i))
                # If not asking, we are in "don't overwrite anything" mode
                else: 
                    deleteList.append((j,i))
    # Reverse the deleteList and delete them from the files list
    deleteList.reverse()
    for item in deleteList:
        del files[item[0]][item[1]]
    # Delete the sublists without items
    i = len(files)-1
    while i >= 0:
        if not files[i]:
            del files[i]
        i-=1
    return files
        
def AskForPassword(message=None):
    "Asks to the user for a password using a dialog"
    # If not message given, use the default one
    if not message:
        message = _(u'Enter the password')
    # It can be simple by now
    password = None
    if not Globals.NOGUI:
        Executor.hideDialog()
        if Globals.PARENT:
            Globals.PARENT.Raise()
        password = wx.GetPasswordFromUser(message, '', '')
        Executor.showDialog()
    # If X server is unavailable use the console
    else:
        password = getpass.getpass(
            (message).encode(sys.getfilesystemencoding(),'replace'))
    if (password == ''):
            password = None
    return password
    
def DeleteFile(file):   
    "This function can be used to delete files and folders"  
    if os.path.islink(file) or os.path.isfile(file):
        os.remove(file)
    # Folders are deleted recursively
    elif os.path.isdir(file):
        for root, dirs, files in os.walk(file, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                if os.path.islink(os.path.join(root, name)):
                    os.remove(os.path.join(root, name))
                else:
                    os.rmdir(os.path.join(root, name))
        os.rmdir(file)

def CreateFolder(dir):
    "Create a folder with full path"
    if not os.path.isdir(dir):
        chunks = dir.split('/')
        subchunk = '/'
        for chunk in chunks:
            subchunk = os.path.join(subchunk, chunk)
            if not os.path.isdir(subchunk):
                #os.mkdir(subchunk, stat.S_IRWXU) UMASK?
                os.mkdir(subchunk)

def BasenameMod(filename):
    "os.path.basename modified so it won't return an empty string"
    # Used mainly by progress dialogs
    if (len(filename) <= 1):
        return filename
    elif (filename[-1] == '/'):
        filename = filename[:-1]
    return os.path.basename(filename)

def Encode(text):
    "Encode texto to send it to pexpect or config files"
    return text.encode(sys.getfilesystemencoding(),'replace')

def Decode(text):
    "Decode a text received from the terminal"
    return text.decode(sys.getfilesystemencoding(),'replace')

def GetExtension(filename):
    "Returns the extension of a file name"
    if filename.rfind('.') != -1:
        return filename[filename.rfind('.')+1:]
    else:
        return ''

def WithoutExtension(filename):
    "Deletes the extension from a file name"
    if filename.rfind('.') != -1:
        return filename[:filename.rfind('.')]
    else:
        return filename
    
def IsInstalled(executable):
    "Returns true if the exec can be found in the system (it uses the PATH)"
    if (not executable) or (not pexpect.which(executable)):
        return False
    else:
        return True
    
def FileLink(origin, destination):
    "Creates a hard link of a file or duplicates a folder"
    if os.path.islink(origin) or os.path.isfile(origin):
        os.link(origin,os.path.join(destination,BasenameMod(origin)))
    # Folders are duplicated
    elif os.path.isdir(origin):
        destinationName = os.path.join(destination,BasenameMod(origin))
        if not os.path.isdir(destinationName):
            os.mkdir(destinationName)
            
def FileSymLink(origin, destination):
    "Creates a symbolic link of a file or duplicates a folder"
    if os.path.islink(origin) or os.path.isfile(origin):
        os.symlink(origin,os.path.join(destination,BasenameMod(origin)))
    # Folders are duplicated
    elif os.path.isdir(origin):
        destinationName = os.path.join(destination,BasenameMod(origin))
        if not os.path.isdir(destinationName):
            os.mkdir(destinationName)
    
def RecursiveLink(origin, destination):
    "Duplicates a file or a file tree by using hard links"
    if os.path.islink(origin) or os.path.isfile(origin):
        os.link(origin,os.path.join(destination,BasenameMod(origin)))
    # Folders are linked recursively
    elif os.path.isdir(origin):
        destinationName = os.path.join(destination,BasenameMod(origin))
        if not os.path.isdir(destinationName):
            os.mkdir(destinationName)
        for root, dirs, files in os.walk(origin, topdown=True):
            # Calculate the relative path of root
            destinationDir = root[len(origin):]
            if os.path.isabs(destinationDir):
                destinationDir = destinationDir[1:]
            # The files are linked
            for name in files:
                os.link(os.path.join(root, name), 
                    os.path.join(os.path.join(destinationName, destinationDir), name))
            # Folders are not linked (can't be done) but created
            for name in dirs:
                aux = os.path.join(os.path.join(destinationName, destinationDir), name)
                os.mkdir(aux)
                # Copy permisions and dates
                shutil.copystat(os.path.join(root,name), aux)
                
def RecursiveMove(origin, destination):
    "Moves a file or a folder with overwriting when needed"
    # When overwriting is not needed, we can just use shutil.move
    
    # Manage files and links
    if os.path.islink(origin) or os.path.isfile(origin):
        destinationName = os.path.join(destination,BasenameMod(origin))
        # Remove the target if it exists
        if os.path.lexists(destinationName):
            DeleteFile(destinationName)
        shutil.move(origin, destinationName)
    # Folders are moved recursively
    elif os.path.isdir(origin):
        destinationName = os.path.join(destination,BasenameMod(origin))
        # Create the target folder if it does not exist
        if not os.path.isdir(destinationName):
            # Delete posible files/links with the same path
            if os.path.lexists(destinationName):
                DeleteFile(destinationName)
            os.mkdir(destinationName)
        for root, dirs, files in os.walk(origin, topdown=True):
            # Calculate the relative path of root
            destinationDir = root[len(origin):]
            if os.path.isabs(destinationDir):
                destinationDir = destinationDir[1:]
            # The files are moved
            for name in files:
                aux = os.path.join(os.path.join(destinationName, destinationDir), name)
                # Overwrite existing files
                if os.path.lexists(aux):
                    DeleteFile(aux)
                shutil.move(os.path.join(root, name), aux)
            # Folders are not moved but created
            for name in dirs:
                aux = os.path.join(os.path.join(destinationName, destinationDir), name)
                if not os.path.isdir(aux):
                    # Delete posible files/links with the same path
                    if os.path.lexists(aux):
                        DeleteFile(aux)
                    os.mkdir(aux)
                    # Copy permisions and dates
                    shutil.copystat(os.path.join(root,name), aux)

def FileCopy(origin, destination):
    "Duplicates a file or a folder"
    destinationName = os.path.join(destination,BasenameMod(origin))
    # Process the simbolic links
    if os.path.islink(origin):
        os.symlink(os.readlink(origin), destinationName)
    # Process the files
    elif os.path.isfile(origin):
        shutil.copy2(origin,destinationName)
    # Process the folders
    elif os.path.isdir(origin):
        os.mkdir(destinationName)
        # Copy permisions and dates
        shutil.copystat(os.path.join(origin), destinationName)

def RecursiveCopy(origin, destination):
    "Duplicates a file or a file tree"
    destinationName = os.path.join(destination,BasenameMod(origin))
    # Process the simbolic links
    if os.path.islink(origin):
        os.symlink(os.readlink(origin), destinationName)
    # Process the files
    elif os.path.isfile(origin):
        shutil.copy2(origin,destinationName)
    # Process the folders
    elif os.path.isdir(origin):
        shutil.copytree(origin,destinationName,True)
    
def Beep():
    "If beep is enabled, makes a beep sound"
    # Beep cannot be performed if wx.App is not created
    if Globals.BEEP and not Globals.NOGUI:
        wx.Bell()
        
def ExecuteExternal(command):
    "Execute a command that is external to Tarumba"
    # Used to invoque other programs to open files
    subprocess.Popen(command,shell=True)
    
def IsGenericMultivolume(filename):
    "Returns true if the filename matches the multivolume pattern"
    if re.match('.*\.[0-9]+$', filename):
        return True
    else:
        return False
    
def GetGenericVolumes(filename):
    "Checks if a file is part of a generic multivolume and returns it's members"
    if IsGenericMultivolume(filename):
        dotPos = filename.rfind('.')+1
        lenSuffix = len(filename[dotPos:])
        suffixMask = '%0'+str(lenSuffix)+'i'
        prefix = filename[:dotPos]
        # Cycle through the existing files
        idx = 0
        volumes = []
        nextVol = prefix + (suffixMask % idx)
        while os.path.isfile(nextVol):
            volumes.append(nextVol)
            idx += 1
            nextVol = prefix + (suffixMask % idx)
        return volumes
    # If not multivolume, return None
    else:
        return None
    
def YesNoDialog(message, title=_(u'Question')):
    "Shows a yes/no dialog in graphical or text mode"
    # If wx available, use a MessageDialog
    if not Globals.NOGUI:
        question = wx.MessageDialog(Globals.PARENT, message, title,
            wx.YES_NO | wx.ICON_QUESTION)
        returnValue = question.ShowModal()
        question.Destroy()
        return returnValue
    # Else use standart input
    else:
        text = message+' ('+Globals.INPUT_YES+'/'+Globals.INPUT_NO+') ' 
        # Ask until a valid answer is given
        input = ''
        while ((input.upper() != Globals.INPUT_YES.upper()) and 
               (input.upper() != Globals.INPUT_NO.upper())):
            # The input/output is encoded using the standart
            sys.stdout.write((text).encode(
                sys.getfilesystemencoding(),'replace'))
            input = (sys.stdin.readline()).decode(
                sys.getfilesystemencoding(),'replace').strip()
        # Compare the input with the fixed (translated) strings
        if input.upper() == Globals.INPUT_YES.upper():
            return wx.ID_YES
        else:
            return wx.ID_NO
        
def YesNoCancelDialog(message, title=_(u'Question')):
    "Shows a yes/no/cancel dialog in graphical or text mode"
    # If wx available, use a MessageDialog
    if not Globals.NOGUI:
        question = wx.MessageDialog(Globals.PARENT, message, title,
            wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
        returnValue = question.ShowModal()
        question.Destroy()
        return returnValue
    # Else use standart input
    else:
        text = message+' ('+Globals.INPUT_YES+'/'+Globals.INPUT_NO+'/' \
            ''+Globals.INPUT_CANCEL+') ' 
        # Ask until a valid answer is given
        input = ''
        while ((input.upper() != Globals.INPUT_YES.upper()) and 
               (input.upper() != Globals.INPUT_NO.upper()) and
               (input.upper() != Globals.INPUT_CANCEL.upper())):
            # The input/output is encoded using the standart
            sys.stdout.write((text).encode(
                sys.getfilesystemencoding(),'replace'))
            input = (sys.stdin.readline()).decode(
                sys.getfilesystemencoding(),'replace').strip()
        # Compare the input with the fixed (translated) strings
        if input.upper() == Globals.INPUT_YES.upper():
            return wx.ID_YES
        elif input.upper() == Globals.INPUT_NO.upper():
            return wx.ID_NO
        else:
            return wx.ID_CANCEL
        
def ErrorDialog(message, title=_(u'Error')):
    "Shows an error dialog in graphical or text mode"
    # If wx available, use a MessageDialog
    if not Globals.NOGUI:
        dialog = wx.MessageDialog(Globals.PARENT, message,title,
            wx.OK | wx.ICON_ERROR)
        dialog.ShowModal()
        dialog.Destroy()
    # Else use standart output
    else:
        sys.stderr.write((title+': '+message+'\n').encode(
            sys.getfilesystemencoding(),'replace'))
            
def WarningDialog(message, title=_(u'Warning')):
    "Shows a warning dialog in graphical or text mode"
    # If wx available, use a MessageDialog
    if not Globals.NOGUI:
        dialog = wx.MessageDialog(Globals.PARENT, message,title,
            wx.OK | wx.ICON_WARNING)
        dialog.ShowModal()
        dialog.Destroy()
    # Else use standart output
    else:
        sys.stderr.write((title+': '+message+'\n').encode(
            sys.getfilesystemencoding(),'replace'))
            
def FileModeString(mode):
    "Simplified version of the filemodestring function in GNU coreutils"
    # I am very sorry for this blasphemy
    
    modeString = ''
    # Most common file types, so test for them first
    if stat.S_ISREG (mode):
        modeString += '-'
    elif stat.S_ISDIR (mode):
        modeString += 'd'
    # Other letters standardized by POSIX 1003.1-2004
    elif stat.S_ISBLK (mode):
        modeString += 'b'
    elif stat.S_ISCHR (mode):
        modeString += 'c'
    elif stat.S_ISLNK (mode):
        modeString += 'l'
    elif stat.S_ISFIFO (mode):
        modeString += 'p'
    # Other file types (though not letters) standardized by POSIX
    elif stat.S_ISSOCK (mode):
        modeString += 's'
    # Nonstandard file types are not included because they can't be handled with Python's stat module
    else:
        modeString += '?'
        
    # User - read
    if mode & stat.S_IRUSR:
        modeString += 'r'
    else:
        modeString += '-'
    # User - write
    if mode & stat.S_IWUSR:
        modeString += 'w'
    else:
        modeString += '-'
    # User - execute & SUID bit
    if mode & stat.S_ISUID:
        if mode & stat.S_IXUSR:
            modeString += 's'
        else:
            modeString += 'S'
    else:
        if mode & stat.S_IXUSR:
            modeString += 'x'
        else:
            modeString += '-'
    # Group - read
    if mode & stat.S_IRGRP:
        modeString += 'r'
    else:
        modeString += '-'
    # Group - write
    if mode & stat.S_IWGRP:
        modeString += 'w'
    else:
        modeString += '-'
    # Group - execute & SGID bit
    if mode & stat.S_ISGID:
        if mode & stat.S_IXGRP:
            modeString += 's'
        else:
            modeString += 'S'
    else:
        if mode & stat.S_IXGRP:
            modeString += 'x'
        else:
            modeString += '-'
    # Other - read
    if mode & stat.S_IROTH:
        modeString += 'r'
    else:
        modeString += '-'
    # Other - write
    if mode & stat.S_IWOTH:
        modeString += 'w'
    else:
        modeString += '-'
    # Other - execute & sticky bit
    if mode & stat.S_ISVTX:
        if mode & stat.S_IXOTH:
            modeString += 's'
        else:
            modeString += 'S'
    else:
        if mode & stat.S_IXOTH:
            modeString += 'x'
        else:
            modeString += '-'
    # Return value
    return modeString

