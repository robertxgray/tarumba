# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Compressor.py
# Purpose:      Common interface for the compressors.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Compressor.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import Executor
import Temporary

import wx
import os
import sys
import shutil
import re

class Compressor:
    "Common interface for the compressors"
    
######################
## ABSTRACT METHODS ##
######################
    
    def prepareTreeListCtrl(self, treeListCtrl):
        "Prepares the TreeListCtrl to show the contents of the file"
        pass
    
    def processOutputInTreeListCtrl(self, filename, output, treeListCtrl):
        "Add the contents of the compressed file to the TreeListCtrl"
        pass
    
    def listCommand(self, filename):
        "Command to list the contents of the compressed file"
        pass
    
    def extractCommand(self, filename, contents):
        "Command to extract the contents from the file"
        pass
   
    def extractCommandParseOutput(self, text=''):
        "How to parse one line of programs output when extracting"
        pass
   
    def addCommand(self, filename, contents, options):
        "Command to add the contents to the file"
        pass
    
    def addCommandParseOutput(self, text=''):
        "How to parse one line of programs output when adding"
        pass
    
    def deleteCommand(self, filename, contents, options):
        "Command to delete the contents from the file"
        pass
    
    def renameCommand(self, filename, contents, newname, options):
        "Command to rename the contents of the file"
        pass
    
    def testCommand(self, filename):
        "Command to test the file integrity"
        pass
    
    def fixCommand(self, filename, newFilename):
        "Command to fix the file"
        pass
    
    def compressionLevels(self):
        "Returns the available compression levels"
        pass
    
    def canCompress(self):
        "True if we can create or modify archives with this format"
        pass
        
    def canEncrypt(self):
        "True if the format allows encryption"
        pass

    def canSplit(self):
        "True if the format can be splitted into volumes"
        pass
    
    def canPack(self):
        "True if the format can store multiple files"
        pass
    
    def canRename(self):
        "True if the format can rename it's content efficiently"
        pass
    
    def canAllowFilesSameName(self):
        "True if the format can store files with the same name"
        pass
    
    def canAllowFileDirSameName(self):
        "True if the format can store files and folders with the same name"
        pass
    
    def extensions(self):
        "Returns the extensions supported by the compression format"
        pass
    
    def enabled(self):
        "If not enabled we can't manage files with this format"
        pass
    
##########################
## NOT ABSTRACT METHODS ##
##########################

    def list(self, filename, execFunction=Executor.execute, env=None):
        "Shows the contents of a file in a treeListCtrl"
        # Gets and executes the external command
        command = self.listCommand(filename)
        error, output = execFunction(command, _(u'Processing file'), 
            unknownProgress=True, env=env)
        return (error, output)
            
    def extract(self, filename, contents, path, execFunction=Executor.execute, env=None): 
        "Extracts the contents to the path"
        # End if no contents given
        if not contents:
            return (0, _(u'0 files extracted.'))
        # Variables
        error = 0
        numFiles = 0
        commands = []
        numToExtract = 0
        totalFiles = 0
        # Save the current directory
        currDir = os.getcwd()
        # Create a temporary folder to duplicate the files
        temporary, sameFileSys = Temporary.tmpDirInFilesys(path)
        Utilities.CreateFolder(temporary)
        # Enter the temporary folder
        commands.append((Executor.CHDIR,[temporary],''))
        os.chdir(temporary)
        # Process every selected content
        for contentPack in contents:
            relativeContents = []
            # Process the contents of the archive
            for con in contentPack:
                # Ignore empty entries (root)
                if con[0]:
                    relativeContent = os.path.join(temporary, con[0])
                    # If it's a folder, create it
                    if (con[1] == 0):
                        Utilities.CreateFolder(relativeContent)
                    # If it's a file, extract it
                    else:
                        relativeContents.append(con)
                        numToExtract += 1
                    totalFiles += 1
            commands += self.extractCommand(filename, relativeContents)
        # The progress range can only be accurate if the parser is defined
        if self.extractCommandParseOutput() is not None:
            totalProgressAux = numToExtract
        else:
            totalProgressAux = None
        # Execute external commands
        error, output = execFunction(commands, 
            _(u'Uncompressing %s') % Utilities.BasenameMod(filename),
            parser=self.extractCommandParseOutput, totalProgress=totalProgressAux, env=env)
        # If execution is correct, move the files to the destination folder
        if not error:
            j = 0
            for contentPack in contents:
                # If the content is not the root, just move it
                if contentPack[0][0]:
                    relativeContent = os.path.join(temporary, contentPack[0][0])
                    shutil.move(relativeContent, path)
                # The root cannot be moved but it's contents
                else:
                    extractedItems = os.listdir(temporary)
                    for item in extractedItems:
                        relativeItem = os.path.join(temporary, item)
                        Utilities.RecursiveMove(relativeItem, path)
                j += 1
            # Restore the initial path
            os.chdir(currDir)
            # Delete temporary folder
            Utilities.DeleteFile(temporary)
            return (error, _(u'%s files extracted.') % totalFiles)
        # If execution had errors, return error message
        else:
            # Restore the initial path
            os.chdir(currDir)
            # Delete temporary folder
            Utilities.DeleteFile(temporary)
            return (error, _(u'Error when extracting files') + ': ' \
                '' + '\n'.join(output))
        
    def add (self, filename, contents, path, options, execFunction=Executor.execute, env=None):
        "Adds the contents to the current compressed file"
        error = 0
        numFiles = 0
        relativeContents = []
        commands = []
        # Save the current directory
        currDir = os.getcwd()
        # Create a temporary folder to duplicate the files
        # Use the same filesystem as the first content and check it again later
        temporary, sameFileSys = Temporary.tmpDirInFilesys(contents[0][0])
        dirDestination = os.path.join(temporary,path)
        Utilities.CreateFolder(dirDestination)
        # Enter the temporary folder
        commands.append((Executor.CHDIR,[temporary],''))
        os.chdir(temporary)
        # Process every group of archive contents
        j = 0
        for contentPack in contents:
            # Process the contents of the archive
            i=0
            for con in contentPack:
                # Check that the file exits and is not a special file
                # This avoids uncontroled errors ie. when adding sockets
                if (not os.path.isfile(con)) and (not os.path.isdir(con)):
                    # Restore the initial path
                    os.chdir(currDir)
                    # Delete temporary folder
                    Utilities.DeleteFile(temporary)
                    return (1, _(u'%s does not exist or is not a regular file.') % con)
                # If we are processing the "main" file/dir
                if i == 0:
                    conName = os.path.join(path, Utilities.BasenameMod(con))
                    relativeContents.append(conName)
                # Else calculate the relative temporary path
                else: 
                    conName = os.path.join(path, con[len(os.path.dirname(contentPack[0][:-1]))+1:])
                dirDestinationCon = os.path.join(temporary, os.path.dirname(conName))
                # Check if we continue in the same file system
                sameFileSys = Temporary.getFileSysOf(dirDestinationCon) == Temporary.getFileSysOf(con)
                # Use symlinks when possible
                if Globals.FOLLOW_LINKS:
                    Utilities.FileSymLink(con, dirDestinationCon)
                else:
                    # if they are in the same filesystem, use hard links
                    if sameFileSys:
                        Utilities.FileLink(con, dirDestinationCon)
                    # If not, we need to copy
                    else:
                        Utilities.FileCopy(con, dirDestinationCon)  
                # Increment indexes
                i += 1
                j += 1
        # Get the compressor command for the contents
        commands += self.addCommand(filename, relativeContents, options)
        # The progress range can only be accurate if the parser is defined
        if self.extractCommandParseOutput() is not None:
            totalProgressAux = j
        else:
            totalProgressAux = None
        # Execute the commands. Show the output when creating multiple volumes
        error, output = execFunction(commands, _(u'Compressing %s') % Utilities.BasenameMod(filename),
            showOutput=options.volumes, parser=self.addCommandParseOutput, totalProgress=totalProgressAux, env=env)
        # Rename Globals.file to the first volume when using generic volumes
        if (not error) and options.volumes and (not os.path.isfile(Globals.file)) and os.path.isfile(Globals.file+'.000'):
            Globals.file = Globals.file+'.000'
        # Restore the initial path
        os.chdir(currDir)
        # Delete temporary folder
        Utilities.DeleteFile(temporary)
        # If the execution is Ok, return Ok message
        if not error:
            return (error, _(u'%s files compressed.') % j)
        # If execution had errors, return error message
        else:
            return (error, _(u'Error when compressing files') + ': ' \
                '' + '\n'.join(output))
   
    def delete (self, filename, contents, options, execFunction=Executor.execute, env=None):
        "Deletes the contents from the current compressed file"
        # Get and execute the external command
        command = self.deleteCommand(filename, contents, options)
        error, output = execFunction(command,
            _(u'Deleting contents from %s') % Utilities.BasenameMod(filename), 
            unknownProgress=True, env=env)
        # If the execution is Ok, return Ok message
        if not error:
            return (error, _(u'%s files deleted.') % len(contents))
        # If execution had errors, return error message
        else:
            return (error, _(u'Error when deleting files') + '' \
                ': ' + '\n'.join(output))
                
    def rename (self, filename, contents, newname, options, execFunction=Executor.execute, env=None):
        "Renames the content to the newname"
        # Get and execute the external command
        command = self.renameCommand(filename, contents, newname, options)
        error, output = execFunction(command,
            _(u'Renaming %(oldname)s to %(newname)s') % 
                {'oldname':contents[0][0], 'newname':newname},
            unknownProgress=True, env=env)
        # If the execution is Ok, return Ok message
        if not error:
            oldnameAux = contents[0][0]
            newnameAux = newname
            # Delete slashes at the end
            if oldnameAux[-1] == '/':
                oldnameAux = oldnameAux[:-1]
            # Delete slashes at the end
            if newnameAux[-1] == '/':
                newnameAux = newnameAux[:-1]
            return (error, _(u'%(oldname)s renamed to %(newname)s')
                % {'oldname':oldnameAux, 'newname':newnameAux})
        # If execution had errors, return error message
        else:
            return (error, _(u'Error in the renaming operation') + '' \
                ': ' + '\n'.join(output))
                
    def test (self, filename, execFunction=Executor.execute, env=None):
        "Test the integrity of the current compressed file"
        # Get and execute the external command
        command = self.testCommand(filename)
        # Add a comment to the end
        command += [('Echo.py', [_(u'File test OK - No errors found.')],
            _(u'Testing the integrity of the file'))]
        error, output = execFunction(command,
            _(u'Testing the integrity of the file'), showOutput = True, env=env)
        return (error, '')

    def fix (self, filename, newFilename, execFunction=Executor.execute, env=None):
        "Fix the current compressed file"
        # Get and execute the external command
        command = self.fixCommand(filename, newFilename)
        # Add a comment to the end
        command += [('Echo.py', [_(u'End of file repairing operations.')], 
            _(u'Fixing file'))]
        error, output =  execFunction(command, _(u'Fixing file'), 
            showOutput = True, env=env)
        return (error, '')

        
