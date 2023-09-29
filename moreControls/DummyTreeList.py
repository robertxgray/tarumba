# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         DummyTreeList.py
# Purpose:      TreeList data storage to use when wx.App is not available.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: MultiSelectionDirCtrl.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx.gizmos

class DummyNode():
    "Class of nodes for the DummyTreeList"
    
    def __init__(self):
        "Constructor of dummy nodes"
        self.__child = []
        self.__data = None
        
    def SetPyData(self, data):
        "Add data to the node"
        self.__data = data
        
    def GetPyData(self):
        "Add data to the node"
        return self.__data
        
    def AddChild(self, childId):
        "Add a new child to the list"
        self.__child.append(childId)
        
    def GetChild(self, num):
        "Return the requested children"
        # If child not exists return None
        if (len(self.__child)-1 < num) or (num < 0):
            return (None, -1)
        # Else return the requested child
        else:
            # If it's the last child, return -1 as cookie
            if len(self.__child) == num+1:
                return (self.__child[num], -1)
            # When more children exists, return also it's number
            else:
                return (self.__child[num], num+1)
        
    def GetChildCount(self):
        "Return the number of children"
        return len(self.__child)
        
        
class DummyTreeList(wx.gizmos.TreeListCtrl):
    "TreeList to use when wx.App is not available"
    
    def __init__(self):
        "Constructor of dummy trees"
        self.__nodes = []
        self.__selection = []
        self.AddRoot('',None)
        
    def AddRoot(self, text, image, selectedImage=None, data=None):
        "Add a root node to the TreeList"
        if len(self.__nodes) < 1:
            self.__nodes.append(DummyNode())
        return 0
    
    def GetRootItem(self):
        "Return the root of the TreeList"
        return 0
    
    def AppendItem(self, parent, text, image=-1, selectedImage=-1, data=None):
        "Append a node to the TreeList"
        self.__nodes.append(DummyNode())
        nodeId = len(self.__nodes)-1
        # Asociate the node with it's parent
        self.__nodes[parent].AddChild(nodeId)
        return nodeId
    
    def DeleteAllItems(self):
        "Delete all the nodes of the TreeList"
        self.__nodes = []
    
    def SetPyData(self, item, obj):
        "Set the data of a TreeList node"
        self.__nodes[item].SetPyData(obj)
        
    def GetPyData(self, item):
        "Get the data of a TreeList node"
        return self.__nodes[item].GetPyData()
    
    def GetColumnCount(self):
        "Return the number of columns in the Tree"
        # A value of zero is adequate for it's current uses
        return 0
    
    def GetChildrenCount(self, item, recursively):
        "Return the number of children of a node"
        if item < len(self.__nodes):
            return self.__nodes[item].GetChildCount()
        else:
            return 0
    
    def GetFirstChild(self, item):
        "Return the first child of a node"
        return self.__nodes[item].GetChild(0)
    
    def GetNextChild(self, item, cookie):
        "Return the requested child of a node"
        return self.__nodes[item].GetChild(cookie)
    
    def GetSelections(self):
        "Return the selected nodes in the tree"
        return self.__selection
    
    def SetSelections(self, selections):
        "Set the selected nodes in the tree"
        self.__selection = selections
        
    def SelectAll(self):
        "Select all the nodes of the tree"
        self.__selection = range(len(self.__nodes))[1:]
        
    def CanShowRootDetails(self):
        "Returns true if the root is shown in multiple-columns mode"
        return False
    
    #####################
    ## DUMMY FUNCTIONS ##
    #####################
    
    # The following functions are dummy because we won't show
    # the TreeList in a direct way
    
    def AssignImageList(self, imageList):
        "Dummy function"
        pass

    def RemoveColumn(self, column):
        "Dummy function"
        pass
    
    def AddColumn(self, text):
        "Dummy function"
        pass
    
    def SetColumnWidth(self, column, width):
        "Dummy function"
        pass
    
    def SetItemText(self, item, text, column):
        "Dummy function"
        pass

