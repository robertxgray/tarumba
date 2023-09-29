# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Clipboard.py
# Purpose:      Tarumba's clipboard support.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Clipboard.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import Temporary
import CompressionManager
import CompressionDialog
import MainFrameMenu

import wx
import os
# Disabled because we don't delete the temporary files
#import sys
#import time

def DirCtrlCopy(event):
    "A file is copied from the file manager"
    # If None event we called it
    if event:
        event.StopPropagation()
    # Get the files being copied
    dirCtrl = Globals.PARENT.multiSelectionDirCtrl1
    files = wx.FileDataObject()
    filesAux = dirCtrl.GetPaths()
    i = 0
    for file in filesAux:
        files.AddFile(file)
        i+=1
    # If none selected, exit
    if len(filesAux) < 1:
        Utilities.Log(_(u'No files selected, nothing to be copied.'),
            Utilities.ERRO)
    else:
        # Send the files to the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(files)
            wx.TheClipboard.Close()
            # Information message to the user
            Utilities.Log(_(u'%s files or folders have been copied from the ' \
                u'filesystem.' % str(i)), Utilities.INFO)
        else:
            Utilities.Log(_(u'Cannot copy data, clipboard not ready.'),
                Utilities.ERRO)
         
def DirCtrlPaste(event):
    "One or more files are paste over the file manager"
    # If None event we called it
    if event:
        event.StopPropagation()
    # Get the files from the clipboard
    files = wx.FileDataObject()
    if wx.TheClipboard.Open():
        if not wx.TheClipboard.GetData(files):
            wx.TheClipboard.Close()
            return
        wx.TheClipboard.Close()
    else:
        Utilities.Log(_(u'Cannot paste data, clipboard not ready.'),
            Utilities.ERRO)
        return
    filenames = files.GetFilenames()
    # Information message to the user
    Utilities.Log(_(u'%s files or folders have been pasted to the ' \
        u'filesystem.' % str(len(filenames))), Utilities.INFO)
    # Get the currently selected item
    dirCtrl = Globals.PARENT.multiSelectionDirCtrl1
    filesAux = dirCtrl.GetPaths()
    # If not the only, something goes wrong
    if len(filesAux) != 1:
        Utilities.Log(_(u'Select the folder where to paste the files.'),
            Utilities.ERRO)
        return
    # Choose the destination for the files
    dirDestination = None
    if os.path.isdir(filesAux[0]):
        dirDestination = filesAux[0]
    elif os.path.isdir(os.path.dirname(filesAux[0])):
        dirDestination = os.path.dirname(filesAux[0])
    else:
        Utilities.Log(_(u'The selected target for paste is not valid.'),
            Utilities.ERRO)
        return
    # Confirm to overwrite the files
    totalFiles = []
    k = 0
    for file in filenames:
        confFilesAux = Utilities.RecursiveSelectionInFileSys(file)
        confFilesAux2 = []
        # Add / at the end of the folders
        for fileAux in confFilesAux:
            if os.path.isdir(fileAux):
                confFilesAux2.append(fileAux+'/')
            else:
                confFilesAux2.append(fileAux)
        # Format the files as taken from the treeListCtrl
        # But include a hint to restore it againt
        for fileAux in confFilesAux2:
            totalFiles.append([fileAux,k])
        k+=1
    confTotalFiles = Utilities.ConfirmOverwriteFilesLocal(
        totalFiles, dirDestination)
    # Restore the list of files to the original format
    confTotalFiles2 = []
    for numFiles in range(k):
        confTotalFiles2.append([])
    currFile = None
    for file in confTotalFiles:
        confTotalFiles2[file[1]].append(file[0])
    # Copy the files
    try:
        i = 0
        for confFiles in confTotalFiles2: 
            i += 1
            # This can happen when we select not to overwrite
            if len(confFiles) < 1:
                continue
            # Get the base folder for the pack
            baseFileName = confFiles[0]
            if baseFileName[-1] == '/':
                baseFileName = baseFileName[:-1]
            baseFolder = os.path.dirname(baseFileName)
            for file in confFiles:
                # This avoids some odd errors
                if not os.path.lexists(file):
                    continue 
                # Remove / at the end of the folders
                if os.path.isdir(file):
                    file = file[:-1] 
                # Calculate the full destination path for the file
                fileDirnameAux = os.path.dirname(file)+'/'
                fullDirDestinationAux = fileDirnameAux[len(baseFolder)+1:]
                fullDirDestination = os.path.join(dirDestination,
                    fullDirDestinationAux)  
                fullDestinationName = os.path.join(fullDirDestination,
                    Utilities.BasenameMod(file))
                # Skip it if it's a folder and exists
                if os.path.isdir(fullDestinationName):
                    continue
                # Skip if source and target are the same file
                if os.path.samefile(fullDirDestination, os.path.dirname(file)):
                    continue
                Utilities.FileCopy(file, fullDirDestination)
        # Rebuild the file system
        dirCtrl.ReCreateTree()
        dirCtrl.SetPath(dirDestination)
    # If error, show it and end
    except OSError, e:
        Utilities.Log(_(u'Error on paste files') + ': ' + unicode(e),
            Utilities.ERRO)
            
def TreeListCopy(event):
    "A file is copied from the compressed file"
    # If None event we called it
    if event:
        event.StopPropagation()
    try:
        treeList = Globals.PARENT.treeListCtrl1
        # Temporary folder for the extraction
        dirTmp = Temporary.tmpDir()
        # If the root is selected, get it's children
        root = treeList.GetRootItem()
        if treeList.IsSelected(root):
            treeList.UnselectAll()       
            childNum = treeList.GetChildrenCount(root, False)
            cookie = None
            for i in range(childNum):
                if i == 0:
                    child, cookie = treeList.GetFirstChild(root)
                else:
                    child, cookie = treeList.GetNextChild(root, cookie)    
                treeList.SelectItem(child, child, False)      
        # Get the files being dragged
        files = wx.FileDataObject()
        selection = treeList.GetSelections()
        for file in selection:
            filename = os.path.join(dirTmp,Utilities.BasenameMod(
                    treeList.GetPyData(file)[0]))
            files.AddFile(filename)
        # If none selected, exit
        if len(selection) < 1:
            Utilities.Log(_(u'No files selected, nothing to be copied.'),
                Utilities.ERRO)
            Utilities.Beep()
            return
        # Decompress selected files
        error, output = CompressionManager.extract(Globals.file, 
            treeList, dirTmp)
        # Show the result
        if error:
            Utilities.Log(output,Utilities.ERRO)
        else:
            Utilities.Log(output,Utilities.INFO)
        # Send the files to the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(files)
            wx.TheClipboard.Close()
            # Information message to the user
            Utilities.Log(_(u'%(number)s files or folders have been copied from ' \
            u'%(filename)s.') % {'number':str(len(selection)),
            'filename':Utilities.BasenameMod(Globals.file)}, Utilities.INFO)
        else:
            Utilities.Log(_(u'Cannot copy data, clipboard not ready.'),
                Utilities.ERRO)
    finally:
        # Delete the temporary folder
        # Disabled to avoid problems because of slow copy
        #if os.fork() == 0:
        #    time.sleep(10)
        #    Utilities.DeleteFile(dirTmp)
        #    sys.exit(0)
        pass

def TreeListPaste(event):
    "One or more files are pasted over the compressed file" 
    # If None event we called it
    if event:
        event.StopPropagation()
    flagNewFile = False
    # Get the files from the clipboard
    files = wx.FileDataObject()
    if wx.TheClipboard.Open():
        if not wx.TheClipboard.GetData(files):
            wx.TheClipboard.Close()
            return
        wx.TheClipboard.Close()
    else:
        Utilities.Log(_(u'Cannot paste data, clipboard not ready.'),
            Utilities.ERRO)
        Utilities.Beep()
        return
    filenames = files.GetFilenames()
    # Information message to the user
    Utilities.Log(_(u'%s files or folders have been pasted.' \
        '' % str(len(filenames))), Utilities.INFO)
    # Get the selected file
    treeList = Globals.PARENT.treeListCtrl1
    filesAux = treeList.GetSelections()
    # If more than one, something goes wrong
    if len(filesAux) > 1:
        Utilities.Log(_(u'Select the folder where to paste the files.'),
            Utilities.ERRO)
        Utilities.Beep()
        return
    # If zero, then add the files to the root
    elif len(filesAux) < 1:
        dirDestination = ''
    else:
        # Choose the destination path for the files
        dirDestination = treeList.GetPyData(filesAux[0])[0] 
        # If it's a file, the destination is it's parent
        if not dirDestination[-1] == '/':
            dirDestination = os.path.dirname(dirDestination)
            
    # If no file loaded and is acompressed file, open it
    if Globals.file == Globals.NO_FILE:
        formatAux = CompressionManager.formatByExtension(filenames[0])
        if formatAux and (len(filenames) == 1):
            try :
                # Changes the cursor to the busy cursor
                Globals.PARENT.busy = wx.BusyCursor()
                # Set the name of the file and reset the options
                Globals.file = filenames[0]
                Globals.compressionOptions = Globals.CompressionOptions()
                # Shows the selected file in the TreeListCtrl
                error, output = CompressionManager.list(
                    Globals.file, Globals.PARENT.treeListCtrl1)
                # Show the result
                if error:
                    Utilities.Log(output,Utilities.ERRO)
                else:
                    Utilities.Log(output,Utilities.INFO)
                # If everything is Ok, change the tile
                if not error:   
                    Globals.PARENT.staticText2.SetLabel(
                        Utilities.BasenameMod(Globals.file))
                # Otherwise change to "no file" mode
                else:
                    MainFrameMenu.closeFile(None)
                # PATCH: Fixes the expand problem in the treeListCtrl
                Globals.PARENT.treeListCtrl1.ExpandAll(
                    Globals.PARENT.treeListCtrl1.GetRootItem())
            finally :
                # Sets the normal cursor again
                if Globals.PARENT.busy:
                    del Globals.PARENT.busy
            return
            
    # If no file loaded and normal file or more than one file, 
    # show the dialog to create new
        else:
            Globals.file = filenames[0]
            dialog = CompressionDialog.create(Globals.PARENT,
                ((len(filenames)>1) or os.path.isdir(filenames[0])))
            if dialog.ShowModal() != wx.ID_OK:
                Globals.file = Globals.NO_FILE
                return
            else:
                Globals.PARENT.staticText2.SetLabel(
                    Utilities.BasenameMod(Globals.file))
                flagNewFile = True
                    
    try:
        # Add the files with the compression manager
        error, output = CompressionManager.add(
            Globals.file, filenames, dirDestination, treeList, 
            Globals.compressionOptions)
        # Show the result
        if error:
            Utilities.Log(output,Utilities.ERRO)
        else:
            Utilities.Log(output,Utilities.INFO)
        # Reload the file in the TreeListCtrl
        error, output = CompressionManager.list(
            Globals.file, treeList)
        # If error, go to "no file" mode and tell the user
        if error:
            MainFrameMenu.closeFile(None)
		# PATCH: Fixes the expand problem in the treeListCtrl
        treeList.ExpandAll(treeList.GetRootItem())
        # Updates the file system (to show the new file)
        if flagNewFile:
            Globals.PARENT.multiSelectionDirCtrl1.ReCreateTree()
    # If it fails, show error and exit
    except OSError, e:
        Utilities.Log(_(u'Error on paste files') + ': ' + unicode(e),
            Utilities.ERRO)


