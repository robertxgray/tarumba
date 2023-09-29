# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         MainFrameMenu.py
# Purpose:      Functions used in the main frame's menu
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: MainFrameMenu.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import MainFrame
import TestDialog
import FixDialog
import EncryptDialog
import DecryptDialog
import SplitDialog
import JoinDialog
import JoinZipDialog
import CompressionManager
import ConfigurationManager
import SearchTools
import MimeIcons
import PathDialog

import wx
import os

def openFile(event, file=None):
    "Opens a file by selecting the compressor"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # If no file given, use a file dialog
    if not file:
        dialog = wx.FileDialog(Globals.PARENT, _(u'Select the file to open'), 
            style=wx.OPEN, defaultDir = Globals.lastUsedPath)
        if dialog.ShowModal() != wx.ID_OK:
            dialog.Destroy()
            return
        file = dialog.GetPath()
        dialog.Destroy()
        # Remember the last path
        Globals.lastUsedPath = os.path.dirname(file)
    # Check that the file exists
    if not os.path.isfile(file):
        Utilities.Log(_(u'Can\'t load the file %s: The file does not exist.' \
            '') % Utilities.BasenameMod(file), Utilities.ERRO)
        Utilities.Beep()
        return
    # Select the file in the file system    
    Globals.PARENT.multiSelectionDirCtrl1.SetPath(file)
    # Open the file via the main function
    Globals.PARENT.OpenFile(None)
      
# List of functions to open last opened files
lastOpenedFuncsList = []

def lastOpenedFunc0(event):
    "Opens the first last opened file"
    return openFile(event, Globals.lastOpenedList[0])
lastOpenedFuncsList.append(lastOpenedFunc0)

def lastOpenedFunc1(event):
    "Opens the second last opened file"
    return openFile(event, Globals.lastOpenedList[1])
lastOpenedFuncsList.append(lastOpenedFunc1)

def lastOpenedFunc2(event):
    "Opens the third last opened file"
    return openFile(event, Globals.lastOpenedList[2])
lastOpenedFuncsList.append(lastOpenedFunc2)

def lastOpenedFunc3(event):
    "Opens the fourth last opened file"
    return openFile(event, Globals.lastOpenedList[3])
lastOpenedFuncsList.append(lastOpenedFunc3)

def lastOpenedFunc4(event):
    "Opens the fifth last opened file"
    return openFile(event, Globals.lastOpenedList[4])
lastOpenedFuncsList.append(lastOpenedFunc4)

def lastOpenedFunc5(event):
    "Opens the sixth last opened file"
    return openFile(event, Globals.lastOpenedList[5])
lastOpenedFuncsList.append(lastOpenedFunc5)

def lastOpenedFunc6(event):
    "Opens the seventh last opened file"
    return openFile(event, Globals.lastOpenedList[6])
lastOpenedFuncsList.append(lastOpenedFunc6)

def lastOpenedFunc7(event):
    "Opens the eighth last opened file"
    return openFile(event, Globals.lastOpenedList[7])
lastOpenedFuncsList.append(lastOpenedFunc7)

def lastOpenedFunc8(event):
    "Opens the ninth last opened file"
    return openFile(event, Globals.lastOpenedList[8])
lastOpenedFuncsList.append(lastOpenedFunc8)

def lastOpenedFunc9(event):
    "Opens the tenth last opened file"
    return openFile(event, Globals.lastOpenedList[9])
lastOpenedFuncsList.append(lastOpenedFunc9)

def clearHistory(event):
    "Clears the list of last opened files"
    Globals.lastOpened = None
    updateLastOpened(None)
    
def updateLastOpened(file):
    "Updates the last opened files"
    # Do nothing if the history is disabled
    if not Globals.REMEMBER_RECENTLY:
        return
    # If a file given, add it to the list
    if file:
        if Globals.lastOpened:
            opened = file + ':' + Globals.lastOpened
        else:
            opened = file
    # Else just load the current one
    else:
        # If no last opened files found
        if not Globals.lastOpened:
            opened = ""
        else:
            opened = Globals.lastOpened
    # Manage empty lists
    openedList = opened.split(':')
    if not openedList[0]:
        openedList = []
    # Avoid duplicates
    if file:
        i = len(openedList)-1
        while i > 0:
            if file == openedList[i]:
                del openedList[i]
            i-=1
    # Delete the older if more than ten
    if len(openedList) > 10:
        openedList = openedList[:10]
    # Update the global variables
    opened = ':'.join(openedList)
    Globals.lastOpened = opened
    Globals.lastOpenedList = openedList
    # Update the config file
    ConfigurationManager.saveValue('LAST_OPENED',opened)
    # Update the last opened menu
    lastOpMenu = Globals.PARENT.menuRecent
    oldItems = lastOpMenu.GetMenuItems()
    for item in oldItems:
        lastOpMenu.DeleteItem(item)
    i = 0
    # Reload the list again
    for item in openedList:
        # Get the id for the item and add it to the menu
        itemId = Globals.PARENT.lastOpenedIds[i]
        menuItem = wx.MenuItem(
            help=_(u'Open %s' % item), id=itemId, text=item, kind=wx.ITEM_NORMAL)
        # Get the bitmap for it's type
        menuItem.SetBitmap(MimeIcons.Icon(item, useList=False))
        lastOpMenu.AppendItem(menuItem)
        # Bind every file with it's open function
        wx.EVT_MENU(Globals.PARENT, itemId, 
              lastOpenedFuncsList[i])
        i+=1
    # Add an entry to delete the history
    lastOpMenu.AppendSeparator()
    itemId = Globals.PARENT.lastOpenedIds[10]
    menuItem = wx.MenuItem(
        help=_(u'Clear the history of recently opened files'),
        id=itemId, text=_(u'Clear History'), kind=wx.ITEM_NORMAL)
    menuItem.SetBitmap(wx.ArtProvider.GetBitmap('gtk-clear',wx.ART_MENU ))    
    lastOpMenu.AppendItem(menuItem)    
    wx.EVT_MENU(Globals.PARENT, itemId, clearHistory)
    
def closeFile(event):
    "Closes the current file and goes to NO_FILE mode"
    # If null even we have called it
    if event:
        event.StopPropagation()
    # Close the archive search
    SearchTools.endArchiveSearch()
    # Change the opened archive label
    oldFile = Globals.file
    Globals.file = Globals.NO_FILE
    Globals.PARENT.staticText2.SetLabel(Globals.NO_FILE)
    Globals.PARENT.MenusSetNofile()
    # Clean the wxTreeListCtrl
    Globals.PARENT.treeListCtrl1.DeleteAllItems()
    for i in range(Globals.PARENT.treeListCtrl1.GetColumnCount(),0,-1):
        Globals.PARENT.treeListCtrl1.RemoveColumn(i-1)
    # PATCH: Fixes the expand problem in the treeListCtrl
    Globals.PARENT.treeListCtrl1.ExpandAll(
        Globals.PARENT.treeListCtrl1.GetRootItem())
    # Show a message to the user
    if oldFile != Globals.NO_FILE:
        Utilities.Log(_(u'File %s closed.') % Utilities.BasenameMod(oldFile), 
            Utilities.INFO)
            
def addFile(event):
    "Add a file to the current compressed file"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Show a file dialog to select the file
    dialog = wx.FileDialog(Globals.PARENT, _(u'Select the file(s) to add'),
        style=wx.OPEN|wx.FD_MULTIPLE, defaultDir = Globals.lastUsedPath)
    if dialog.ShowModal() != wx.ID_OK:
        dialog.Destroy()
        return
    # Remember the last used path
    Globals.lastUsedPath = os.path.dirname(dialog.GetPath())
    files = dialog.GetPaths()
    dialog.Destroy()
    # Check that the files exist
    for file in files:
        if not os.path.isfile(file):
            Utilities.Log(_(u'Can\'t add the file %s: The file does not exist.' \
                '') % Utilities.BasenameMod(file), Utilities.ERRO)
            Utilities.Beep()
            return
    # Select the files in the file system    
    Globals.PARENT.multiSelectionDirCtrl1.SetPaths(files)
    # If no file loaded, create a new file
    if Globals.file == Globals.NO_FILE:
        Globals.PARENT.CreateCompressed(None)
    # Else add the files to the current one
    else:
        # Unselect the archive contents to add always to the root
        Globals.PARENT.treeListCtrl1.UnselectAll()
        Globals.PARENT.AddToFile(None)
        
def addFolder(event):
    "Add a folder to the current compressed file"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Show a dir dialog to select the folder
    dialog = wx.DirDialog(Globals.PARENT, _(u'Select the folder to add'),
        defaultPath = Globals.lastUsedPath)
    if dialog.ShowModal() != wx.ID_OK:
        dialog.Destroy()
        return
    # Remember the last used path
    Globals.lastUsedPath = dialog.GetPath()
    folder = dialog.GetPath()
    dialog.Destroy()
    # Check that the files exist
    if not os.path.isdir(folder):
        Utilities.Log(_(u'Can\'t add the folder %s: The folder does not exist.' \
            '') % Utilities.BasenameMod(folder), Utilities.ERRO)
        Utilities.Beep()
        return
    # Select the folder in the file system    
    Globals.PARENT.multiSelectionDirCtrl1.SetPath(folder)
    # If no file loaded, create a new file
    if Globals.file == Globals.NO_FILE:
        Globals.PARENT.CreateCompressed(None)
    # Else add the files to the current one
    else:
        # Unselect the archive contents to add always to the root
        Globals.PARENT.treeListCtrl1.UnselectAll()
        Globals.PARENT.AddToFile(None)
        
def extractSelected(event):
    "Extract the selected contents into a folder"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Select the folder where to extract the files
    dialog = wx.DirDialog(Globals.PARENT, 
        _(u'Select the folder where to extract'), 
        defaultPath = Globals.lastUsedPath)
    if dialog.ShowModal() != wx.ID_OK:
        dialog.Destroy()
        return
    # Remember the last used path
    Globals.lastUsedPath = dialog.GetPath()
    folder = dialog.GetPath()
    dialog.Destroy()
    # Check that the files exist
    if not os.path.isdir(folder):
        Utilities.Log(_(u'Can\'t extract to the folder %s: The folder does not exist.' \
            '') % Utilities.BasenameMod(folder), Utilities.ERRO)
        Utilities.Beep()
        return
    # Select the folder in the file system    
    Globals.PARENT.multiSelectionDirCtrl1.SetPath(folder)
    # Extract the files
    Globals.PARENT.ExtractFiles(None)
        
def extractAll(event):
    "Extract all the contents into a folder"
    Globals.PARENT.treeListCtrl1.SelectItem(Globals.PARENT.treeListCtrl1.GetRootItem())
    extractSelected(None)
    
def setRecompressionLevel(event):
    "Opens a dialog that allows the user to change the compression level"
    # If null event we have called it
    if event:
        event.StopPropagation()
    # Check if a file has been loaded
    if Globals.file == Globals.NO_FILE:
        Utilities.Log(_(u'You must open a file with Tarumba first.'), 
            Utilities.ERRO)
        return
    # Get the compression levels for the format
    levels = CompressionManager.compressionLevels(None)
    levelsAux = []
    # Get the display name for every level
    defaultLevel = 0
    i=0
    for level in levels:
        levelsAux.append(level[0])
        if level[2]:
            defaultLevel = i
        i+=1
    dialog = wx.SingleChoiceDialog(
        Globals.PARENT, _(u'Select the level that you wan to use.'), 
        _(u'Set recompression level'),
        levelsAux, 
        wx.CHOICEDLG_STYLE)
    dialog.SetSelection(defaultLevel)
    if dialog.ShowModal() == wx.ID_OK:
        # Reasociate the label with the display name
        levelName = dialog.GetStringSelection()
        for level in levels:
            if levelName == level[0]:
                Globals.compressionOptions.level = level[1]
                # Show a log message
                Utilities.Log(_(u'Recompression level changed to %(level)s' \
                    u' for file %(file)s.' % {'level':level[1], 
                    'file':Utilities.BasenameMod(Globals.file)}),
                    Utilities.INFO)
                break
    dialog.Destroy()

def testFile(event):
    "Tests the integrity of a file"
    # If null even we have called it
    if event:
        event.StopPropagation()  
    dialog = TestDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    
def fixFile(event):
    "Repairs a damaged file"
    # If null event we have called it
    if event:
        event.StopPropagation()    
    # Inform about the risks of repairing...
    Utilities.WarningDialog(
        _(u'Fixing damaged files is a very complex process and in many\n' \
          u'cases won\'t be possible to recover all the information.\n' \
          u'Tarumba will try to perform some basic fixing operations\n' \
          u'that can be useful in some cases, if those operations\n' \
          u'fail you will need to look up at the damaged file\'s\n' \
          u'format documentation and try to perform a manual fix.'))
    dialog = FixDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    # Update the file system to show the created files
    Globals.PARENT.multiSelectionDirCtrl1.ReCreateTree()
    
def encrypt(event):
    "Encrypts a file"
    # If null event we have called it
    if event:
        event.StopPropagation()  
    dialog = EncryptDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    # Update the file system to show the created files
    Globals.PARENT.multiSelectionDirCtrl1.ReCreateTree()
    
def decrypt(event):
    "Decrypts a file"
    # If null event we have called it
    if event:
        event.StopPropagation()  
    dialog = DecryptDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    # Update the file system to show the created files
    Globals.PARENT.multiSelectionDirCtrl1.ReCreateTree()
    
def split(event):
    "Splits a file into smaller volumes"
    # If null event we have called it
    if event:
        event.StopPropagation()  
    dialog = SplitDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    # Update the file system to show the created files
    Globals.PARENT.multiSelectionDirCtrl1.ReCreateTree()
    
def join(event):
    "Joins volumes from a previous splitted file"
    # If null event we have called it
    if event:
        event.StopPropagation()  
    dialog = JoinDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    # Update the file system to show the created files
    Globals.PARENT.multiSelectionDirCtrl1.ReCreateTree()
    
def joinZip(event):
    "Joins multivolume zip files created with other programs (winzip)"
    # If null event we have called it
    if event:
        event.StopPropagation()  
    dialog = JoinZipDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    # Update the file system to show the created files
    Globals.PARENT.multiSelectionDirCtrl1.ReCreateTree()
    
def ShowHidden(event):
    "Show or hide the hidden files"
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.SHOW_HIDDEN
    # Update the file system
    Globals.SHOW_HIDDEN = show
    Globals.PARENT.multiSelectionDirCtrl1.ShowHidden(show)
    # Update the check status
    Globals.PARENT.menu6.Check(MainFrame.wxID_WXFRAME1MENU6ITEMS0,show)
    # Save the value
    ConfigurationManager.saveValue('SHOW_HIDDEN',str(show))
    
def AlternativeFileView(event):
    "Change the file-view mode"
    # Some booleans are reversed because the alternative is now the default
    
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = not event.IsChecked()
        
        # The program must be restarted
        Utilities.WarningDialog(_(u'This option requires Tarumba to be restarted.'))
        
    else:
        show = Globals.ALTERNATIVE_TREEVIEW
    # Save the configuration changes
    Globals.ALTERNATIVE_TREEVIEW = show
    # Update the check status
    Globals.PARENT.menu6.Check(MainFrame.wxID_WXFRAME1MENU6ITEMS7,not show)
    # Save the value
    ConfigurationManager.saveValue('ALTERNATIVE_TREEVIEW',str(show))
    
def ShowToolBar(event):
    "Show or hide the tool bar" 
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.SHOW_TOOLBAR
    # Show or hide the tool bar
    Globals.SHOW_TOOLBAR = show
    Globals.PARENT.toolBar1.Show(show)
    # PATCH: It truly updates the parent frame
    size = Globals.PARENT.GetSize()
    size2 = wx.Size(size.x+1,size.y+1)
    Globals.PARENT.SetSize(size2)
    Globals.PARENT.SetSize(size)
    # Update the check status
    Globals.PARENT.menu6.Check(MainFrame.wxID_WXFRAME1MENU6ITEMS1,show)
    # Save the value
    ConfigurationManager.saveValue('SHOW_TOOLBAR',str(show))
    
def ShowStatusBar(event):
    "Show or hide the status bar" 
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.SHOW_STATUSBAR
    # Show or hide the status bar
    Globals.SHOW_STATUSBAR = show
    Globals.PARENT.statusBar1.Show(show)
    # PATCH: It truly updates the parent frame
    size = Globals.PARENT.GetSize()
    size2 = wx.Size(size.x+1,size.y+1)
    Globals.PARENT.SetSize(size2)
    Globals.PARENT.SetSize(size)
    # Update the check status
    Globals.PARENT.menu6.Check(MainFrame.wxID_WXFRAME1MENU6ITEMS2,show)
    # Save the value
    ConfigurationManager.saveValue('SHOW_STATUSBAR',str(show))

def ShowFileSystem(event):
    "Show or hide the file system" 
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.SHOW_FILESYSTEM
    # Show or hide the file system
    if show:
        Globals.PARENT.splitterWindow2.SplitVertically(
            Globals.PARENT.panel1, Globals.PARENT.panel2, 300)
    else:
        Globals.PARENT.splitterWindow2.Unsplit(Globals.PARENT.panel1)
    # Update the check status
    Globals.PARENT.menu6.Check(MainFrame.wxID_WXFRAME1MENU6ITEMS3,show)
    # Save the value
    Globals.SHOW_FILESYSTEM = show
    ConfigurationManager.saveValue('SHOW_FILESYSTEM',str(show))
    
def SetEasyMode(event):
    "Set the GUI in easy mode"
    # If null event we have called it
    if event:
        event.StopPropagation()
    Globals.SHOW_TOOLBAR = True
    ShowToolBar(None)
    Globals.SHOW_STATUSBAR = True
    ShowStatusBar(None)
    Globals.SHOW_FILESYSTEM = False
    ShowFileSystem(None)
    
def SetExpertMode(event):
    "Set the GUI in expert mode"
    # If null event we have called it
    if event:
        event.StopPropagation()
    Globals.SHOW_TOOLBAR = False
    ShowToolBar(None)
    Globals.SHOW_STATUSBAR = False
    ShowStatusBar(None)
    Globals.SHOW_FILESYSTEM = True
    ShowFileSystem(None)
    
def SetFullMode(event):
    "Set the GUI in full mode"
    # If null event we have called it
    if event:
        event.StopPropagation()
    Globals.SHOW_TOOLBAR = True
    ShowToolBar(None)
    Globals.SHOW_STATUSBAR = True
    ShowStatusBar(None)
    Globals.SHOW_FILESYSTEM = True
    ShowFileSystem(None)
    
def BeepOption(event):
    "Enable or disable the beep option"
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.BEEP
    # Update the check status
    Globals.PARENT.menu5.Check(MainFrame.wxID_WXFRAME1MENU5ITEMS0,show)
    # Save the value
    Globals.BEEP = show
    ConfigurationManager.saveValue('BEEP',str(show))
    
def FollowLinksOption(event):
    "Enable or disable the follow links option"
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.FOLLOW_LINKS
    # Update the check status
    Globals.PARENT.menu5.Check(MainFrame.wxID_WXFRAME1MENU5ITEMS1,show)
    # Save the value
    Globals.FOLLOW_LINKS = show
    ConfigurationManager.saveValue('FOLLOW_LINKS',str(show))
    
def ConfirmOverwriteOption(event):
    "Enable or disable the confirm overwrite option"
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.NO_CONFIRM_OVERWRITE
    # This can be dangerous, so ask to the user
    if event and (show):
        answer = Utilities.YesNoDialog(_(u'This can be dangerous. ' \
            u'Are you sure?\n'), _(u'WARNING'))
        if (answer != wx.ID_YES):
            show = False
    # Update the check status
    Globals.PARENT.menu5.Check(MainFrame.wxID_WXFRAME1MENU5ITEMS2,show)
    # Save the value
    Globals.NO_CONFIRM_OVERWRITE = show
    ConfigurationManager.saveValue('NO_CONFIRM_OVERWRITE',str(show))
    
def AskToEncryptOption(event):
    "Enable or disable the ask to encrypt option"
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.NO_ASK_TO_ENCRYPT
    # Update the check status
    Globals.PARENT.menu5.Check(MainFrame.wxID_WXFRAME1MENU5ITEMS3,show)
    # Save the value
    Globals.NO_ASK_TO_ENCRYPT = show
    ConfigurationManager.saveValue('NO_ASK_TO_ENCRYPT',str(show))
    
def RememeberRecentlyOpened(event):
    "Enable or disable the remember recently opened option"
    # If null event we are on startup sequence
    show = None
    if event:
        event.StopPropagation()
        show = event.IsChecked()
    else:
        show = Globals.REMEMBER_RECENTLY
    # Update the check status
    Globals.PARENT.menu5.Check(MainFrame.wxID_WXFRAME1MENU5ITEMS5,show)
    # Save the value
    Globals.REMEMBER_RECENTLY = show
    ConfigurationManager.saveValue('REMEMBER_RECENTLY',str(show))
    # Enable or disable the last opened menu
    updateLastOpened(None)
    Globals.PARENT.menu1.Enable(
        MainFrame.wxID_WXFRAME1MENU1ITEMS2,Globals.REMEMBER_RECENTLY)
    
def PathOptions(event):
    "Shows the path options dialog"
    # If null event we have called it
    if event:
        event.StopPropagation()  
    dialog = PathDialog.create(Globals.PARENT)
    dialog.ShowModal()
    dialog.Destroy()
    
def DisableUnavailableOptions():
    "Disable the options in menu when their dependencies are not available"
    # Encrypt and decrypt via SSL
    openSSLinstalled = Utilities.IsInstalled(Globals.OPENSSL_BIN)
    Globals.PARENT.menu2.Enable(
        MainFrame.wxID_WXFRAME1MENU2ITEMS2, openSSLinstalled)
    Globals.PARENT.menu2.Enable(
        MainFrame.wxID_WXFRAME1MENU2ITEMS3, openSSLinstalled)
    if openSSLinstalled:
        Utilities.Debug(_(u'OpenSSL found in your system, encrypt and ' \
            'decrypt options enabled.'))
    else:
        Utilities.Debug(_(u'WARNING: OpenSSL not found in your system, ' \
            'encrypt and decrypt options disabled.'))
    # Join-zip
    zipInstalled = Utilities.IsInstalled(Globals.ZIP_BIN)
    Globals.PARENT.menu2.Enable(
        MainFrame.wxID_WXFRAME1MENU2ITEMS6, zipInstalled)
    # Omit zip related messages as they are already present in the zip module

