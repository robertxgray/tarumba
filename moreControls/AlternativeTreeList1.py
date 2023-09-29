#Boa:Frame:Frame1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         AlternativeTreeList1.py
# Purpose:      TreeList composed of a dir-tree and a file-list.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: AlternativeTreeList1.py $
# Copyright:    (c) 2012 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx
import wx.lib.mixins.listctrl
import wx.lib.embeddedimage

# Constant definition of file nodes
NODE_FILE = 'F'
# Constant definition of directory nodes
NODE_DIR = 'D'

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

[wxID_FRAME1, wxID_FRAME1LISTCTRL1, wxID_FRAME1SPLITTERWINDOW1, wxID_FRAME1TREECTRL1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class AltTreeListFile1():
    "Class of data for files in the AlternativeTreeList1"
    def __init__(self, text, image):
        "Constructor of nodes"
        self.__text = [text]
        self.__image = image
        self.__data = None
        
    def GetImage(self):
        "Returns the file icon"
        return self.__image
    
    def AddText(self, column, text):
        "Sets the text for a column"
        # Auto generate the list items
        while column > len(self.__text)-1:
            self.__text.append('')
        self.__text[column] = text
        
    def GetTexts(self):
        "Returns the list of text for columns"
        return self.__text
    
    def SetData(self, data):
        "Sets the stored data"
        self.__data = data
    
    def GetData(self):
        "Returns the stored data"
        return self.__data

class AltTreeListDir1():
    "Class of data for directories in the AlternativeTreeList1"
    
    def __init__(self, text):
        "Constructor of nodes"
        self.__text = [text]
        self.__data = None
        self.__files = []
        
    def SetData(self, data):
        "Sets the stored data"
        self.__data = data
        
    def GetData(self):
        "Returns the stored data"
        return self.__data
        
    def AddFile(self, file):
        "Add a new file to the node"
        self.__files.append(file)
        # Return the index as identifier
        return len(self.__files)-1
        
    def GetFiles(self):
        "Return the file list"
        # If file not exists return None
        return self.__files
    
    def AddText(self, column, text):
        "Sets the text for a column"
        # Auto generate the list items
        while column > len(self.__text)-1:
            self.__text.append('')
        self.__text[column] = text
        
    def GetTexts(self):
        "Returns the list of text for columns"
        return self.__text

class AlternativeTreeList1(wx.Panel, wx.lib.mixins.listctrl.ColumnSorterMixin):
    "TreeList composed of a dir-tree and a file-list"
              
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

        self.treeCtrl1 = wx.TreeCtrl(id=wxID_FRAME1TREECTRL1, name='treeCtrl1',
              parent=self.splitterWindow1,
              style=wx.TR_MULTIPLE | wx.TR_HAS_BUTTONS | wx.TR_FULL_ROW_HIGHLIGHT)

        self.listCtrl1 = wx.ListCtrl(id=wxID_FRAME1LISTCTRL1, name='listCtrl1',
              parent=self.splitterWindow1, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
              
        self.splitterWindow1.SplitHorizontally(self.treeCtrl1, self.listCtrl1, 150)

        self._init_sizers()
              
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
        style=wx.TR_DEFAULT_STYLE, validator=wx.DefaultValidator, name='treeListCtrl1'):
        "Constructor for AlternativeTreeList1."
        # Parent constructor
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style, name=name)
        # Call to BOA auto-generated functions
        self._init_ctrls(parent)
        
        # Events
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.DirSelected, self.treeCtrl1)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.FileSelected, self.listCtrl1)
        
        # Current selected directory
        self.current_dir = None
        self.current_num_subdirs = 0
        
        # Icons used for sorting
        self.image_sortup = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16,16))
        self.image_sortdown = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16,16))
        
        # The ColumnSorterMixin enables sortable columns
        self.itemDataMap = {}
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, 0)
        
    def GetTreeCtrl(self):
        "Returns a pointer to the tree control"
        return self.treeCtrl1
        
    # Used by the ColumnSorterMixin
    def GetListCtrl(self):
        return self.listCtrl1

    # Used by the ColumnSorterMixin
    def GetSortImages(self):
        return (self.image_sortdown, self.image_sortup)
        
    def AddRoot(self, text, image):
        "Adds the root node to the tree, returning the new item."
        dirData = AltTreeListDir1(text)
        identifier = self.treeCtrl1.AddRoot(text, image)
        self.treeCtrl1.SetPyData(identifier, dirData)
        return (NODE_DIR, identifier)
        
    def GetRootItem(self):
        "Returns the root item for the tree control."
        return (NODE_DIR, self.treeCtrl1.GetRootItem())
        
    def EventRightClick(self, function):
        "Assigns a function for the right-click events"
        wx.EVT_RIGHT_DOWN(self.treeCtrl1, function)
        wx.EVT_RIGHT_DOWN(self.listCtrl1, function)
        
    def EventDoubleClick(self, function):
        "Assigns a function for the double-click events"
        wx.EVT_TREE_ITEM_ACTIVATED(self.treeCtrl1, wxID_FRAME1TREECTRL1, function)
        wx.EVT_LIST_ITEM_ACTIVATED(self.listCtrl1, wxID_FRAME1LISTCTRL1, function)
        
    def ExpandFolder(self, event):
        "Expands a folder due to a double-click event"
        # Event in treeCtrl
        if event.GetEventType() == wx.wxEVT_COMMAND_TREE_ITEM_ACTIVATED:
            self.treeCtrl1.Toggle(event.GetItem())
        # Event in listCtrl
        else:
            # Get the tree item associated with the list item
            subIdx = self.listCtrl1.GetItemData(event.GetIndex())
            subDir, cookie = self.treeCtrl1.GetFirstChild(self.current_dir)
            for index in range(subIdx):
                subDir, cookie = self.treeCtrl1.GetNextChild(self.current_dir, cookie)
            # Select and expand the tree item
            self.treeCtrl1.SelectItem(subDir)
            self.treeCtrl1.Expand(subDir)
        
    def PopupMenu(self):
        "Pops up the given menu at the specified coordinates, relative to this window."
        return (NODE_DIR, self.treeCtrl1.GetRootItem())
        
    def AppendItem(self, parent, text, image, selectedImage=-1):
        "Appends an item. Can be a file or a folder."
        # Directories
        if image == 1:
            dirData = AltTreeListDir1(text)
            identifier =  self.treeCtrl1.AppendItem(
                parent[1], text, image, selectedImage)
            self.treeCtrl1.SetPyData(identifier, dirData)
            return (NODE_DIR, identifier)
        # Files
        else:
            fileData = AltTreeListFile1(text, image)
            dirData = self.treeCtrl1.GetPyData(parent[1])
            fileId = dirData.AddFile(fileData)
            return (NODE_FILE, parent[1], fileId)
        
    def DeleteAllItems(self):
        "Deletes all items in the control."
        self.listCtrl1.DeleteAllItems()
        return self.treeCtrl1.DeleteAllItems()
    
    def GetColumnCount(self):
        "Returns the number of columns."
        return self.listCtrl1.GetColumnCount()
        
    def AddColumn(self, text):
        "For report view mode (only), adds a column."
        colNumber = self.listCtrl1.GetColumnCount()
        listItem = wx.ListItem()
        # Enable icons
        listItem.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE
        listItem.m_image = -1
        listItem.m_text = text
        # Update the number of columns in the list sorter
        self.SetColumnCount(colNumber+1)
        return self.listCtrl1.InsertColumnInfo(colNumber, listItem)

    def RemoveColumn(self, column):
        "Deletes a column."
        return self.listCtrl1.DeleteColumn(column)
        
    def SetColumnWidth(self, column, width):
        "Sets the column width."
        return self.listCtrl1.SetColumnWidth(column, width)
        
    def SetItemText(self, item, text, column):
        "Sets the item text for this item."
        # Code for files
        if item[0] == NODE_FILE:
            dirData = self.treeCtrl1.GetPyData(item[1])
            fileData = dirData.GetFiles()[item[2]]
            fileData.AddText(column, text)
        # Code for directories
        else:
            dirData = self.treeCtrl1.GetPyData(item[1])
            dirData.AddText(column, text)
        
    def SetPyData(self, item, obj):
        "Associates application-defined data with this item."
        # Directories
        if item[0] == NODE_DIR:
            dirData = self.treeCtrl1.GetPyData(item[1])
            dirData.SetData(obj)
        # Files
        else:
            dirData = self.treeCtrl1.GetPyData(item[1])
            fileData = dirData.GetFiles()[item[2]]
            fileData.SetData(obj)
            
    def GetPyData(self, item):
        "Returns the application-defined data associated with the given item."
        # Directories
        if item[0] == NODE_DIR:
            dirData = self.treeCtrl1.GetPyData(item[1])
            return dirData.GetData()
        # Files
        else:
            dirData = self.treeCtrl1.GetPyData(item[1])
            fileData = dirData.GetFiles()[item[2]]
            return fileData.GetData()
        
    def AssignImageList(self, imageList):
        "Sets the image list associated with the control and takes ownership of it."
        # Add the small arrows used for column sorting
        self.image_sortup = imageList.Add(SmallUpArrow.GetBitmap())
        self.image_sortdown = imageList.Add(SmallDnArrow.GetBitmap())
        # With Assign, the image list is deleted by the widget
        self.treeCtrl1.SetImageList(imageList)
        self.listCtrl1.AssignImageList(imageList, wx.IMAGE_LIST_SMALL)
        
    def ExpandAll(self, item=None):
        "Expands all items in the tree."
        retValue = self.treeCtrl1.ExpandAll()
        # PATCH: Select the root item to load the list
        self.SelectItem(self.GetRootItem())
        return retValue
    
    def DirSelected(self, event):
        "Updates the list of files when a folder is selected."
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected item
        selected = event.GetItem()
        self.current_dir = selected
        if selected:
            # Start clearing the list
            self.listCtrl1.DeleteAllItems()
            listIndex = 0
            self.itemDataMap.clear()
            # Remove the sort icons
            for col in range(self.listCtrl1.GetColumnCount()):
                colItem = self.listCtrl1.GetColumn(col)
                colItem.SetImage(-1)
                self.listCtrl1.SetColumn(col, colItem)
            # Read and process the sub-directories
            subDir, cookie = self.treeCtrl1.GetFirstChild(selected)
            while subDir:
                # The first colum includes the icon
                texts = self.treeCtrl1.GetPyData(subDir).GetTexts()
                index = self.listCtrl1.InsertImageStringItem(listIndex, str(texts[0]), 1)
                self.listCtrl1.SetItemData(index, listIndex)
                # Add the other colums
                i = 1
                while i < len(texts):
                    self.listCtrl1.SetStringItem(listIndex, i, str(texts[i]))
                    i += 1
                # Add the information to the dataMap
                self.itemDataMap[listIndex] = tuple(texts)
                # Get the next sub-directory
                subDir, cookie = self.treeCtrl1.GetNextChild(selected, cookie)
                # Increment the list index
                listIndex += 1
            # Save the number of subdirs in the current directory
            self.current_num_subdirs = listIndex
            # Process the list of files in the node
            dirData = self.treeCtrl1.GetPyData(selected)
            for file in dirData.GetFiles():
                texts = file.GetTexts()
                image = file.GetImage()
                # The first colum includes the icon
                index = self.listCtrl1.InsertImageStringItem(listIndex, str(texts[0]), image)
                self.listCtrl1.SetItemData(index, listIndex)
                # Add the other colums
                i = 1
                while i < len(texts):
                    self.listCtrl1.SetStringItem(listIndex, i, str(texts[i]))
                    i += 1
                # Add the information to the dataMap
                self.itemDataMap[listIndex] = tuple(texts)
                # Increment the list index
                listIndex += 1
                    
    def FileSelected(self, event):
        "Deselect all the directories when a file is selected."
        # If null event we have called it
        if event:
            event.StopPropagation()
        self.treeCtrl1.UnselectAll()
        
    def SelectItem(self, item):
        "Selects the given item."
        self.UnselectAll()
        self.treeCtrl1.SelectItem(item[1])
        if item[0] == NODE_FILE:
            self.listCtrl1.Select(item[2]-self.current_num_subdirs)
            
    def IsSelected(self, item):
        "Returns true if the item is selected."
        # Directories
        if item[0] == NODE_DIR:
            return self.treeCtrl1.IsSelected(item[1])
        # Files
        else:
            return (self.treeCtrl1.IsSelected(item[1])) and (
                self.listCtrl1.IsSelected(item[2]-self.current_num_subdirs))
            
    def EnsureVisible(self, item):
        "Ensures this item is visible."
        self.treeCtrl1.EnsureVisible(item[1])
        if item[0] == NODE_FILE:
            self.listCtrl1.EnsureVisible(item[2]-self.current_num_subdirs)
        
    def UnselectAll(self):
        "Removes the selection from the currently selected items."
        # Tree
        self.treeCtrl1.UnselectAll()
        # List
        selected = self.listCtrl1.GetFirstSelected()
        while selected >= 0:
            self.listCtrl1.Select(selected, False)
            selected = self.listCtrl1.GetNextSelected(selected)
                    
    def GetSelections(self):
        "Returns the selected items."
        selections = []
        # Tree - Directories
        if self.listCtrl1.GetSelectedItemCount() == 0:
            for selected in self.treeCtrl1.GetSelections():
                selections.append((NODE_DIR, selected))
        # List
        else:
            idxSelected = self.listCtrl1.GetFirstSelected()
            selected = self.listCtrl1.GetItemData(idxSelected)
            while idxSelected >= 0:
                # Files
                if selected >= self.current_num_subdirs:
                    selections.append((NODE_FILE, self.current_dir, selected-self.current_num_subdirs))
                # Directories
                else:
                    subDir, cookie = self.treeCtrl1.GetFirstChild(self.current_dir)
                    for index in range(selected):
                        subDir, cookie = self.treeCtrl1.GetNextChild(self.current_dir, cookie)
                    selections.append((NODE_DIR, subDir))
                # Get the next selected
                idxSelected = self.listCtrl1.GetNextSelected(idxSelected)
                selected = self.listCtrl1.GetItemData(idxSelected)
        return selections
    
    def GetFirstChild(self, item):
        "Returns the first child; call GetNextChild for the next child."
        if item[0] == NODE_DIR:
            # Get the number of sub-folders
            numSubDirs = self.treeCtrl1.GetChildrenCount(item[1], False)
            # If there are sub-folders, return the first one
            if numSubDirs > 0:
                itemAux, cookieAux = self.treeCtrl1.GetFirstChild(item[1])
                # Include the index-in-list in the cookie
                return ((NODE_DIR, itemAux), (1, cookieAux))
            # Else return the first file
            else:
                dirData = self.treeCtrl1.GetPyData(item[1])
                files = dirData.GetFiles()
                if len(files) > 0:
                    # Include the index-in-list in the cookie
                    return((NODE_FILE, item[1], 0), (1, 0))
        
    def GetNextChild(self, item, cookie):
        "Returns the next child; call GetFirstChild for the first child."
        if item[0] == NODE_DIR:
            # Get the number of sub-folders
            numSubDirs = self.treeCtrl1.GetChildrenCount(item[1], False)
            # If the requested item is another sub-folder, return the next one
            if cookie[0] < numSubDirs:
                itemAux, cookieAux = self.treeCtrl1.GetNextChild(item[1], cookie[1])
                return ((NODE_DIR, itemAux), (cookie[0]+1, cookieAux))
            else:
                # If no more sub-folders left, return the first file
                if cookie[0] == numSubDirs:
                    return ((NODE_FILE, item[1], 0), (cookie[0]+1, 0))
                # Else return the next file
                else:
                    nextFileIdx = cookie[1]+1
                    return ((NODE_FILE, item[1], nextFileIdx), (cookie[0]+1, nextFileIdx))
        
    def GetChildrenCount(self, item, recursively = True):
        "Returns the number of items in the branch."
        # Directories
        if item[0] == NODE_DIR:
            dirData = self.treeCtrl1.GetPyData(item[1])
            recursiveCount = 0
            # Recursive
            if recursively:
                subDir, cookie = self.treeCtrl1.GetFirstChild(item[1])
                while subDir:
                    recursiveCount += self.GetChildrenCount((NODE_DIR, subDir), True)
                    subDir, cookie = self.treeCtrl1.GetNextChild(selected, cookie)
            # Return the number of files in the node + sub-dirs + recursion
            return len(dirData.GetFiles()) + self.treeCtrl1.GetChildrenCount(item[1], False) + recursiveCount
        # Files
        else:
            return 0
        
    def CanShowRootDetails(self):
        "Returns true if the root is shown in multiple-columns mode"
        return False

