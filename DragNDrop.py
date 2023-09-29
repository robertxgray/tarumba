# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         DragNDrop.py
# Purpose:      Tarumba's drag and drop support.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: DragNDrop.py $
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

# Flag to enable or disable dropping files on the TreeListCtrl
READONLY = False

def InitDragDropDirCtrl(parent, dirCtrl):
    "Asociate drag and drop events from the file manager"
    
    # DropTarget class for the DirCTrl
    class DirCtrlFileDropTarget(wx.FileDropTarget):
        def OnDropFiles(self, x, y, filenames):
            return DirCtrlDrop(filenames)
        def OnDragOver(self, x, y, d):
            return DirCtrlDragOver(x, y, d)

    global __theDirCtrl
    __theDirCtrl = dirCtrl
    # Alternative DirCtrl
    if Globals.ALTERNATIVE_TREEVIEW:
        # Asociate drag events on the DirCtrl
        wx.EVT_TREE_BEGIN_DRAG(parent, dirCtrl.GetTreeCtrl().GetTreeCtrl().GetId(), DirCtrlDrag)
        wx.EVT_LIST_BEGIN_DRAG(parent, dirCtrl.GetListCtrl().GetId(), DirCtrlDrag)
        # Set the DirCtrl as the origin for the dragNdrop
        global __dirCtrlDropSource1
        global __dirCtrlDropSource2
        __dirCtrlDropSource1 = wx.DropSource(dirCtrl.GetTreeCtrl().GetTreeCtrl())
        __dirCtrlDropSource2 = wx.DropSource(dirCtrl.GetListCtrl())
        # Asociate drop events on the DirCtrl
        dirCtrl.GetTreeCtrl().SetDropTarget(DirCtrlFileDropTarget())
        dirCtrl.GetListCtrl().SetDropTarget(DirCtrlFileDropTarget())
    # Old DirCtrl
    else:
        # Asociate drag events on the DirCtrl
        wx.EVT_TREE_BEGIN_DRAG(parent, dirCtrl.GetTreeCtrl().GetId(), DirCtrlDrag)
        # Set the DirCtrl as the origin for the dragNdrop
        global __dirCtrlDropSource
        __dirCtrlDropSource = wx.DropSource(dirCtrl.GetTreeCtrl())
        # Asociate drop events on the DirCtrl
        dirCtrl.SetDropTarget(DirCtrlFileDropTarget())
        
def InitDragDropTreeList(parent, treeListCtrl):
    "Asociate drag and drop events from the compressed file"
    
    # DropTarget class for the TreeList
    class TreeListFileDropTarget(wx.FileDropTarget):
        def OnDropFiles(self, x, y, filenames):
            return TreeListDrop(filenames)
        def OnDragOver(self, x, y, d):
            return TreeListDragOver(x, y, d)
        
    global __theTreeList
    __theTreeList = treeListCtrl
    # Alternative DirCtrl
    if Globals.ALTERNATIVE_TREEVIEW:
        # Asociate drag events on the DirCtrl
        wx.EVT_TREE_BEGIN_DRAG(parent, treeListCtrl.GetTreeCtrl().GetId(), TreeListDrag)
        wx.EVT_LIST_BEGIN_DRAG(parent, treeListCtrl.GetListCtrl().GetId(), TreeListDrag)
        # Set the DirCtrl as the origin for the dragNdrop
        global __treeListDropSource1
        global __treeListDropSource2
        __treeListDropSource1 = wx.DropSource(treeListCtrl.GetTreeCtrl())
        __treeListDropSource2 = wx.DropSource(treeListCtrl.GetListCtrl())
        # Asociate drop events on the DirCtrl
        treeListCtrl.GetTreeCtrl().SetDropTarget(TreeListFileDropTarget())
        treeListCtrl.GetListCtrl().SetDropTarget(TreeListFileDropTarget())  
    # Old DirCtrl
    else:
        # Asociate drag events on the TreeListCtrl
        wx.EVT_TREE_BEGIN_DRAG(parent, treeListCtrl.GetId(), TreeListDrag)
        # Set the TreeList as the origin for the dragNdrop
        global __treeListDropSource
        __treeListDropSource = wx.DropSource(treeListCtrl)
        # Asociate drop events on the TreeList
        treeListCtrl.SetDropTarget(TreeListFileDropTarget()) 

def DirCtrlDrag(event):
    "A file is dragged from the file manager"
    # If None event we called it
    if event:
        event.StopPropagation()
    # Get the files being dragged
    global __theDirCtrl
    files = wx.FileDataObject()
    filesAux = __theDirCtrl.GetPaths()
    i = 0
    for file in filesAux:
        files.AddFile(file)
        i+=1
    # Information message to the user
    Utilities.Log(_(u'%s files or folders have been dragged from the ' \
            u'filesystem.' % str(i)), Utilities.INFO)
    # Begin the drag N drop
    if Globals.ALTERNATIVE_TREEVIEW:
        # DirCtrl
        if event.GetEventType() == wx.EVT_TREE_BEGIN_DRAG.typeId:
            global __dirCtrlDropSource1
            __dirCtrlDropSource1.SetData(files)
            __dirCtrlDropSource1.DoDragDrop()
        # ListCtrl
        else:
            global __dirCtrlDropSource2
            __dirCtrlDropSource2.SetData(files)
            __dirCtrlDropSource2.DoDragDrop()
    # Old DirCtrl
    else:
        global __dirCtrlDropSource
        __dirCtrlDropSource.SetData(files)
        __dirCtrlDropSource.DoDragDrop()
        
def DirCtrlDragOver(x, y, d):
    "A file is dragged over the file manager"
    global __theDirCtrl
    if Globals.ALTERNATIVE_TREEVIEW:
        # DirCtrl
        if wx.FindWindowAtPointer() == __theDirCtrl.GetTreeCtrl().GetTreeCtrl():
            treeAux = __theDirCtrl.GetTreeCtrl().GetTreeCtrl()
            item, flags = treeAux.HitTest(wx.Point(x,y))
            # Select the file under the mouse
            selAux = treeAux.GetSelections()
            if not ((len(selAux) == 1) and (selAux[0] == item)):
                treeAux.UnselectAll()
                treeAux.SelectItem(item)
                treeAux.ScrollTo(item)
        # ListCtrl
        else:
            listAux = __theDirCtrl.GetListCtrl()
            item, flags = listAux.HitTest(wx.Point(x,y))
            # Select the file under the mouse
            selAux = listAux.GetFirstSelected()
            if not ((listAux.GetSelectedItemCount() == 1) and (selAux == item)):
                # Unselect all
                oldSel = listAux.GetFirstSelected()
                while oldSel >= 0:
                    listAux.Select(oldSel, False)
                    oldSel = listAux.GetNextSelected(oldSel)
                listAux.Select(item)
                listAux.EnsureVisible(item)
    # Old DirCtrl
    else:
        # Get the file under the mouse
        treeAux = __theDirCtrl.GetTreeCtrl()
        item, flags = treeAux.HitTest(wx.Point(x,y))
        # Select the file under the mouse
        selAux = treeAux.GetSelections()
        if not ((len(selAux) == 1) and (selAux[0] == item)):
            treeAux.UnselectAll()
            treeAux.SelectItem(item)
            treeAux.ScrollTo(item)
    return d            
             
def DirCtrlDrop(filenames):
    "One or more files are drop over the file manager"
    # Information message to the user
    Utilities.Log(_(u'%s files or folders have been dropped to the ' \
        u'filesystem.' % str(len(filenames))), Utilities.INFO)
    # Get the currently selected item
    global __theDirCtrl
    filesAux = __theDirCtrl.GetPaths()
    # If not the only, something goes wrong
    if len(filesAux) != 1:
        Utilities.Log(_(u'Select the folder where to drop the files.'), Utilities.ERRO)
        return wx.DragNone
    # Choose the destination for the files
    dirDestination = None
    if os.path.isdir(filesAux[0]):
        dirDestination = filesAux[0]
    elif os.path.isdir(os.path.dirname(filesAux[0])):
        dirDestination = os.path.dirname(filesAux[0])
    else:
        Utilities.Log(_(u'The selected target for drop is not valid.'), Utilities.ERRO)
        return wx.DragNone
    # Avoid messages when all source and destination files are the same
    sourceEqDest = True
    for file in filenames:
        if (os.path.dirname(file) != dirDestination):
            sourceEqDest = False
    if sourceEqDest:
        return wx.DragNone
    # It is easy to drag-and-drog by mistake. Ask for confirmation
    answer = Utilities.YesNoDialog(_('Do you want to copy the files to\n%s?') % dirDestination,
        _('Copy confirmation'))
    if (answer != wx.ID_YES):
        return wx.DragCancel
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
    confTotalFiles = Utilities.ConfirmOverwriteFilesLocal(totalFiles, dirDestination, firstCall=True)
    # If confTotalFiles is none, the user pressed Cancel
    if not confTotalFiles:
        return wx.DragNone
    # Restore the list of files to the original format
    confTotalFiles2 = []
    for numFiles in range(k):
        confTotalFiles2.append([])
    currFile = None
    for file in confTotalFiles:
        confTotalFiles2[file[1]].append(file[0])
    # Copy the files
    try:
        for confFiles in confTotalFiles2: 
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
                fullDirDestination = os.path.join(dirDestination, fullDirDestinationAux)  
                fullDestinationName = os.path.join(fullDirDestination, Utilities.BasenameMod(file))
                # Skip it if it's a folder and exists
                if os.path.isdir(fullDestinationName):
                    continue
                # Skip if source and target are the same file
                if os.path.samefile(fullDirDestination, os.path.dirname(file)):
                    continue
                Utilities.FileCopy(file, fullDirDestination)
        # Rebuild the file system
        __theDirCtrl.ReCreateTree()
        __theDirCtrl.SetPath(dirDestination)
        # End Ok
        return wx.DragCopy
    # If error, show it and end
    except OSError, e:
        Utilities.Log(_(u'Error on drop files') + ': ' + unicode(e),
            Utilities.ERRO)
        return wx.DragError
    
def TreeListDrag(event):
    "A file is dragged from the compressed file"
    # If None event we called it
    if event:
        event.StopPropagation()
    try:
        global __theTreeList
        # Temporary folder for the extraction
        dirTmp = Temporary.tmpDir()
        # If the root is selected, get it's children
        root = __theTreeList.GetRootItem()
        if __theTreeList.IsSelected(root):
            __theTreeList.UnselectAll()       
            childNum = __theTreeList.GetChildrenCount(root, False)
            cookie = None
            for i in range(childNum):
                if i == 0:
                    child, cookie = __theTreeList.GetFirstChild(root)
                else:
                    child, cookie = __theTreeList.GetNextChild(root, cookie)    
                __theTreeList.SelectItem(child, child, False)      
        # Get the files being dragged
        files = wx.FileDataObject()
        selection = __theTreeList.GetSelections()
        for file in selection:
            filename = os.path.join(dirTmp,Utilities.BasenameMod(__theTreeList.GetPyData(file)[0]))
            files.AddFile(filename)
        # Decompress selected files
        error, output = CompressionManager.extract(Globals.file, __theTreeList, dirTmp)
        # Show the result
        if error:
            Utilities.Log(output,Utilities.ERRO)
        else:
            Utilities.Log(output,Utilities.INFO)
        # Information message to the user
        Utilities.Log(_(u'%(number)s files or folders have been dragged from ' \
            u'%(filename)s.') % {'number':str(len(selection)),
            'filename':Utilities.BasenameMod(Globals.file)}, Utilities.INFO)
        # Begin the drag N drop
        if Globals.ALTERNATIVE_TREEVIEW:
            # DirCtrl
            if event.GetEventType() == wx.EVT_TREE_BEGIN_DRAG.typeId:
                global __treeListDropSource1
                __treeListDropSource1.SetData(files)
                __treeListDropSource1.DoDragDrop()
            # ListCtrl
            else:
                global __treeListDropSource2
                __treeListDropSource2.SetData(files)
                __treeListDropSource2.DoDragDrop()
        # Old DirCtrl
        else:
            global __treeListDropSource
            __treeListDropSource.SetData(files)
            __treeListDropSource.DoDragDrop()
    finally:
        # Delete the temporary folder
        # Disabled to avoid problems because of slow copy
        #if os.fork() == 0:
        #    time.sleep(10)
        #    Utilities.DeleteFile(dirTmp)
        #    sys.exit(0)
        pass

def TreeListDragOver(x, y, d):
    "A file is dragged over the compressed file"
    global READONLY
    # Cancel the drag operation if readonly
    if READONLY:
        return wx.DragNone
    # If no compressed file loaded, exit or the computer explodes
    global __theTreeList
    if not __theTreeList.GetRootItem():
        return d
    if Globals.ALTERNATIVE_TREEVIEW:
        # DirCtrl
        if wx.FindWindowAtPointer() == __theTreeList.GetTreeCtrl():
            treeAux = __theTreeList.GetTreeCtrl()
            item, flags = treeAux.HitTest(wx.Point(x,y))
            # Select the file under the mouse
            selAux = treeAux.GetSelections()
            if not ((len(selAux) == 1) and (selAux[0] == item)):
                treeAux.UnselectAll()
                treeAux.SelectItem(item)
                treeAux.ScrollTo(item)
        # ListCtrl
        else:
            listAux = __theTreeList.GetListCtrl()
            item, flags = listAux.HitTest(wx.Point(x,y))
            # Select the file under the mouse
            selAux = listAux.GetFirstSelected()
            if not ((listAux.GetSelectedItemCount() == 1) and (selAux == item)):
                # Unselect all
                oldSel = listAux.GetFirstSelected()
                while oldSel >= 0:
                    listAux.Select(oldSel, False)
                    oldSel = listAux.GetNextSelected(oldSel)
                listAux.Select(item)
                listAux.EnsureVisible(item)
    # Old DirCtrl
    else: 
        # Get the file under the mouse
        treeAux = __theTreeList
        item, flags, cols = treeAux.HitTest(wx.Point(x,y))
        # Select the file under the mouse
        selAux = treeAux.GetSelections()
        if not ((len(selAux) == 1) and (selAux[0] == item)):
            treeAux.UnselectAll()
            treeAux.SelectItem(item)
            treeAux.ScrollTo(item)
    return d  

def TreeListDrop(filenames):
    "One or more files are drop over the compressed file"
    # Information message to the user
    Utilities.Log(_(u'%s files or folders have been dropped.' % str(len(filenames))), Utilities.INFO) 
    flagNewFile = False  
    # Get the selected file
    global __theTreeList
    filesAux = __theTreeList.GetSelections()
    # If zero, then add the files to the root
    if len(filesAux) < 1:
        folder = ''
    else:
        # Choose the destination path for the files
        folderInfo = __theTreeList.GetPyData(filesAux[0])
        folder = folderInfo[0]
        # If it's a file, the destination is it's parent
        if not folder[-1] == '/':
            folder = os.path.dirname(folder)
        # Also go up for multiple folders
        elif len(filesAux) > 1:
            folder = os.path.dirname(folder[:-1])
            
    # If no file loaded and is a compressed file, open it
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
                error, output = CompressionManager.list(Globals.file, Globals.PARENT.treeListCtrl1)
                # Show the result
                if error:
                    Utilities.Log(output,Utilities.ERRO)
                else:
                    Utilities.Log(output,Utilities.INFO)
                # If everything is Ok, change the tile
                if not error:   
                    Globals.PARENT.staticText2.SetLabel(Utilities.BasenameMod(Globals.file))
                # Otherwise change to "no file" mode
                else:
                    MainFrameMenu.closeFile(None)
                # PATCH: Fixes the expand problem in the treeListCtrl
                Globals.PARENT.treeListCtrl1.ExpandAll(Globals.PARENT.treeListCtrl1.GetRootItem())
            finally :
                # Sets the normal cursor again
                if Globals.PARENT.busy:
                    del Globals.PARENT.busy
            return wx.DragCopy
            
    # If no file loaded and normal file or more than one file, 
    # show the dialog to create new
        else:
            Globals.file = filenames[0]
            dialog = CompressionDialog.create(Globals.PARENT,
                ((len(filenames)>1) or os.path.isdir(filenames[0])))
            if dialog.ShowModal() != wx.ID_OK:
                Globals.file = Globals.NO_FILE
                return wx.DragNone
            else:
                Globals.PARENT.staticText2.SetLabel(Utilities.BasenameMod(Globals.file))
                flagNewFile = True
                    
    try:
        # It is easy to drag-and-drog by mistake. Ask for confirmation
        if folder:
            answer = Utilities.YesNoDialog(_('Do you want to add the files to the current archive in ' \
                'the path\n%s?') % folder, _('Compress confirmation'))
        else:
            answer = Utilities.YesNoDialog(_('Do you want to add the files to the current archive?'),
                _('Compress confirmation'))
        if (answer != wx.ID_YES):
            return wx.DragCancel
        # Add the files with the compression manager
        error, output = CompressionManager.add(Globals.file, filenames, folder,
            __theTreeList, Globals.compressionOptions)
        # Show the result
        if error:
            Utilities.Log(output,Utilities.ERRO)
        else:
            Utilities.Log(output,Utilities.INFO)
        # Reload the file in the TreeListCtrl
        error, output = CompressionManager.list(Globals.file, __theTreeList)
        # If error, go to "no file" mode and tell the user
        if error:
            MainFrameMenu.closeFile(None)
		# PATCH: Fixes the expand problem in the treeListCtrl
        __theTreeList.ExpandAll(__theTreeList.GetRootItem())
        # Re-select the destination folder, so it can be found easily
        if folder:
            exists, nodeId = Utilities.CheckFileExistsOnTree(folderInfo[0], __theTreeList, folderInfo[1])
            __theTreeList.SelectItem(nodeId)
            __theTreeList.EnsureVisible(nodeId)
        # Updates the file system (to show the new file)
        if flagNewFile:
            __theDirCtrl.ReCreateTree()
    # If it fails, show error and exit
    except OSError, e:
        Utilities.Log(_(u'Error on paste files') + ': ' + unicode(e),
            Utilities.ERRO)
        return wx.DragError

