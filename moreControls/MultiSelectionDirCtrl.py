# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         MultiSelectionDirCtrl.py
# Purpose:      DirCtrl that allows multiple selection.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: MultiSelectionDirCtrl.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

class MultiSelectionDirCtrl(wx.GenericDirCtrl):
    "DirCtrl with multiple selection."
    
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
        style=wx.TR_HAS_BUTTONS, name='multiSelectionDirCtrl', defaultFilter=0, 
        filter='', dir=''):
        "Constructor for MultiSelectionDirCtrl."
        wx.GenericDirCtrl.__init__(self, parent=parent, id=id, pos=pos, 
            size=size, style=style, name=name, defaultFilter=defaultFilter, 
            filter=filter, dir=dir)
        # We set the wxTR_MULTIPLE mode for the tree
        self.GetTreeCtrl().SetWindowStyle(
            wx.TR_MULTIPLE | wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | 
            wx.TR_FULL_ROW_HIGHLIGHT )
        
    def GetPaths(self):
        "Return the selected paths."
        # Get the selected items in the tree
        ids = self.GetTreeCtrl().GetSelections()
        paths = []
        # Reset the selected items
        self.GetTreeCtrl().UnselectAll()
        # Get the path for every selected item
        for id in ids:
            self.GetTreeCtrl().SelectItem(id, True)
            paths.append(self.GetPath())
            self.GetTreeCtrl().SelectItem(id, False)
        # Select all the items again
        for id in ids:
            self.GetTreeCtrl().SelectItem(id, True)
        return paths
    
    def SetPath(self, path):
        "Set the path to the given file"
        # Patched to unselect previous paths
        self.GetTreeCtrl().UnselectAll()
        return wx.GenericDirCtrl.SetPath(self, path)
    
    def SetPaths(self, paths):
        "Like SetPaths but for multiple files"
        # Patched to unselect previous paths
        self.GetTreeCtrl().UnselectAll()
        for path in paths:
            wx.GenericDirCtrl.SetPath(self, path)
            
    def EventRightClick(self, function):
        "Assigns a function for the right-click events"
        wx.EVT_RIGHT_DOWN(self.GetTreeCtrl(), function)
        
    def EventDoubleClick(self, function):
        "Assigns a function for the double-click events"
        wx.EVT_TREE_ITEM_ACTIVATED(self, self.GetTreeCtrl().GetId(), function)
        
    def ExpandFolder(self, event):
        "Expands a folder due to a double-click event"
        self.GetTreeCtrl().Toggle(event.GetItem())
       
