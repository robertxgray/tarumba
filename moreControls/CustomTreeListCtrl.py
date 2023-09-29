# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         CustomTreeListCtrl.py
# Purpose:      Custom TreeListCtrl with additional functions.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: CustomTreeListCtrl.py $
# Copyright:    (c) 2012 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx.gizmos
       
class CustomTreeListCtrl(wx.gizmos.TreeListCtrl):
    "Custom TreeListCtrl with additional functions"
    
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
            style=wx.TR_DEFAULT_STYLE, validator=wx.DefaultValidator, name=''):
        "Constructor of CustomTreeListCtrl"
        wx.gizmos.TreeListCtrl.__init__(self, parent=parent, id=id, pos=pos, size=size,
            style=wx.TR_HAS_BUTTONS | wx.TR_MULTIPLE | wx.TR_FULL_ROW_HIGHLIGHT, 
            validator=validator, name=name) 
        
    def EventRightClick(self, function):
        "Assigns a function for the right-click events"
        wx.EVT_RIGHT_DOWN(self.GetMainWindow(), function)
        
    def EventDoubleClick(self, function):
        "Assigns a function for the double-click events"
        wx.EVT_TREE_ITEM_ACTIVATED(self, self.GetId(), function)
        
    def ExpandFolder(self, event):
        "Expands a folder due to a double-click event"
        self.Toggle(event.GetItem())
        
    def CanShowRootDetails(self):
        "Returns true if the root is shown in multiple-columns mode"
        return True

    def SetItemText(self, item, text, column):
        "Sets the item text for this item"
        # Overriden to allow no-text input
        # The no-text input is used by the AlternativeTreeList1
        return wx.gizmos.TreeListCtrl.SetItemText(self, item, str(text), column)
