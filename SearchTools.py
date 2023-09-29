# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         SearchTools.py
# Purpose:      Provides search capabilities to the main frame.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: SearchTools.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities

import wx
import os

######################
## GLOBAL VARIABLES ##
######################

# Event bound
eventBound = False

# Local search
findLocalDialog = None
findLocalData = None
findLocalTop = None
findLocalRestart = False
findLocalOcurr = None
findLocalText = None
findLocalFlags = None

# Archive search
findArchiveDialog = None
findArchiveData = None
findArchiveOcurr = None
findArchiveRestart = False
findArchiveText = None
findArchiveFlags = None
    
#######################
## PRIVATE FUNCTIONS ##
#######################

def __searchCompareAux(text1, text2, flags):
    "Compares two texts with the use of wx.FR_WHOLEWORD and wx.FR_MATCHCASE"
    # Process the FR_MATCHCASE flag
    if not (flags & wx.FR_MATCHCASE):
        text1 = text1.upper()
        text2 = text2.upper()
    # Process the FR_WHOLEWORD flag
    if flags & wx.FR_WHOLEWORD:
        return (text1 == text2)
    else:
        return (text1.find(text2) >= 0)
    
def __onFindLocal(event):
    "Performs the search over the file system"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Define global variables
    global findLocalTop
    global findLocalOcurr
    global findLocalRestart
    global findLocalData
    global findLocalDialog
    global findLocalText
    global findLocalFlags
    # Get the find params
    text = event.GetFindString()
    text = Utilities.Encode(text)
    flags = event.GetFlags()
    # If not the first search and the search changed, restart
    if findLocalOcurr:
        # Ignore the changes in the wx.FR_DOWN flag
        if ((findLocalText != text) or ((findLocalFlags|wx.FR_DOWN) != (flags|wx.FR_DOWN))):
            findLocalRestart = True
    findLocalText = text
    findLocalFlags = flags
    # Rebuild the find dialog on reset, with search down selected
    if findLocalRestart:
        position = findLocalDialog.GetPosition()
        title = findLocalDialog.GetTitle()
        findLocalDialog.Destroy()
        # Re-create the find data
        findLocalData = wx.FindReplaceData()
        findLocalData.SetFlags(wx.FR_DOWN | event.GetFlags())
        findLocalData.SetFindString(text)
        # Re-create the find dialog
        findLocalDialog = wx.FindReplaceDialog(Globals.PARENT,
            findLocalData, title)
        findLocalDialog.SetPosition(position)
        findLocalDialog.Show()
        # Reset the ocurrence and end restart
        findLocalOcurr = None
        findLocalRestart = False
    # If it's the first search, init the ocurrence variable
    if findLocalOcurr is None:
        findLocalOcurr = 0
    # Else calculate the next ocurrence
    else:
        if flags & wx.FR_DOWN:
            findLocalOcurr += 1
        else:
            findLocalOcurr -= 1
    # If we are before the first instance, end the process
    if findLocalOcurr < 0:
        Utilities.Log(_(u'Search finished with no more results. ' \
        u'Click on find to restart the search.'),Utilities.WARN)
        findLocalRestart = True
        return    
    # Find files with the requested name
    lvarOcurr = 0
    for root, dirs, files in os.walk(findLocalTop, topdown=True):
        # Sorting the names gives nicer results
        files.sort()
        for name in files:
            # Use custom compare to allow wx.FR_WHOLEWORD and wx.FR_MATCHCASE
            if __searchCompareAux(name, text, flags):
                if findLocalOcurr == lvarOcurr:
                    fullPath = os.path.join(root, name)
                    Globals.PARENT.multiSelectionDirCtrl1.SetPath(fullPath)
                    Utilities.Log(_(u'Found %s') % fullPath,Utilities.INFO)
                    return
                lvarOcurr += 1
        # Sorting the names gives nicer results
        dirs.sort()
        for name in dirs:
            # Use custom compare to allow wx.FR_WHOLEWORD and wx.FR_MATCHCASE
            if __searchCompareAux(name, text, flags):
                if findLocalOcurr == lvarOcurr:
                    fullPath = os.path.join(root, name)
                    Globals.PARENT.multiSelectionDirCtrl1.SetPath(fullPath)
                    Utilities.Log(_(u'Found %s') % fullPath,Utilities.INFO)
                    return
                lvarOcurr += 1
    # When no more results, reset the ocurrence variable
    Utilities.Log(_(u'Search finished with no more results. ' \
        u'Click on find to restart the search.'),Utilities.WARN)
    findLocalRestart = True
    
def __onFindArchive(event):
    "Performs the search over the compressed archive"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Define global variables
    global findArchiveOcurr
    global findArchiveRestart
    global findArchiveData
    global findArchiveDialog
    global findArchiveText
    global findArchiveFlags
    # Get the find params
    text = event.GetFindString()
    text = Utilities.Encode(text)
    flags = event.GetFlags()
    # If not the first search and the search changed, restart
    if findArchiveOcurr:
        if ((findArchiveText != text) or (
            # Ignore the changes in the wx.FR_DOWN flag
            (findArchiveFlags|wx.FR_DOWN) != (flags|wx.FR_DOWN))):
            findArchiveRestart = True
    findArchiveText = text
    findArchiveFlags = flags
    # Rebuild the find dialog on reset, with search down selected
    if findArchiveRestart:
        position = findArchiveDialog.GetPosition()
        title = findArchiveDialog.GetTitle()
        findArchiveDialog.Destroy()
        # Re-create the find data
        findArchiveData = wx.FindReplaceData()
        findArchiveData.SetFlags(wx.FR_DOWN | event.GetFlags())
        findArchiveData.SetFindString(text)
        # Re-create the find dialog
        findArchiveDialog = wx.FindReplaceDialog(Globals.PARENT,
            findArchiveData, title)
        findArchiveDialog.SetPosition(position)
        findArchiveDialog.Show()
        # Reset the ocurrence and end restart
        findArchiveOcurr = None
        findArchiveRestart = False
    # If it's the first search, init the ocurrence variable
    if findArchiveOcurr is None:
        findArchiveOcurr = 0
    # Else calculate the next ocurrence
    else:
        if flags & wx.FR_DOWN:
            findArchiveOcurr += 1
        else:
            findArchiveOcurr -= 1
    # If we are before the first instance, end the process
    if findArchiveOcurr < 0:
        Utilities.Log(_(u'Search finished with no more results. ' \
        u'Click on find to restart the search.'),Utilities.WARN)
        findArchiveRestart = True
        return    
    # Get all the items in the tree
    items = Utilities.RecursiveSelection(Globals.PARENT.treeListCtrl1, 
        Globals.PARENT.treeListCtrl1.GetRootItem())
    # Search the requested pattern through the contents of the file
    lvarOcurr = 0
    for item in items:
        # Get the file name for the item
        itemPath = item[0]
        itemName = Utilities.BasenameMod(itemPath)
        itemOcurr = item[1]
        # Use custom compare to allow wx.FR_WHOLEWORD and wx.FR_MATCHCASE
        if __searchCompareAux(itemName, text, flags):
            if findArchiveOcurr == lvarOcurr:
                # Get the treeItemId
                exists, nodeId = Utilities.CheckFileExistsOnTree(itemPath, 
                    Globals.PARENT.treeListCtrl1, itemOcurr)
                Globals.PARENT.treeListCtrl1.SelectItem(nodeId)
                Globals.PARENT.treeListCtrl1.EnsureVisible(nodeId)
                Utilities.Log(_(u'Found %s') % itemPath,Utilities.INFO)
                return
            lvarOcurr += 1
    # When no more results, reset the ocurrence variable
    Utilities.Log(_(u'Search finished with no more results. ' \
        u'Click on find to restart the search.'),Utilities.WARN)
    findArchiveRestart = True
    
######################
## PUBLIC FUNCTIONS ##
######################
    
def search(event):
    "Main search function"
    global findLocalDialog
    global findArchiveDialog
    
    dialog = event.GetDialog()
    if findLocalDialog and findLocalDialog.GetId() == dialog.GetId():
        return __onFindLocal(event)
    if findArchiveDialog and findArchiveDialog.GetId() == dialog.GetId():
        return __onFindArchive(event)

def endLocalSearch():
    "Closes the local search dialog"
    global findLocalDialog
    if findLocalDialog:
        findLocalDialog.Destroy()
        
def endArchiveSearch():
    "Closes the archive search dialog"
    global findArchiveDialog
    if findArchiveDialog:
        findArchiveDialog.Destroy()
    
def searchLocal(event):
    "Shows a dialog to search files on the file system"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Bind the find event if not done yet
    global eventBound
    if not eventBound:
        Globals.PARENT.Bind(wx.EVT_FIND, search)
        Globals.PARENT.Bind(wx.EVT_FIND_NEXT, search)
        eventBound = True
    # Get the name of the selected folder
    folder = Globals.PARENT.multiSelectionDirCtrl1.GetPaths()
    # Check that only one folder has been selected
    if len(folder)!=1:
        Utilities.Log(_(u'You need to select the folder where to ' \
        u'perform the search.'),Utilities.ERRO)
        return
    # If a file is selected, get it's folder
    if not os.path.isdir(folder[0]):
        folder[0] = os.path.dirname(folder[0])
    # Show the folder where we are searching
    Utilities.Log(_(u'Searching files in %s') % folder[0],Utilities.INFO)
    # Prepare the search variables
    global findLocalDialog
    global findLocalData
    global findLocalTop
    global findLocalOcurr
    global findLocalRestart
    # Reset the ocurrences
    findLocalOcurr = None
    # Set the top folder
    findLocalTop = folder[0]
    # Get previous find data and destroy previous dialog
    if findLocalDialog:
        oldFlags = findLocalDialog.GetData().GetFlags()
        oldText = findLocalDialog.GetData().GetFindString()
        findLocalDialog.Destroy()
    # If not previous, use initial values
    else:
        oldFlags = 0
        oldText = ''
    # Init the find data
    findLocalData = wx.FindReplaceData()
    findLocalData.SetFlags(oldFlags | wx.FR_DOWN)
    findLocalData.SetFindString(oldText)
    # Init the find dialog
    findLocalDialog = wx.FindReplaceDialog(Globals.PARENT, findLocalData,
        _(u'Search in %s') % folder[0])
    # Show the find dialog
    findLocalDialog.Show()
    
def searchArchive(event):
    "Shows a dialog to search files on compressed archive"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Bind the find event if not done yet
    global eventBound
    if not eventBound:
        Globals.PARENT.Bind(wx.EVT_FIND, search)
        Globals.PARENT.Bind(wx.EVT_FIND_NEXT, search)
        eventBound = True
    # Check if we have a file loaded
    if Globals.file == Globals.NO_FILE:
        Utilities.Log(_(u'You must open a compressed file before searching on in.'),
            Utilities.ERRO)
        return
    # Show the archive where we are searching
    baseName = Utilities.BasenameMod(Globals.file)
    Utilities.Log(_(u'Searching files in %s') % baseName,Utilities.INFO)
    # Prepare the search variables
    global findArchiveDialog
    global findArchiveData
    global findArchiveOcurr
    global findArchiveRestart
    # Reset the ocurrences
    findArchiveOcurr = None
    # Get previous find data and destroy previous dialog
    if findArchiveDialog:
        oldFlags = findArchiveDialog.GetData().GetFlags()
        oldText = findArchiveDialog.GetData().GetFindString()
        findArchiveDialog.Destroy()
    # If not previous, use initial values
    else:
        oldFlags = 0
        oldText = ''
    # Init the find data
    findArchiveData = wx.FindReplaceData()
    findArchiveData.SetFlags(oldFlags | wx.FR_DOWN)
    findArchiveData.SetFindString(oldText)
    # Init the find dialog
    findArchiveDialog = wx.FindReplaceDialog(Globals.PARENT, findArchiveData,
        _(u'Search in %s') % baseName)
    # Show the find dialog
    findArchiveDialog.Show()

