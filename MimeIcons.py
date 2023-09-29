# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         MimeIcons.py
# Purpose:      Manages the icons shown in the TreeListCtrl.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: MimeIcons.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx
import os

import Globals
import Utilities

###############
## VARIABLES ##
###############

# Image size
__imageSize = (16,16)

# Image list loaded in the TreeListCtrl
__imageList = wx.ImageList(__imageSize[0], __imageSize[1])

# Dictionary for file types
__fileTypes = {}

# Generic file
__genericFile = -1

# Mime type manager
__manager = wx.TheMimeTypesManager

###############
## FUNCTIONS ##
###############

def Begin():
    "Reset the image list"
    global __imageSize
    global __imageList
    global __fileTypes
    # Reset the list
    __imageList = wx.ImageList(__imageSize[0], __imageSize[1])
    __fileTypes.clear()
    # The first icon is for the compressed archive
    # Can be configured in Globals.itclFile
    TARUMBA_ICONS = os.getenv('TARUMBA_ICONS')
    if not(TARUMBA_ICONS):
        TARUMBA_ICONS = os.path.join(os.path.dirname(sys.argv[0]), 'icons')
    itclFile = __imageList.Add(wx.Bitmap(
        TARUMBA_ICONS+'/box.png', wx.BITMAP_TYPE_PNG))
    # Folder
    folder = __imageList.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, 
        wx.ART_OTHER, __imageSize))
    # Expanded folder
    # PATCH: GenericDirCtrl is not showing the expanded folders. Apply to the other
    #        controls to provide the same behaviour
    folderExp = folder
    #folderExp = __imageList.Add(wx.ArtProvider_GetBitmap(
    #    wx.ART_FILE_OPEN, wx.ART_OTHER, __imageSize))
    # Generic file
    global __genericFile
    __genericFile = __imageList.Add(wx.ArtProvider_GetBitmap(
        wx.ART_NORMAL_FILE, wx.ART_OTHER, __imageSize))
    # Return the folder icons
    return (folder, folderExp)
        
def End(treeListCtrl):
    "Assign the icons to the TreeListCtrl"
    global __imageList
    treeListCtrl.AssignImageList(__imageList)
    
def Icon(file, useList=True):
    "Return the icon associated with the given file"
    global __genericFile
    global __fileTypes
    global __imageSize
    try:
        extension = Utilities.GetExtension(file).lower()
        # If the file has no extension, use the generic icon
        if extension == '':
            raise Exception()
        # If we know the icon and is already in the list, return it
        if useList and extension in __fileTypes:
            return __fileTypes[extension]
        # Otherwise we need to add it to the list
        else:
            type = __manager.GetFileTypeFromExtension(extension)
            # Use the generic icon if the extension is unknown
            if not type:
                raise Exception()
            # We need to deactive the log to avoid an error popup when
            # there is no icon for the file type
            nolog = wx.LogNull()
            iconName = type.GetIconInfo()[1]
            del nolog
            # Executable files have their own icon
            if iconName == 'exec':
                icon = wx.ArtProvider_GetBitmap(wx.ART_EXECUTABLE_FILE, 
                    wx.ART_OTHER, __imageSize)
            else:   
                # GetIcon returns an icon with size 32x32
                # We rescale it as the DirCtrl does
                # We could also get the 16x16 icon, but this gives different
                # results with some icon themes
                if not os.path.isfile(iconName):
                    raise Exception()
                bitmap = wx.Bitmap(iconName)
                image = bitmap.ConvertToImage()
                if ((image.GetWidth != __imageSize[0]) or (
                    image.GetHeight != __imageSize[1])):
                    image.Rescale(__imageSize[0], __imageSize[1],
                        wx.IMAGE_QUALITY_HIGH)
                icon = wx.BitmapFromImage(image)
            # If we can't get the icon we use the generic icon
            if not icon.IsOk():
                raise Exception()
            # If we are using the main list, return it's index
            if useList:
                aux = __imageList.Add(icon)
                __fileTypes[extension] = aux
                return aux
            # Else return the bitmap itself
            else:
                return icon
    # If file not found, use a generic one
    except Exception, e:
        if useList:
            return __genericFile
        else:
            return wx.ArtProvider_GetBitmap(
                wx.ART_NORMAL_FILE, wx.ART_OTHER, __imageSize)


