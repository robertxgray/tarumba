#Boa:Frame:Frame1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         AlternativeDirCtrl1.py
# Purpose:      DirCtrl composed of a dir-tree and a file-list.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: AlternativeDirCtrl1.py $
# Copyright:    (c) 2012 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import MimeIcons
import Utilities

import wx
import wx.lib.mixins.listctrl
import wx.lib.embeddedimage
import os
import time
import pwd
import grp

# Small arrows used when a column is sorted
# Yes, this has been "stolen" from the wxPython demo
SmallUpArrow = wx.lib.embeddedimage.PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAADxJ"
    "REFUOI1jZGRiZqAEMFGke2gY8P/f3/9kGwDTjM8QnAaga8JlCG3CAJdt2MQxDCAUaOjyjKMp"
    "cRAYAABS2CPsss3BWQAAAABJRU5ErkJggg==")
SmallDnArrow = wx.lib.embeddedimage.PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEhJ"
    "REFUOI1jZGRiZqAEMFGke9QABgYGBgYWdIH///7+J6SJkYmZEacLkCUJacZqAD5DsInTLhDR"
    "bcPlKrwugGnCFy6Mo3mBAQChDgRlP4RC7wAAAABJRU5ErkJggg==")

[wxID_FRAME1, wxID_FRAME1LISTCTRL1, wxID_FRAME1SPLITTERWINDOW1, wxID_FRAME1DIRCTRL1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class AlternativeDirCtrl1(wx.Panel, wx.lib.mixins.listctrl.ColumnSorterMixin):
    "DirCtrl composed of a dir-tree and a file-list"
              
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.splitterWindow1, 1, border=0, flag=wx.EXPAND)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAME1SPLITTERWINDOW1,
            name='splitterWindow1', parent=self, style=wx.SP_3D)
        self.splitterWindow1.SetMinimumPaneSize(50)

        self.dirCtrl1 = wx.GenericDirCtrl(parent=self.splitterWindow1, id=wxID_FRAME1DIRCTRL1, 
            style=wx.DIRCTRL_DIR_ONLY, dir=self.current_dir)
        
        self.dirCtrl1.GetTreeCtrl().SetWindowStyle(
            wx.TR_MULTIPLE | wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | 
            wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_NO_LINES)

        self.listCtrl1 = wx.ListCtrl(id=wxID_FRAME1LISTCTRL1, name='listCtrl1',
            parent=self.splitterWindow1, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
              
        self.splitterWindow1.SplitHorizontally(self.dirCtrl1, self.listCtrl1, 150)

        self._init_sizers()
              
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
        style=wx.TR_HAS_BUTTONS, name='alternativeDirCtrl1', defaultFilter=0, 
        filter='', dir=''):
        # Current selected directory
        self.current_dir = dir
        # Parent constructor
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style, name=name)
        # Call to BOA auto-generated functions
        self._init_ctrls(parent)
        
        # Show hidden files?
        self.showHidden = self.dirCtrl1.GetShowHidden()
        
        # Events
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.DirSelected, self.dirCtrl1.GetTreeCtrl())
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.FileSelected, self.listCtrl1)

        # Icons used for sorting
        self.image_sortup = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16,16))
        self.image_sortdown = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16,16))
        
        # The ColumnSorterMixin enables sortable columns
        self.itemDataMap = {}
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, 0)
        
        # LIST COLUMNS
        
        # File name
        listItem = wx.ListItem()
        listItem.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE
        listItem.m_image = -1
        listItem.m_text = _(u'Name')
        self.listCtrl1.InsertColumnInfo(0, listItem)
        self.listCtrl1.SetColumnWidth(0, 200)
        
        # File name
        listItem.m_text = _(u'Size')
        self.listCtrl1.InsertColumnInfo(1, listItem)
        self.listCtrl1.SetColumnWidth(1, 100)
        
        # Modification date
        listItem.m_text = _(u'Date')
        self.listCtrl1.InsertColumnInfo(2, listItem)
        self.listCtrl1.SetColumnWidth(2, 100)
        
        # Modification time
        listItem.m_text = _(u'Time')
        self.listCtrl1.InsertColumnInfo(3, listItem)
        self.listCtrl1.SetColumnWidth(3, 100)
        
        # User
        listItem.m_text = _(u'User')
        self.listCtrl1.InsertColumnInfo(4, listItem)
        self.listCtrl1.SetColumnWidth(4, 100)
        
        # Group
        listItem.m_text = _(u'Group')
        self.listCtrl1.InsertColumnInfo(5, listItem)
        self.listCtrl1.SetColumnWidth(5, 100)
        
        # Permissions
        listItem.m_text = _(u'Permissions')
        self.listCtrl1.InsertColumnInfo(6, listItem)
        self.listCtrl1.SetColumnWidth(6, 100)
        
        # Update the number of columns in the list sorter
        self.SetColumnCount(7)
        
    # Used by the ColumnSorterMixin
    def GetListCtrl(self):
        "Returns a pointer to the list control"
        return self.listCtrl1

    # Used by the ColumnSorterMixin
    def GetSortImages(self):
        "Returns the images to be put on the column header when sorting"
        return (self.image_sortdown, self.image_sortup)
    
    def GetTreeCtrl(self):
        "Returns a pointer to the tree control"
        return self.dirCtrl1
    
    def ShowHidden(self, show):
        "If true, hidden folders and files will be displayed by the control"
        self.showHidden = show
        return self.dirCtrl1.ShowHidden(show)
        
    def EventRightClick(self, function):
        "Assigns a function for the right-click events"
        wx.EVT_RIGHT_DOWN(self.dirCtrl1.GetTreeCtrl(), function)
        wx.EVT_RIGHT_DOWN(self.listCtrl1, function)
        
    def EventDoubleClick(self, function):
        "Assigns a function for the double-click events"
        wx.EVT_TREE_ITEM_ACTIVATED(self.dirCtrl1.GetTreeCtrl(), wxID_FRAME1DIRCTRL1, function)
        wx.EVT_LIST_ITEM_ACTIVATED(self.listCtrl1, wxID_FRAME1LISTCTRL1, function)
        
    def ExpandFolder(self, event):
        "Expands a folder due to a double-click event"
        # Event in treeCtrl
        if event.GetEventType() == wx.wxEVT_COMMAND_TREE_ITEM_ACTIVATED:
            self.dirCtrl1.Toggle(event.GetItem())
        # Event in listCtrl
        else:
            # Get the tree item associated with the list item
            subIdx = self.listCtrl1.GetItemData(event.GetIndex())
            subDir = os.path.join(self.current_dir, self.listCtrl1.GetItemText(subIdx))
            # Select and expand the tree item
            self.dirCtrl1.SetPath(subDir)
        
    def PopupMenu(self):
        "Pops up the given menu at the specified coordinates, relative to this window."
        return (NODE_DIR, self.dirCtrl1.GetRootItem())

    def DirSelected(self, event):
        "Updates the list of files when a folder is selected."
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected path
        newPath = self.dirCtrl1.GetPath()
        if newPath:
            self.current_dir = newPath
            # Start clearing the list
            self.listCtrl1.DeleteAllItems()
            listIndex = 0
            self.itemDataMap.clear()
            # Remove the sort icons
            for col in range(self.listCtrl1.GetColumnCount()):
                colItem = self.listCtrl1.GetColumn(col)
                colItem.SetImage(-1)
                self.listCtrl1.SetColumn(col, colItem)
            # Request a new image list
            folder, folderExp = MimeIcons.Begin()
            # Read and process the path contents
            contentsAux = os.listdir(newPath)
            # Put the folders at the beginning
            dirsAux = []
            filesAux = []
            for con in contentsAux:
                # Ignore hidden files when configured
                if not self.showHidden and con.startswith('.'):
                    continue
                # Put files and folders in different lists
                if os.path.isdir(os.path.join(newPath, con)):
                    dirsAux.append(con)
                else:
                    filesAux.append(con)
            # Sort and re-join the list
            #dirsAux.sort()   # Disabled to imitate the TreeList's behaviour
            #filesAux.sort()
            contents = dirsAux + filesAux
            # Add every content to the listCtrl
            for con in contents:
                dataMapTuple = ()
                fullPath = os.path.join(newPath, con)
                # Set the icon for folders
                if os.path.isdir(fullPath):
                    icon = folder
                # Set the icon for files
                else:
                    icon = MimeIcons.Icon(fullPath)
                # Get the attributes via os.stat
                stats = os.stat(fullPath)
                # Add the list item
                index = self.listCtrl1.InsertImageStringItem(listIndex, con, icon)
                self.listCtrl1.SetItemData(index, listIndex)
                # Size
                self.listCtrl1.SetStringItem(listIndex, 1, str(stats.st_size))
                # Modification date
                modAux = time.localtime(stats.st_mtime)
                modDate = time.strftime("%Y-%m-%d", modAux)
                self.listCtrl1.SetStringItem(listIndex, 2, modDate)
                # Modification time
                modTime = time.strftime("%H:%M", modAux)
                self.listCtrl1.SetStringItem(listIndex, 3, modTime)
                # User
                try:
                    user = pwd.getpwuid(stats.st_uid).pw_name
                except Exception, e:
                    user = str(stats.st_uid)
                self.listCtrl1.SetStringItem(listIndex, 4, user)
                # Group
                try:
                    group = grp.getgrgid(stats.st_gid).gr_name
                except Exception, e:
                    group = str(stats.st_gid)
                self.listCtrl1.SetStringItem(listIndex, 5, group)
                # Permissions
                perms = Utilities.FileModeString(stats.st_mode)
                self.listCtrl1.SetStringItem(listIndex, 6, perms)
                # Add the information to the dataMap
                self.itemDataMap[listIndex] = (con, stats.st_size, modDate, modTime, perms, user, group)
                # Increment the list index
                listIndex += 1
        # Apply the icons
        MimeIcons.End(self)
                
    def AssignImageList(self, imageList):
        "Sets the image list associated with the control and takes ownership of it."
        # Add the small arrows used for column sorting
        self.image_sortup = imageList.Add(SmallUpArrow.GetBitmap())
        self.image_sortdown = imageList.Add(SmallDnArrow.GetBitmap())
        # With Assign, the image list is deleted by the widget
        self.listCtrl1.AssignImageList(imageList, wx.IMAGE_LIST_SMALL)
                    
    def FileSelected(self, event):
        "Deselect all the directories when a file is selected."
        # If null event we have called it
        if event:
            event.StopPropagation()
        self.dirCtrl1.GetTreeCtrl().UnselectAll()
    
    def GetPaths(self):
        "Return the selected paths."
        paths = []
        # Get the selected items in the tree
        ids = self.dirCtrl1.GetTreeCtrl().GetSelections()
        if ids:
            # Reset the selected items
            self.dirCtrl1.GetTreeCtrl().UnselectAll()
            # Get the path for every selected item
            for id in ids:
                self.dirCtrl1.GetTreeCtrl().SelectItem(id, True)
                paths.append(self.dirCtrl1.GetPath())
                self.dirCtrl1.GetTreeCtrl().SelectItem(id, False)
            # Select all the items again
            for id in ids:
                self.dirCtrl1.GetTreeCtrl().SelectItem(id, True)
        # Get the selected items in the list
        else:
            idxSelected = self.listCtrl1.GetFirstSelected()
            selected = self.listCtrl1.GetItemText(idxSelected)
            while idxSelected >= 0:
                # Add the full path
                paths.append(os.path.join(self.current_dir, selected))
                # Get the next selected
                idxSelected = self.listCtrl1.GetNextSelected(idxSelected)
                selected = self.listCtrl1.GetItemText(idxSelected)
        return paths
    
    def SetPath(self, path):
        "Set the path to the given file"
        # Patched to unselect previous paths
        self.dirCtrl1.GetTreeCtrl().UnselectAll()
        self.dirCtrl1.SetPath(path)
        # Select also the file in the listCtrl
        basename = Utilities.BasenameMod(path)
        if not os.path.isdir(path):
            for i in range(self.listCtrl1.GetItemCount()):
                if basename == self.listCtrl1.GetItemText(i):
                    self.listCtrl1.Select(i)
                    self.listCtrl1.EnsureVisible(i)
                    break
    
    def SetPaths(self, paths):
        "Like SetPaths but for multiple files"
        # Patched to unselect previous paths
        self.dirCtrl1.GetTreeCtrl().UnselectAll()
        # Selecting a folder deselects the files, but this will be used to select
        # multiple files in the same folder (I hope so...)
        self.dirCtrl1.SetPath(paths[0])
        for path in paths:
            # Select also the file in the listCtrl
            basename = Utilities.BasenameMod(path)
            if not os.path.isdir(path):
                for i in range(self.listCtrl1.GetItemCount()):
                    if basename == self.listCtrl1.GetItemText(i):
                        self.listCtrl1.Select(i)
                        #self.listCtrl1.EnsureVisible(i)
                        break
            
    def ReCreateTree(self):
        "Collapse and expand the tree, thus re-creating it from scratch"
        self.dirCtrl1.ReCreateTree()
    
