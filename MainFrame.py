#Boa:Frame:Frame1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         MainFrame.py
# Purpose:      Tarumba's GUI.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: MainFrame.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
from moreControls.ColorLogCtrl import ColorLogCtrl
import CompressionDialog
import CompressionManager
import ConfigurationManager
import MainFrameMenu
import TipOfTheDay
import DragNDrop
import Clipboard
import Temporary
import SearchTools

# Import the alternative controls when corresponding
if Globals.ALTERNATIVE_TREEVIEW:
    from moreControls.AlternativeTreeList1 import AlternativeTreeList1
    from moreControls.AlternativeDirCtrl1 import AlternativeDirCtrl1
else:
    from moreControls.MultiSelectionDirCtrl import MultiSelectionDirCtrl
    from moreControls.CustomTreeListCtrl import CustomTreeListCtrl

import wx
import sys
import os
from wx.lib.wordwrap import wordwrap
import mimetypes
import shutil
import stat

def create(parent):
    return Frame1(parent)
 
[wxID_FRAME1, wxID_FRAME1MULTISELECTIONDIRCTRL1, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL2, wxID_FRAME1SPLITTERWINDOW1, wxID_FRAME1SPLITTERWINDOW2, 
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2, wxID_FRAME1COLORLOGCTRL1, 
 wxID_FRAME1TREELISTCTRL1, wxID_FRAME1TOOLBAR1, wxID_FRAME1STATUSBAR1
] = [wx.NewId() for _init_ctrls in range(12)]

[wxID_WXFRAME1MENU1ITEMS0, wxID_WXFRAME1MENU1ITEMS1,
 wxID_WXFRAME1MENU1ITEMS2, wxID_WXFRAME1MENU1ITEMS3
] = [wx.NewId() for _init_coll_menu1_Items in range(4)]

[wxID_WXFRAME1MENU2ITEMS0, wxID_WXFRAME1MENU2ITEMS1,
 wxID_WXFRAME1MENU2ITEMS2, wxID_WXFRAME1MENU2ITEMS3,
 wxID_WXFRAME1MENU2ITEMS4, wxID_WXFRAME1MENU2ITEMS5,
 wxID_WXFRAME1MENU2ITEMS6
] = [wx.NewId() for _init_coll_menu2_Items in range(7)]

[wxID_WXFRAME1MENU3ITEMS0
] = [wx.NewId() for _init_coll_menu3_Items in range(1)]

[wxID_WXFRAME1MENU4ITEMS0, wxID_WXFRAME1MENU4ITEMS1,
 wxID_WXFRAME1MENU4ITEMS2, wxID_WXFRAME1MENU4ITEMS3,
 wxID_WXFRAME1MENU4ITEMS4, wxID_WXFRAME1MENU4ITEMS5
] = [wx.NewId() for _init_coll_menu4_Items in range(6)]

[wxID_WXFRAME1MENU5ITEMS0, wxID_WXFRAME1MENU5ITEMS1,
 wxID_WXFRAME1MENU5ITEMS2, wxID_WXFRAME1MENU5ITEMS3,
 wxID_WXFRAME1MENU5ITEMS4, wxID_WXFRAME1MENU5ITEMS5
] = [wx.NewId() for _init_coll_menu5_Items in range(6)]

[wxID_WXFRAME1MENU6ITEMS0, wxID_WXFRAME1MENU6ITEMS1,
 wxID_WXFRAME1MENU6ITEMS2, wxID_WXFRAME1MENU6ITEMS3,
 wxID_WXFRAME1MENU6ITEMS4, wxID_WXFRAME1MENU6ITEMS5,
 wxID_WXFRAME1MENU6ITEMS6, wxID_WXFRAME1MENU6ITEMS7
] = [wx.NewId() for _init_coll_menu6_Items in range(8)]

[wxID_WXFRAME1POPUPMENU1ITEMS0, wxID_WXFRAME1POPUPMENU1ITEMS1, 
 wxID_WXFRAME1POPUPMENU1ITEMS2, wxID_WXFRAME1POPUPMENU1ITEMS3, 
 wxID_WXFRAME1POPUPMENU1ITEMS4, wxID_WXFRAME1POPUPMENU1ITEMS5,
 wxID_WXFRAME1POPUPMENU1ITEMS6, wxID_WXFRAME1POPUPMENU1ITEMS7
] = [wx.NewId() for _init_coll_popupmenu1_Items in range(8)]

[wxID_WXFRAME1POPUPMENU2ITEMS0, wxID_WXFRAME1POPUPMENU2ITEMS1, 
 wxID_WXFRAME1POPUPMENU2ITEMS2, wxID_WXFRAME1POPUPMENU2ITEMS3,
 wxID_WXFRAME1POPUPMENU2ITEMS4, wxID_WXFRAME1POPUPMENU2ITEMS5,
 wxID_WXFRAME1POPUPMENU2ITEMS6
] = [wx.NewId() for _init_coll_popupmenu2_Items in range(7)]

[wxID_WXFRAME1TOOLBAR1ITEMS0, wxID_WXFRAME1TOOLBAR1ITEMS1,
 wxID_WXFRAME1TOOLBAR1ITEMS2, wxID_WXFRAME1TOOLBAR1ITEMS3,
 wxID_WXFRAME1TOOLBAR1ITEMS4, wxID_WXFRAME1TOOLBAR1ITEMS5,
 wxID_WXFRAME1TOOLBAR1ITEMS6, wxID_WXFRAME1TOOLBAR1ITEMS7
] = [wx.NewId() for _init_coll_popupmenu2_Items in range(8)]

class Frame1(wx.Frame):
    "GUI for the file manager"

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText1, 0, border=0, flag=wx.CENTER)
        parent.AddWindow(self.multiSelectionDirCtrl1, 1, border=0, 
            flag=wx.EXPAND)
        
    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText2, 0, border=0, flag=wx.CENTER)
        parent.AddWindow(self.treeListCtrl1, 1, border=0, flag=wx.EXPAND)

    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menu1, title=_(u'&File'))
        parent.Append(menu=self.menu4, title=_(u'&Edit'))
        parent.Append(menu=self.menu2, title=_(u'&Tools'))
        parent.Append(menu=self.menu6, title=_(u'&View'))
        parent.Append(menu=self.menu5, title=_(u'&Options'))
        parent.Append(menu=self.menu3, title=_(u'&Help'))
        
    def _init_coll_menu1_Items(self, parent):
        # generated method, don't edit

        item = wx.MenuItem(id=wxID_WXFRAME1MENU1ITEMS0, 
            text=_(u'&New')+u'\tCtrl+N', help=_(u'Start with a new empty file'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-new',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU1ITEMS0, 
            MainFrameMenu.closeFile)

        parent.AppendSeparator()

        item = wx.MenuItem(id=wxID_WXFRAME1MENU1ITEMS1, 
            text=_(u'&Open')+u'\tCtrl+O', help=_(u'Open a compressed file'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-open',wx.ART_MENU ))
        parent.AppendItem(item)      
        wx.EVT_MENU(self, wxID_WXFRAME1MENU1ITEMS1, 
            MainFrameMenu.openFile)
              
        parent.AppendMenu(help=_(u'Open a recently opened file'),
            id=wxID_WXFRAME1MENU1ITEMS2, text=_(u'Open &recent'),
            submenu=self.menuRecent)
              
        parent.AppendSeparator()
        
        item = wx.MenuItem(id=wxID_WXFRAME1MENU1ITEMS3, 
            text=_(u'Set recompression &level')+u'\tCtrl+L', 
            help=_(u'Change the recompression level for the current file'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-refresh',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU1ITEMS3, 
            MainFrameMenu.setRecompressionLevel)
        
        parent.AppendSeparator()
              
        item = wx.MenuItem(help=_(u'Exit from Tarumba'),
            id=wx.ID_EXIT, text=_(u'&Exit')+u'\tCtrl+Q')
        parent.AppendItem(item)
        wx.EVT_MENU(self, wx.ID_EXIT, self.Exit)
        
    def _init_coll_menu2_Items(self, parent):
        # generated method, don't edit

        item = wx.MenuItem(help=_(u'Test the integrity of a compressed file'),
            id=wxID_WXFRAME1MENU2ITEMS0, 
            text=_(u'&Test integrity')+u'\tCtrl+T')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-apply',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU2ITEMS0, 
            MainFrameMenu.testFile)
              
        item = wx.MenuItem(help=_(u'Try to repair a damaged compressed file'),
            id=wxID_WXFRAME1MENU2ITEMS1, text=_(u'&Repair file')+u'\tCtrl+R')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-preferences',wx.ART_MENU))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU2ITEMS1, 
            MainFrameMenu.fixFile)
              
        parent.AppendSeparator()
        
        item = wx.MenuItem(
            help=_(u'Protect any file with standart encryption'),
            id=wxID_WXFRAME1MENU2ITEMS2, text=_(u'&Encrypt file'+u'\tCtrl+E'))
        item.SetBitmap(wx.ArtProvider.GetBitmap(
            'gtk-dialog-authentication',wx.ART_MENU))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU2ITEMS2, 
            MainFrameMenu.encrypt)
              
        item = wx.MenuItem(help=_(u'Decrypt a previously encrypted file'),
            id=wxID_WXFRAME1MENU2ITEMS3, text=_(u'&Decrypt file')+u'\tCtrl+D')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-dnd',wx.ART_MENU))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU2ITEMS3, 
            MainFrameMenu.decrypt)
              
        parent.AppendSeparator()
        
        item = wx.MenuItem(
            help=_(u'Split any file to get several smaller files'),
            id=wxID_WXFRAME1MENU2ITEMS4, 
            text=_(u'&Split in generic volumes')+u'\tCtrl+S')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-cut',wx.ART_MENU))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU2ITEMS4, 
            MainFrameMenu.split)
              
        item = wx.MenuItem(
            help=_(u'Join splitted files to get the original file'),
            id=wxID_WXFRAME1MENU2ITEMS5, 
            text=_(u'&Join generic volumes')+u'\tCtrl+J')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-dnd-multiple',wx.ART_MENU))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU2ITEMS5, 
            MainFrameMenu.join)
              
        parent.AppendSeparator()
        
        item = wx.MenuItem(
            help=_(u'Join multivolume zip files created with other programs'),
            id=wxID_WXFRAME1MENU2ITEMS6, 
            text=_(u'Join multivolume &zip')+u'\tCtrl+Z')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-dnd-multiple',wx.ART_MENU))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU2ITEMS6, 
            MainFrameMenu.joinZip)
              
    def _init_coll_menu3_Items(self, parent):
        # generated method, don't edit

        item = wx.MenuItem(help=_(u'Open the Tarumba user\'s manual'),
              id=wxID_WXFRAME1MENU3ITEMS0, text=_(u'User &manual')+u'\tCtrl+M',
              kind=wx.ITEM_NORMAL)
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-help',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU3ITEMS0, self.Manual)
              
        item = wx.MenuItem(help=_(u'Tarumba\'s version info and credits'),
              id=wx.ID_ABOUT, text=_(u'&About Tarumba'))
        parent.AppendItem(item)   
        wx.EVT_MENU(self, wx.ID_ABOUT, self.About)
        
    def _init_coll_menu4_Items(self, parent):
        # generated method, don't edit
        
        item = wx.MenuItem(help=_(u'Search files inside the compressed file'),
            id=wxID_WXFRAME1MENU4ITEMS0, 
            text=_(u'Search in &compressed')+u'\tCtrl+F')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-find',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU4ITEMS0, SearchTools.searchArchive)
              
        item = wx.MenuItem(help=_(u'Search files inside the file system'),
            id=wxID_WXFRAME1MENU4ITEMS1, 
            text=_(u'Search in &file system'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-find',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU4ITEMS1, SearchTools.searchLocal)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(
            help=_(u'Copy the items selected in the compressed file'),
            id=wxID_WXFRAME1MENU4ITEMS2, 
            text=_(u'&Copy from compressed')+u'\tCtrl+C')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-copy',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU4ITEMS2, Clipboard.TreeListCopy)
           
        item = wx.MenuItem(
            help=_(u'Paste the files in clipboard to the compressed file'),
            id=wxID_WXFRAME1MENU4ITEMS3, 
            text=_(u'&Paste to compressed')+u'\tCtrl+V')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-paste',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU4ITEMS3, Clipboard.TreeListPaste)
            
        parent.AppendSeparator()
        
        item = wx.MenuItem(
            help=_(u'Copy the items selected in the file system'),
            id=wxID_WXFRAME1MENU4ITEMS4, 
            text=_(u'Copy &from file system'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-copy',wx.ART_MENU ))
        parent.AppendItem(item) 
        wx.EVT_MENU(self, wxID_WXFRAME1MENU4ITEMS4, Clipboard.DirCtrlCopy)  
         
        item = wx.MenuItem(
            help=_(u'Paste the files in clipboard to the file system'),
            id=wxID_WXFRAME1MENU4ITEMS5, 
            text=_(u'Paste &to file system'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-paste',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU4ITEMS5, Clipboard.DirCtrlPaste)
        
    def _init_coll_menu5_Items(self, parent):
        # generated method, don't edit
        
        item = wx.MenuItem(help=_(u'Make the speeker beep when a process finishes'),
            id=wxID_WXFRAME1MENU5ITEMS0, text=_(u'&Beep when done'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU5ITEMS0, MainFrameMenu.BeepOption)
        
        item = wx.MenuItem(help=_(u'Keep a history of the recently opened files'),
            id=wxID_WXFRAME1MENU5ITEMS5, text=_(u'&Remember recently opened'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU5ITEMS5, MainFrameMenu.RememeberRecentlyOpened)
        
        item = wx.MenuItem(help=_(u'Process the symlinks as the files they link'),
            id=wxID_WXFRAME1MENU5ITEMS1, text=_(u'&Follow symlinks'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU5ITEMS1, MainFrameMenu.FollowLinksOption)
        
        item = wx.MenuItem(help=_(u'Overwrite existing files without confirmation'),
            id=wxID_WXFRAME1MENU5ITEMS2, text=_(u'No prompt to &overwrite'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU5ITEMS2, MainFrameMenu.ConfirmOverwriteOption)
        
        item = wx.MenuItem(help=_(u'No encryption will be offered when adding files'),
            id=wxID_WXFRAME1MENU5ITEMS3, text=_(u'No ask to &encrypt'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU5ITEMS3, MainFrameMenu.AskToEncryptOption)
              
        parent.AppendSeparator()
        
        item = wx.MenuItem(help=_(u'Temporal and auxiliar program\'s path configuration'),
            id=wxID_WXFRAME1MENU5ITEMS4, text=_(u'&Paths')+u'\tCtrl+P')
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-properties',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU5ITEMS4, MainFrameMenu.PathOptions)
              
    def _init_coll_menu6_Items(self, parent):
        # generated method, don't edit
        
        item = wx.MenuItem(help=_(u'Show the hidden files in the file system'),
            id=wxID_WXFRAME1MENU6ITEMS0, text=_(u'Show &hidden files')+u'\tCtrl+H',
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS0, MainFrameMenu.ShowHidden)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(help=_(u'Show the tool bar for easy file operation'),
            id=wxID_WXFRAME1MENU6ITEMS1, text=_(u'Show &tool bar'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS1, MainFrameMenu.ShowToolBar)
        
        item = wx.MenuItem(help=_(u'Show the status bar with additional help'),
            id=wxID_WXFRAME1MENU6ITEMS2, text=_(u'Show &status bar'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS2, MainFrameMenu.ShowStatusBar)
        
        item = wx.MenuItem(help=_(u'Enable the file system as part of the expert mode'),
            id=wxID_WXFRAME1MENU6ITEMS3, text=_(u'Show &file system'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS3, MainFrameMenu.ShowFileSystem)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(help=_(u'Configures the GUI for easy usage'),
            id=wxID_WXFRAME1MENU6ITEMS4, text=_(u'Set &easy mode'))
        item.SetBitmap(wx.Bitmap(self.TARUMBA_ICONS+'/gtk-select-color.png',
            wx.BITMAP_TYPE_PNG))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS4, MainFrameMenu.SetEasyMode)
        
        item = wx.MenuItem(help=_(u'Configures the GUI with advanced options'),
            id=wxID_WXFRAME1MENU6ITEMS5, text=_(u'Set e&xpert mode'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-page-setup',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS5, MainFrameMenu.SetExpertMode)
        
        item = wx.MenuItem(help=_(u'Shows all the elements in the GUI'),
            id=wxID_WXFRAME1MENU6ITEMS6, text=_(u'Set &full mode'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-fullscreen',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS6, MainFrameMenu.SetFullMode)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(help=_(u'Use a single-tree manager for file operations'),
            id=wxID_WXFRAME1MENU6ITEMS7, text=_(u'&Compact file view'),
            kind=wx.ITEM_CHECK)
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1MENU6ITEMS7, MainFrameMenu.AlternativeFileView)
        
    def _init_coll_popupmenu1_Items(self, parent):
        # generated method, don't edit

        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS0, 
            text=_(u'Edit with Tarumba'),
            help=_(u'Load the selected compressed file in Tarumba'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-edit',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS0, self.OpenFile)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS1, 
            text=_(u'Open'),
            help=_(u'Open the selected file with the default program'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-execute',wx.ART_MENU ))
        parent.AppendItem(item)
        
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS1, self.ExternalOpenLocalDefault)
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS2, 
            text=_(u'Open with...'),
            help=_(u'Open the selected file with a custom program'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-find-and-replace',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS2, self.ExternalOpenLocalWith)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS3, 
            text=_(u'Add to the compressed file'),
            help=_(u'Add the selected files/folders to the current compressed'))
        item.SetBitmap(wx.Bitmap(self.TARUMBA_ICONS+'/gtk-go-forward.png',
            wx.BITMAP_TYPE_PNG))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS3, self.AddToFile)
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS4, 
            text=_(u'Add to a new compressed file'),
            help=_(u'Create a new compressed file with the selected contents'))
        item.SetBitmap(wx.Bitmap(self.TARUMBA_ICONS+'/gtk-jump-to.png',
            wx.BITMAP_TYPE_PNG))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS4, self.CreateCompressed)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS5, 
            text=_(u'Create new folder'),
            help=_(u'Create a new folder in the selected path'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-directory',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS5, self.NewFolderLocal)
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS6, 
            text=_(u'Move/Rename'),
            help=_(u'Move or rename the selected file or folder'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-sort-ascending',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS6, self.RenameLocal)
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU1ITEMS7, 
            text=_(u'Delete'),
            help=_(u'Delete the selected files and folders'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-delete',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU1ITEMS7, self.DeleteLocal)
        
    def _init_coll_popupmenu2_Items(self, parent):
        # generated method, don't edit
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU2ITEMS0, 
            text=_(u'Open'),
            help=_(u'Open the selected file with the default program'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-execute',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU2ITEMS0, self.ExternalOpenCompressedDefault)
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU2ITEMS1, 
            text=_(u'Open with...'),
            help=_(u'Open the selected file with a custom program'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-find-and-replace',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU2ITEMS1, self.ExternalOpenCompressedWith)
        
        parent.AppendSeparator()
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU2ITEMS2, 
            text=_(u'Extract the selected files'),
            help=_(u'Extract the selection to the current path in the file system'))
        item.SetBitmap(wx.Bitmap(self.TARUMBA_ICONS+'/gtk-go-back.png',
            wx.BITMAP_TYPE_PNG))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU2ITEMS2, self.ExtractFiles)
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU2ITEMS3, 
            text=_(u'Extract all the files'),
            help=_(u'Extract all the files to the current path in the file system'))
        item.SetBitmap(wx.Bitmap(self.TARUMBA_ICONS+'/gtk-extract-all-2.png',
            wx.BITMAP_TYPE_PNG))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU2ITEMS3, self.ExtractAll)
        
        parent.AppendSeparator()
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU2ITEMS4, 
            text=_(u'Create new folder'),
            help=_(u'Create a new folder in the selected path'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-directory',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU2ITEMS4, self.NewFolder)
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU2ITEMS5, 
            text=_(u'Move/Rename'),
            help=_(u'Move or rename the selected file or folder'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-sort-ascending',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU2ITEMS5, self.Rename)
        
        item = wx.MenuItem(id=wxID_WXFRAME1POPUPMENU2ITEMS6, 
            text=_(u'Delete'),
            help=_(u'Delete the selected files and folders'))
        item.SetBitmap(wx.ArtProvider.GetBitmap('gtk-delete',wx.ART_MENU ))
        parent.AppendItem(item)
        wx.EVT_MENU(self, wxID_WXFRAME1POPUPMENU2ITEMS6, self.DeleteFiles)

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar1 = wx.MenuBar()

        self.menu1 = wx.Menu(title='')
        self.menu2 = wx.Menu(title='')
        self.menu3 = wx.Menu(title='')
        self.menu4 = wx.Menu(title='')
        self.menu5 = wx.Menu(title='')
        self.menu6 = wx.Menu(title='')
        
        self.menuRecent = wx.Menu(title='')
        
        self.popupmenu1 = wx.Menu(title='')
        self.popupmenu2 = wx.Menu(title='')

        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_menu1_Items(self.menu1)
        self._init_coll_menu2_Items(self.menu2)
        self._init_coll_menu3_Items(self.menu3)
        self._init_coll_menu4_Items(self.menu4)
        self._init_coll_menu5_Items(self.menu5)
        self._init_coll_menu6_Items(self.menu6)
        
        self._init_coll_popupmenu1_Items(self.popupmenu1)
        self._init_coll_popupmenu2_Items(self.popupmenu2)  
        
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)

        self.panel1.SetSizer(self.boxSizer1)
        self.panel2.SetSizer(self.boxSizer2)
        
    def _init_toolbar(self):
        # generated method, don't edit
        tsize = (24,24)
        self.toolBar1.SetToolBitmapSize(tsize)
        
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS0, _(u'New'), 
            wx.ArtProvider.GetBitmap('gtk-new', wx.ART_TOOLBAR, tsize), 
            longHelp=_(u'Start with a new empty file'))
        self.Bind(wx.EVT_TOOL, MainFrameMenu.closeFile, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS0)
            
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS1, _(u'Open'), 
            wx.ArtProvider.GetBitmap('gtk-open', wx.ART_TOOLBAR, tsize), 
            longHelp=_(u'Open a compressed file'))
        self.Bind(wx.EVT_TOOL, MainFrameMenu.openFile, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS1)
            
        self.toolBar1.AddSeparator()
        
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS2, _(u'Add file'), 
            wx.Bitmap(self.TARUMBA_ICONS+'/gtk-add-file.png',
            wx.BITMAP_TYPE_PNG), 
            longHelp=_(u'Add a file to the current compressed'))
        self.Bind(wx.EVT_TOOL, MainFrameMenu.addFile, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS2)
        
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS3, _(u'Add folder'), 
            wx.Bitmap(self.TARUMBA_ICONS+'/gtk-add-folder.png',
            wx.BITMAP_TYPE_PNG), 
            longHelp=_(u'Add a folder to the current compressed'))
        self.Bind(wx.EVT_TOOL, MainFrameMenu.addFolder, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS3)
        
        self.toolBar1.AddSeparator()
        
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS4, _(u'Extract sel.'),
            wx.Bitmap(self.TARUMBA_ICONS+'/gtk-go-up.png',
            wx.BITMAP_TYPE_PNG),
            longHelp=_(u'Extract the selected files and folders'))
        self.Bind(wx.EVT_TOOL, MainFrameMenu.extractSelected, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS4)
        
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS5, _(u'Extract all'), 
            wx.Bitmap(self.TARUMBA_ICONS+'/gtk-extract-all.png',
            wx.BITMAP_TYPE_PNG), 
            longHelp=_(u'Extract all the files and folders'))
        self.Bind(wx.EVT_TOOL, MainFrameMenu.extractAll, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS5)
        
        self.toolBar1.AddSeparator()
        
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS6, _(u'Delete sel.'), 
            wx.ArtProvider.GetBitmap('gtk-delete', wx.ART_TOOLBAR, tsize), 
            longHelp=_(u'Delete the selected files and folders'))
        self.Bind(wx.EVT_TOOL, self.DeleteFiles, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS6)
        
        self.toolBar1.AddLabelTool(wxID_WXFRAME1TOOLBAR1ITEMS7, _(u'Open sel.'), 
            wx.ArtProvider.GetBitmap('gtk-execute', wx.ART_TOOLBAR, tsize), 
            longHelp=_(u'Open the selected file with the default program'))
        self.Bind(wx.EVT_TOOL, self.ExternalOpenCompressedDefault, 
            id=wxID_WXFRAME1TOOLBAR1ITEMS7)
        
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
             size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE, 
             title=u'Tarumba')
        self._init_utils()
        self.SetClientSize(wx.Size(800, 600))
        self.SetSizeHints(800, 600)
        self.SetMenuBar(self.menuBar1)

        self.splitterWindow1 = wx.SplitterWindow(id=wxID_FRAME1SPLITTERWINDOW1,
              name='splitterWindow1', parent=self,  style=wx.SP_3D)
        self.splitterWindow1.SetMinimumPaneSize(50)

        self.splitterWindow2 = wx.SplitterWindow(id=wxID_FRAME1SPLITTERWINDOW2,
              name='splitterWindow2', parent=self.splitterWindow1,
              style=wx.SP_3D)
        self.splitterWindow2.SetMinimumPaneSize(50)

        self.colorLogCtrl1 = ColorLogCtrl(id=wxID_FRAME1COLORLOGCTRL1, 
              name='colorLogCtrl1', parent=self.splitterWindow1)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1',
              parent=self.splitterWindow2,  style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2',
              parent=self.splitterWindow2,  style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=_(u'File system'), name='staticText1',
              parent=self.panel1, 
              style=wx.ALIGN_CENTER)

        # Dir-tree + file-list version of the file manager
        if Globals.ALTERNATIVE_TREEVIEW:
            self.multiSelectionDirCtrl1 = AlternativeDirCtrl1(defaultFilter=0, 
                  dir=os.getcwd(), filter='', id=wxID_FRAME1MULTISELECTIONDIRCTRL1, 
                  name='multiSelectionDirCtrl1', parent=self.panel1, 
                  style=wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER)
        # Single-tree version of the file manager
        else:
            self.multiSelectionDirCtrl1 = MultiSelectionDirCtrl(defaultFilter=0, 
                  dir=os.getcwd(), filter='', id=wxID_FRAME1MULTISELECTIONDIRCTRL1, 
                  name='multiSelectionDirCtrl1', parent=self.panel1, 
                  style=wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=Utilities.BasenameMod(Globals.file), name='staticText2',
              parent=self.panel2, 
              style=wx.ALIGN_CENTER)

        # Dir-tree + file-list version of the compressed file
        if Globals.ALTERNATIVE_TREEVIEW:
            self.treeListCtrl1 = AlternativeTreeList1(id=wxID_FRAME1TREELISTCTRL1,
                  name='treeListCtrl1', parent=self.panel2)
        # Single-tree version of the compressed file
        else:
            self.treeListCtrl1 = CustomTreeListCtrl(id=wxID_FRAME1TREELISTCTRL1,
                  name='treeListCtrl1', parent=self.panel2)
              
        self.toolBar1 = wx.ToolBar(id=wxID_FRAME1TOOLBAR1, name='toolBar1',
              parent=self, style=wx.TB_HORIZONTAL | wx.TB_TEXT | wx.TB_NO_TOOLTIPS)
        self.SetToolBar(self.toolBar1)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self.SetStatusBar(self.statusBar1)
        
        self.splitterWindow1.SplitHorizontally(self.splitterWindow2,
              self.colorLogCtrl1, self.splitterWindow1.GetSize().GetHeight()-150)
              
        self.splitterWindow2.SplitVertically(self.panel1, self.panel2, 
              self.splitterWindow2.GetSize().GetWidth()/2)
        
        self._init_toolbar()
            
        self._init_sizers()

    def __init__(self, parent):
        "Creates the GUI for the file manager."
        
        # Get the icon's path
        self.TARUMBA_ICONS = os.getenv('TARUMBA_ICONS')
        if not(self.TARUMBA_ICONS):
            self.TARUMBA_ICONS = os.path.join(os.path.dirname(sys.argv[0]), 'icons')
        
        # Call to BOA auto-generated functions
        self._init_ctrls(parent)
        
        # Set the icon for the window
        bundle = wx.IconBundle()
        bundle.AddIconFromFile(self.TARUMBA_ICONS+'/64x64.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(self.TARUMBA_ICONS+'/48x48.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(self.TARUMBA_ICONS+'/32x32.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(self.TARUMBA_ICONS+'/24x24.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(self.TARUMBA_ICONS+'/22x22.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(self.TARUMBA_ICONS+'/16x16.png',
            wx.BITMAP_TYPE_PNG)
        self.SetIcons(bundle)
        
        # Rigth click to show popup menus
        self.multiSelectionDirCtrl1.EventRightClick(self.OnmultiSelectionDirCtrl1RightDown)
        self.treeListCtrl1.EventRightClick(self.OntreeListCtrl1RightDown)
        
        # Double click (or enter) can be used to open files
        self.multiSelectionDirCtrl1.EventDoubleClick(self.ExternalOpenLocalDefault)
        self.treeListCtrl1.EventDoubleClick(self.ExternalOpenCompressedDefault)
            
        # Show the help for the popus in the status bar
        wx.EVT_MENU_HIGHLIGHT_ALL(self.popupmenu1, self.ShowHelpStringPopupMenu1)
        wx.EVT_MENU_HIGHLIGHT_ALL(self.popupmenu2, self.ClearHelpString)
        wx.EVT_MENU_CLOSE(self.popupmenu1, self.ClearHelpString)
        wx.EVT_MENU_CLOSE(self.popupmenu2, self.ClearHelpString)
            
        # Init the drag and drog
        DragNDrop.InitDragDropDirCtrl(self, self.multiSelectionDirCtrl1)
        DragNDrop.InitDragDropTreeList(self, self.treeListCtrl1)
        
        # Define the default log output
        Globals.OUTPUT_LOG=self.colorLogCtrl1
        # Define the parent of the dialogs
        Globals.PARENT=self
        
        # Set de menus in "no file" mode
        self.MenusSetNofile()
        
        # Load the last opened list
        self.lastOpenedIds = []
        for i in range(11):
            self.lastOpenedIds.append(wx.NewId())
        MainFrameMenu.updateLastOpened(None)
        # Enable or disable the menu
        self.menu1.Enable(wxID_WXFRAME1MENU1ITEMS2,Globals.REMEMBER_RECENTLY)
        
        # Update the status of the GUI options
        MainFrameMenu.ShowHidden(None)
        MainFrameMenu.ShowToolBar(None)
        MainFrameMenu.ShowStatusBar(None)
        MainFrameMenu.ShowFileSystem(None)
        MainFrameMenu.AlternativeFileView(None)
        MainFrameMenu.BeepOption(None)
        MainFrameMenu.RememeberRecentlyOpened(None)
        MainFrameMenu.FollowLinksOption(None)
        MainFrameMenu.ConfirmOverwriteOption(None)
        MainFrameMenu.AskToEncryptOption(None)
        
        # Disable not available options
        MainFrameMenu.DisableUnavailableOptions()
        
        # Show the tip of the day
        Utilities.Log(TipOfTheDay.message(),Utilities.SPAM)
        
        # Check if the gettext resources were available
        if not Globals.LOCALE_AVAILABLE:
            Utilities.Log(_(u'Tarumba is not available in your languaje, ' \
                u'please help us to translate it.'), Utilities.WARN)

    def OnmultiSelectionDirCtrl1RightDown(self,event):
        "Shows the PopupMenu in the DirCtrl"
        event.GetEventObject().PopupMenu(self.popupmenu1, event.GetPosition())
        
    def OntreeListCtrl1RightDown(self,event):
        "Shows the PopupMenu in the TreeListCtrl"
        # Do not show it if the file system is hidden
        if Globals.SHOW_FILESYSTEM:
            event.GetEventObject().PopupMenu(self.popupmenu2, event.GetPosition())
        
    def ClearHelpString(self,event):
        "Clears the help string"
        self.PopStatusText()
    
    def ShowHelpStringPopupMenu1(self,event):
        "Shows help strings for popup menus on the status bar"
        self.PopStatusText()
        self.PushStatusText(self.popupmenu1.GetHelpString(event.GetMenuId()))
        
    def ShowHelpStringPopupMenu2(self,event):
        "Shows help strings for popup menus on the status bar"
        self.PushStatusText(self.popupmenu2.GetHelpString(event.GetMenuId()))

######################
## CUSTOM FUNCTIONS ##
######################

    def OpenFile(self, event):
        "Open a compressed file"
        self.busy = None
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the name of the selected files
        selFiles = self.multiSelectionDirCtrl1.GetPaths()
        # If a files has been selected
        if len(selFiles)==1:
            try :
                # Changes the cursor to the busy cursor
                self.busy = wx.BusyCursor()
                # Set the name of the file and reset the options
                Globals.file = selFiles[0]
                Globals.compressionOptions = Globals.CompressionOptions()
                # Shows the selected file in the TreeListCtrl
                error, output = CompressionManager.list(
                    Globals.file, self.treeListCtrl1)
                # Show the result
                if error:
                    Utilities.Log(output,Utilities.ERRO)
                else:
                    Utilities.Log(output,Utilities.INFO)
                    # Update the last opened files
                    MainFrameMenu.updateLastOpened(Globals.file)
                # If everything is Ok, change the tile
                if not error:   
                    self.staticText2.SetLabel(
                        Utilities.BasenameMod(Globals.file))
                # Otherwise change to "no file" mode
                else:
                    # Reset Globals.file because we set it
                    # This avoids the file closed message
                    Globals.file = Globals.NO_FILE
                    MainFrameMenu.closeFile(None)
                # PATCH: Fixes the expand problem in the treeListCtrl
                self.treeListCtrl1.ExpandAll(self.treeListCtrl1.GetRootItem())
            finally :
                # Sets the normal cursor again
                if self.busy:
                    del self.busy
        # If no selected file shows an error message
        else:
            Utilities.Log(_(u'You need to select the file that ' \
                u'you want to open.'),Utilities.ERRO)
    
    def ExtractFiles(self, event):
        "Extract the selected files to the selected path"
        # If null event we have called it
        self.busy = None
        if event:
            event.StopPropagation()
        # Get the selected files ids
        files = self.treeListCtrl1.GetSelections()
        # Test that at least one has been selected
        if len(files)<1:
            Utilities.Log(_(u'No files have been selected.'),
                Utilities.ERRO)
            Utilities.Beep()
            return
        # Get the name of the selected folder
        folder = self.multiSelectionDirCtrl1.GetPaths()
        # Check that only one folder has been selected
        if len(folder)!=1:
            Utilities.Log(_(u'You need to select the folder where to ' \
            u'extract the files.'),Utilities.ERRO)
            Utilities.Beep()
            return
        # If a file is selected, get it's folder
        if not os.path.isdir(folder[0]):
            folder[0] = os.path.dirname(folder[0])
        try:
            # Change the cursor to busy cursor
            self.busy = wx.BusyCursor()
            # Extract the files via the manager
            error, output = CompressionManager.extract(Globals.file, 
                self.treeListCtrl1, folder[0])
            # Show the result
            if error:
                Utilities.Log(output,Utilities.ERRO)
            elif output:
                Utilities.Log(output,Utilities.INFO)
        finally :
            # Sets the normal cursor again
            if self.busy:
                del self.busy
        # Updates the file system
        self.multiSelectionDirCtrl1.ReCreateTree()
        self.multiSelectionDirCtrl1.SetPath(folder[0])
                
    def ExtractAll(self,event):
        "Extract all the files."
        self.treeListCtrl1.SelectItem(self.treeListCtrl1.GetRootItem())
        self.ExtractFiles(None)
        
    def CreateCompressed(self,event):
        "Compress the selected files into a new archive."
        self.busy = None
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the name for the selected files/folders
        contents = self.multiSelectionDirCtrl1.GetPaths()
        if (len(contents)<1):
            Utilities.Log(_(u'There are no selected files.'),
                Utilities.ERRO)
            Utilities.Beep()
            return
        # Rename the compressed file as the first content
        Globals.file = contents[0]
        # Show the dialog with the compression options
        dialog = CompressionDialog.create(self,
            ((len(contents)>1) or os.path.isdir(contents[0])))
        if dialog.ShowModal() == wx.ID_OK:
            try:
                # Change the cursor to busy cursor
                self.busy = wx.BusyCursor()
                # Create the compressed archive via the manager
                error, output = CompressionManager.add(
                    Globals.file, contents, '', None, 
                    Globals.compressionOptions)
                # Updates the file system (to show the new file)
                self.multiSelectionDirCtrl1.ReCreateTree()
                self.multiSelectionDirCtrl1.SetPath(contents[0])
                # Show the results
                if error:
                    Utilities.Log(output,Utilities.ERRO)
                else:
                    Utilities.Log(output,Utilities.INFO)
                # Reload the archive in the TreeListCtrl
                error, output = CompressionManager.list(
                    Globals.file,self.treeListCtrl1)
                # If everything is Ok, change the title
                if not error:   
                    self.staticText2.SetLabel(
                        Utilities.BasenameMod(Globals.file))
                # Otherwise change to "no file" mode and inform
                else:
                    # Reset Globals.file because we set it
                    # This avoids the file closed message
                    Globals.file = Globals.NO_FILE
                    MainFrameMenu.closeFile(None)
                # PATCH: Fixes the expand problem in the treeListCtrl
                self.treeListCtrl1.ExpandAll(self.treeListCtrl1.GetRootItem())
            finally :
                # Sets the normal cursor again
                if self.busy:
                    del self.busy
                # End the compression dialog
                dialog.Destroy()   
                    
    def AddToFile(self,event):
        "Add the selected files to the current archive."
        self.busy = None
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the name for the selected files/folders
        contents = self.multiSelectionDirCtrl1.GetPaths()
        if (len(contents)<1):
            Utilities.Log(_(u'There are no selected files.'),
                Utilities.ERRO)
            Utilities.Beep()
            return
        # Get the destination folder in the compressed archive
        dirId = self.treeListCtrl1.GetSelections()
        # If nothing selected, add to the main folder
        if len(dirId) < 1:
            folder = ''
        # If more than one selected show error
        elif len(dirId) > 1:
            Utilities.Log(_(u'You cannot select more than one destination in the' \
                ' compressed file.'),
                Utilities.ERRO)
            Utilities.Beep()
            return
        else:
            folderInfo = self.treeListCtrl1.GetPyData(dirId[0])
            folder = folderInfo[0]
            # If not a folder get it's parent
            if folder and (not folder[-1] == '/'):
                folder = os.path.dirname(folder)
        try:
            # Change the cursor to busy cursor
            self.busy = wx.BusyCursor()
            # Add the files via the compression manager
            error, output = CompressionManager.add(
                Globals.file, contents, folder, self.treeListCtrl1, 
                Globals.compressionOptions)
            # Show the result
            if error:
                Utilities.Log(output,Utilities.ERRO)
            elif output:
                Utilities.Log(output,Utilities.INFO)
            # Reload the archive in the TreeListCtrl
            error, output = CompressionManager.list(
                Globals.file, self.treeListCtrl1)
            # If there is a problem change to "no file" mode
            if error:
                MainFrameMenu.closeFile(None)
            else:
                # PATCH: Fixes the expand problem in the treeListCtrl
                self.treeListCtrl1.ExpandAll(self.treeListCtrl1.GetRootItem())
                # Re-select the destination folder, so it can be found easily
                if folder:
                    exists, nodeId = Utilities.CheckFileExistsOnTree(folderInfo[0], 
                        self.treeListCtrl1, folderInfo[1])
                    self.treeListCtrl1.SelectItem(nodeId)
                    self.treeListCtrl1.EnsureVisible(nodeId)
            
        finally :
            # Sets the normal cursor again
            if self.busy:
                del self.busy
                    
    def DeleteFiles(self, event):
        "Delete the selected files from the current compressed archive."
        self.busy = None
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Check that at least one has been selected
        ids = self.treeListCtrl1.GetSelections()
        if len(ids)<1:
            Utilities.Log(_(u'There are no selected files.'),
                Utilities.ERRO)
            Utilities.Beep()
            return
        try:
            # Change the cursor to busy cursor 
            self.busy = wx.BusyCursor()
            # Delete the files via the compression manager
            error, output = CompressionManager.delete(
                Globals.file, self.treeListCtrl1, Globals.compressionOptions)            
            # Show the result
            if error:
                Utilities.Log(output,Utilities.ERRO)
            elif output:
                Utilities.Log(output,Utilities.INFO)
            # If not error and output None, the user did not confirm the action
            if (error or output):
                # Reload the file in the TreeListCtrl
                error, output = CompressionManager.list(
                    Globals.file, self.treeListCtrl1)
                # If there is a problem change to "no file" mode
                if error:
                    MainFrameMenu.closeFile(None)
                else:
                    # PATCH: Fixes the expand problem in the treeListCtrl
                    self.treeListCtrl1.ExpandAll(self.treeListCtrl1.GetRootItem())
        finally :
            # Sets the normal cursor again
            if self.busy:
                del self.busy
                
    def NewFolder(self,event):
        "Creates a new folder in the compressed file"
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Declare the tmpFolder variable because used in finally clause
        tmpFolder = None
        # If a file is selected, use it's path for the base
        folder = ''
        ids = self.treeListCtrl1.GetSelections()
        if len(ids)==1:
            folder = os.path.dirname(self.treeListCtrl1.GetPyData(ids[0])[0])
        # Ask for the full path of the new folder
        dialog = wx.TextEntryDialog(self, 
            _(u'Input the path for the new folder:'),'', '')
        dialog.SetValue(folder + '/' + _(u'new_folder'))
        if dialog.ShowModal() == wx.ID_OK:
            try:
                # Change the cursor to busy cursor
                self.busy = wx.BusyCursor()
                # Create the new folder into a temporary one
                tmpFolder = Temporary.tmpDir()
                nomDirAux = dialog.GetValue()
                # Be carefull with absolute paths and end slashes
                while len(nomDirAux) > 0 and nomDirAux[0] == '/':
                    nomDirAux = nomDirAux[1:]
                while len(nomDirAux) > 0 and nomDirAux[-1] == '/':
                    nomDirAux = nomDirAux[:-1]
                # Exit if no folder name given
                if not nomDirAux:
                    return
                # Create the given folder into the temporary
                newDir = os.path.join(tmpFolder, nomDirAux)
                Utilities.CreateFolder(newDir)
                # Allow multiple folder level to be created
                basefol = os.path.dirname(nomDirAux)
                # Add the files via the compression manager
                error, output = CompressionManager.add(
                    Globals.file, [newDir], basefol, self.treeListCtrl1,
                    Globals.compressionOptions)
                # Show the result
                if error:
                    Utilities.Log(output,Utilities.ERRO)
                elif output:
                    Utilities.Log(output,Utilities.INFO)
                # Reload the archive in the TreeListCtrl
                error, output = CompressionManager.list(
                    Globals.file, self.treeListCtrl1)
                # If there is a problem change to "no file" mode
                if error:
                    MainFrameMenu.closeFile(None)
            # PATCH: Fixes the expand problem in the treeListCtrl
                self.treeListCtrl1.ExpandAll(self.treeListCtrl1.GetRootItem())
            finally :
                # Sets the normal cursor again
                if self.busy:
                    del self.busy
                # Destroy the dialog
                dialog.Destroy()
                # Destroy the temporary folder
                if tmpFolder:
                    Utilities.DeleteFile(tmpFolder)
                    
    def Rename(self,event):
        "Renames or moves a file or folder inside the archive"
        self.busy = None
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Check that one has been selected
        ids = self.treeListCtrl1.GetSelections()
        if len(ids)!=1:
            Utilities.Log(_(u'Select one file or folder to be renamed.'),
                Utilities.ERRO)
            Utilities.Beep()
            return
        # Ask for the new filename
        filenameAux = self.treeListCtrl1.GetPyData(ids[0])[0]
        # Delete slashes at the end
        if filenameAux[-1] == '/':
            filenameAux = filenameAux[:-1]
        dialog = wx.TextEntryDialog(self, 
            _(u'Input the new name/path:'),'', '')
        dialog.SetValue(filenameAux)
        if dialog.ShowModal() != wx.ID_OK:
            return
        try:
            newName = dialog.GetValue()
            # Exit on empty name
            if not newName:
                return
            # Delete slashes at the end
            if newName[-1] == '/':
                newName = newName[:-1]
            # Avoid things like /../
            if newName[0] == '/':
                newName = newName[1:]
            if newName != os.path.normpath(newName) or newName[0] == '/':
                Utilities.Log(_(u'The name %s is not allowed.')%newName, 
                    Utilities.ERRO)
                Utilities.Beep()
                return
            # Change the cursor to busy cursor 
            self.busy = wx.BusyCursor()
            # Rename the files via the compression manager
            error, output = CompressionManager.rename(
                Globals.file, self.treeListCtrl1, newName, Globals.compressionOptions)            
            # Show the result
            if error:
                Utilities.Log(output,Utilities.ERRO)
            else:
                Utilities.Log(output,Utilities.INFO)
            # Reload the file in the TreeListCtrl
            error, output = CompressionManager.list(
                Globals.file, self.treeListCtrl1)
            # If there is a problem change to "no file" mode
            if error:
                MainFrameMenu.closeFile(None)
            # PATCH: Fixes the expand problem in the treeListCtrl
            self.treeListCtrl1.ExpandAll(self.treeListCtrl1.GetRootItem())
        finally :
            # Sets the normal cursor again
            if self.busy:
                del self.busy
              
########################
## AUXILIAR FUNCTIONS ##
########################

    def MenusSetReadonly(self):
        "Enables only the read actions on the menus"
        # Add to file
        self.popupmenu1.Enable(
            wxID_WXFRAME1POPUPMENU1ITEMS3, False)
        # Open
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS0, True)
        # Open with
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS1, True)
        # Extract selected files
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS2, True)
        # Extract all
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS3, True)
        # Create new folder
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS4, False)
        # Move/rename
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS5, False)
        # Delete selected files
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS6, False)
        # Recompression level
        self.menu1.Enable(
            wxID_WXFRAME1MENU1ITEMS3, False)
        # Search
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS0, True)
        # Copy
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS2, True)
        # Paste
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS3, False)
        # Toolbar - add
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS2, False)
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS3, False)
        # Toolbar - extract
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS4, False)
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS5, False)
        # Toolbar - delete
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS6, False)
        # Toolbar - open
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS7, True)
            
        # Disable drop events on the TreeListCtrl
        DragNDrop.READONLY = True
        
            
    def MenusSetNopack(self):
        "Disables the pack related actions on the menus"
        # Same as Readonly but can only extract all the files
        self.MenusSetReadonly()
        # Extract selected files
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS2, False)
            
    def MenusSetNofile(self):
        "Disables all actions over files"
        # Add to file
        self.popupmenu1.Enable(
            wxID_WXFRAME1POPUPMENU1ITEMS3, False)
        # Open
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS0, False)
        # Open with
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS1, False)
        # Extract selected files
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS2, False)
        # Extract all
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS3, False)
        # Create new folder
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS4, False)
        # Move/rename
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS5, False)
        # Delete selected files
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS6, False)
        # Recompression level
        self.menu1.Enable(
            wxID_WXFRAME1MENU1ITEMS3, False)
        # Search
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS0, False)
        # Copy
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS2, False)
        # Paste can be used to create a new file - ENABLED
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS3, True)
        # Toolbar - add can be used to create a new file - ENABLED
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS2, True)
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS3, True)
        # Toolbar - extract
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS4, False)
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS5, False)
        # Toolbar - delete
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS6, False)
        # Toolbar - open
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS7, False)
            
        # Enable drop events on the TreeListCtrl
        DragNDrop.READONLY = False
            
    def MenusSetFull(self):
        "Enables all actions over files"
        # Add to file
        self.popupmenu1.Enable(
            wxID_WXFRAME1POPUPMENU1ITEMS3, True)
        # Open
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS0, True)
        # Open with
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS1, True)
        # Extract selected files
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS2, True)
        # Extract all
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS3, True)
        # Create new folder
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS4, True)
        # Move/rename
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS5, True)
        # Delete selected files
        self.popupmenu2.Enable(
            wxID_WXFRAME1POPUPMENU2ITEMS6, True)
        # Recompression level
        self.menu1.Enable(
            wxID_WXFRAME1MENU1ITEMS3, True)
        # Search
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS0, True)
        # Copy
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS2, True)
        # Paste
        self.menu4.Enable(
            wxID_WXFRAME1MENU4ITEMS3, True)
        # Toolbar - add
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS2, True)
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS3, True)
        # Toolbar - extract
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS4, True)
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS5, True)
        # Toolbar - delete
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS6, True)
        # Toolbar - open
        self.toolBar1.EnableTool(
            wxID_WXFRAME1TOOLBAR1ITEMS7, True)
            
        # Enable drop events on the TreeListCtrl
        DragNDrop.READONLY = False
            
    def NewFolderLocal(self,event):
        "Creates a new folder in the file system"
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the name of the selected folder
        folder = self.multiSelectionDirCtrl1.GetPaths()
        # Check that only one has been selected 
        if len(folder)!=1:
            Utilities.Log(_(u'Select the base directory where you want ' \
            u'to create another.'),Utilities.ERRO)
            return
        # If not a folder, get it's parent
        if not os.path.isdir(folder[0]):
            folder[0] = os.path.dirname(folder[0])
        # Ask for the full path of the new folder
        dialog = wx.TextEntryDialog(self, 
            _(u'Input the path for the new folder:'),'', '')
        dialog.SetValue(folder[0] + '/' + _(u'new_folder'))
        if dialog.ShowModal() == wx.ID_OK:
            try:
                nomDirAux = dialog.GetValue()
                # If empty path don't continue
                if not nomDirAux:
                    return
                # Create the new folder
                Utilities.CreateFolder(nomDirAux)
                Utilities.Log(_(u'Local folder %s created.') % nomDirAux, 
                    Utilities.INFO)
                # Update the file system
                self.multiSelectionDirCtrl1.ReCreateTree()
                self.multiSelectionDirCtrl1.SetPath(dialog.GetValue())
            # If there is a problem show a message
            except Exception, e:
                Utilities.Log(_(u'Cannot create the new folder:') +
                ' ' + unicode(e), Utilities.ERRO)
        dialog.Destroy()
        
    def RenameLocal(self, event):
        "Renames a file or folder selected in the file system."
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected paths
        files = self.multiSelectionDirCtrl1.GetPaths()
        # If nothing selected show a message and end
        if len(files) != 1:
            Utilities.Log(_(u'Select the file or folder that you want to rename.'),
                Utilities.ERRO)
            return
        # Ask for the new filename
        dialog = wx.TextEntryDialog(self, 
            _(u'Input the new name:'),'', '')
        dialog.SetValue(files[0])
        if dialog.ShowModal() == wx.ID_OK:
            try:
                newName = dialog.GetValue()
                # Exit on empty name
                if not newName:
                    return
                # Avoid things like /../
                if newName != os.path.normpath(newName):
                    Utilities.Log(_(u'The name %s is not allowed.')%newName,
                        Utilities.ERRO)
                    return
                # Move the file/folder
                # Can't use os.rename because does not work between file systems
                shutil.move(files[0], newName)
                Utilities.Log(_(u'Local file %(source)s renamed to ' \
                    '%(destination)s.') % {'source':files[0],
                    'destination':newName}, Utilities.INFO)
                # Update the file system
                self.multiSelectionDirCtrl1.ReCreateTree()
                self.multiSelectionDirCtrl1.SetPath(newName)
            # If error show a message
            except Exception, e:
                Utilities.Log(_(u'Cannot move the file:') +
                ' ' + unicode(e), Utilities.ERRO)
        dialog.Destroy()
        
    def DeleteLocal(self, event):
        "Deletes the files or folders selected in the file system."
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected paths
        files = self.multiSelectionDirCtrl1.GetPaths()
        # If nothing selected show a message and end
        if len(files) < 1:
            Utilities.Log(_(u'Select the file of folder that you want to delete.'),
                Utilities.ERRO)
            return
        # Ask for confirmation before deleting
        filesStr = ''
        for file in files:
            filesStr += '\n' + file
        answer = Utilities.YesNoDialog(_(u'The folling files and ' \
            'folders will be deleted. Do you want to continue?\n') + filesStr)
        if (answer != wx.ID_YES):
            return
        # Delete the files one by one
        for file in files:
            try:
                Utilities.DeleteFile(file)
            except Exception, e:
                Utilities.Log(_(u'Cannot delete %s:') % file +
                    ' ' + unicode(e), Utilities.ERRO)
        Utilities.Log(_(u'%s local files or folders have been ' \
            'deleted.') % str(len(files)), Utilities.INFO)
        # Update the file system
        self.multiSelectionDirCtrl1.ReCreateTree()
        self.multiSelectionDirCtrl1.SetPath(os.path.dirname(file))
        
    def Exit(self,event):
        "Exit from Tarumba."
        # If null event we have called it
        if event:
            event.StopPropagation()
        self.Close()
        
    def Manual(self, event):
        "Shows the user manual."
        # No implemented yet
        Utilities.ErrorDialog(_(u'The user manual is not available yet.'),
            _(u'Sorry'))
        
    def About(self, event):
        "Show information about Tarumba."
        # If null event we have called it
        if event:
            event.StopPropagation()     
        info = wx.AboutDialogInfo()
        info.Name = u'Tarumba'
        info.Version = Globals.VERSION
        info.Copyright = u'2005-2011 Félix Medrano Sanz\n'
        info.Description = wordwrap(
            _(u'Tarumba is a graphic user interface to work with compressed ' \
            u'files.')+'\n\n'+_(u'Published under the GPL v3 License.'),
            350, wx.ClientDC(self))
        info.WebSite = (u'http://sourceforge.net/projects/tarumba/', 
            _(u'Tarumba\'s home page at sourceforge'))
        info.Developers = [ u'Félix Medrano Sanz ('+_(u'Author')+u')',
                            u'Maria L. Castro Brylka ('+_(u'English localization')+u')' ]
        wx.AboutBox(info)
        
    def ExternalOpenLocalDefault(self, event):
        "Opens a local file with the default external program"
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected paths
        files = self.multiSelectionDirCtrl1.GetPaths()
        # If not a file selected show a message and end
        if len(files) != 1:
            Utilities.Log(_(u'Select one file to be opened.'),
                Utilities.ERRO)
            return
        # If the item selected is a folder, expand it
        if not os.path.isfile(files[0]):
            self.multiSelectionDirCtrl1.ExpandFolder(event)
            return
        try:
            # Get the mimetype for the file
            manager = wx.TheMimeTypesManager
            mime, codif = mimetypes.guess_type(files[0])
            # If the type is unknown warn the user
            if not mime:
                raise Exception()
            type = manager.GetFileTypeFromMimeType(mime)
            command = type.GetOpenCommand("'"+files[0].replace("'","'\"'\"'")+"'")
            # If no default program for this file type warn the user
            if not command:
                raise Exception()
            # Open the file with the default program
            Utilities.ExecuteExternal(command)
        except Exception, e:
            Utilities.Log(_(u'Could not get the default program for this ' \
                'file type. You must input the program to open the file.'),
                Utilities.WARN)
            self.ExternalOpenLocalWith(None)
    
    def ExternalOpenLocalWith(self, event):
        "Opens a local file with a selected external program"
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected paths
        files = self.multiSelectionDirCtrl1.GetPaths()
        # If not a file selected show a message and end
        if len(files) != 1:
            Utilities.Log(_(u'Select one file to be opened.'),
                Utilities.ERRO)
            return
        # Be sure that the item is a file
        if not os.path.isfile(files[0]):
            Utilities.Log(_(u'Select one file to be opened.'),
                Utilities.ERRO)
            return
        # Ask for the external program to use
        dialog = wx.TextEntryDialog(
            self, _(u'Input the program to open the file'), ' ', '')
        # Show the last program used
        if (Globals.lastExternal and (Globals.lastExternal != 'None')):
            dialog.SetValue(Globals.lastExternal)
        # If program requested, use it to open the file
        if dialog.ShowModal() == wx.ID_OK:
            command = dialog.GetValue()
            if len(command) > 0:
                # Check if the command can be executed
                if not Utilities.IsInstalled(command):
                    Utilities.Log(
                        _(u'"%s" cannot be found in your system.') % command, 
                        Utilities.ERRO)
                    # Destroy the dialog and exit
                    dialog.Destroy()
                    return
                Globals.lastExternal = command
                ConfigurationManager.saveValue('LAST_EXTERNAL',command)
                command += ' ' + "'"+files[0].replace("'","'\"'\"'")+"'"
                Utilities.ExecuteExternal(command)
        # Destroy the dialog
        dialog.Destroy()
    
    def ExternalOpenCompressedDefault(self, event):
        "Opens a compressed file with the default external program"
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected paths
        selection = self.treeListCtrl1.GetSelections()
        # If not a file selected show a message and end
        if len(selection) != 1:
            Utilities.Log(_(u'Select one file to be opened.'),
                Utilities.ERRO)
            return
        files = [self.treeListCtrl1.GetPyData(selection[0])]
        # If the item selected is a folder, expand it
        if (not files[0][0]) or files[0][0][-1] == '/':
            self.treeListCtrl1.ExpandFolder(event)
            return
        try:
            # Get the mimetype for the file
            manager = wx.TheMimeTypesManager
            mime, codif = mimetypes.guess_type(files[0][0])
            # If the type is unknown warn the user
            if not mime:
                raise Exception()
            type = manager.GetFileTypeFromMimeType(mime)
            command = type.GetOpenCommand("'"+files[0][0].replace("'","'\"'\"'")+"'")
            # If no default program for this file type warn the user
            if not command:
                raise Exception()
            # Get a temporary folder
            tmpFolder = Temporary.tmpDir()
            # Caltulate the name of the created file
            tmpFile = os.path.join(tmpFolder,Utilities.BasenameMod(files[0][0]))
            # Make the file read-only
            os.chmod(tmpFile,stat.S_IRUSR)
            # Get the open command for the temporary file
            command = type.GetOpenCommand("'"+tmpFile.replace("'","'\"'\"'")+"'")
            # Extract the file via the manager
            error, output = CompressionManager.extract(Globals.file, 
                self.treeListCtrl1, tmpFolder)        
            # Stop and inform in case of error
            if error:
                Utilities.Log(output,Utilities.ERRO)
                return
            # Open the file with the default program
            Utilities.ExecuteExternal(command)
        except Exception, e:
            Utilities.Log(_(u'Could not get the default program for this ' \
                'file type. You must input the program to open the file.'),
                Utilities.WARN)
            self.ExternalOpenCompressedWith(None)
    
    def ExternalOpenCompressedWith(self,event):
        "Opens a compressed file with a selected external program"
        # If null event we have called it
        if event:
            event.StopPropagation()
        # Get the selected paths
        selection = self.treeListCtrl1.GetSelections()
        # If not a file selected show a message and end
        if len(selection) != 1:
            Utilities.Log(_(u'Select one file to be opened.'),
                Utilities.ERRO)
            return
        files = [self.treeListCtrl1.GetPyData(selection[0])]
        # Be sure that the item is a file
        if (not files[0][0]) or files[0][0][-1] == '/':
            Utilities.Log(_(u'Select one file to be opened.'),
                Utilities.ERRO)
            return
        # Ask for the external program to use
        dialog = wx.TextEntryDialog(self, _(u'Select one file to be opened.'), ' ', '')
        # Show the last program used
        if (Globals.lastExternal and (Globals.lastExternal != 'None')):
            dialog.SetValue(Globals.lastExternal)
        # If program requested, use it to open the file
        if dialog.ShowModal() == wx.ID_OK:
            command = dialog.GetValue()
            if len(command) > 0:
                # Check if the command can be executed
                if not Utilities.IsInstalled(command):
                    Utilities.Log(
                        _(u'"%s" cannot be found in your system.') % command, 
                        Utilities.ERRO)
                    # Destroy the dialog and exit
                    dialog.Destroy()
                    return
                Globals.lastExternal = command
                ConfigurationManager.saveValue('LAST_EXTERNAL',command)
                # Get a temporary folder
                tmpFolder = Temporary.tmpDir()
                # Extract the file via the manager
                error, output = CompressionManager.extract(Globals.file, 
                    self.treeListCtrl1, tmpFolder)
                # Stop and inform in case of error
                if error:
                    Utilities.Log(output,Utilities.ERRO)
                    return
                # Caltulate the name of the created file
                tmpFile = os.path.join(tmpFolder,Utilities.BasenameMod(files[0][0]))  
                # Make the file read-only
                os.chmod(tmpFile,stat.S_IRUSR) 
                command += ' ' + "'"+tmpFile.replace("'","'\"'\"'")+"'"
                Utilities.ExecuteExternal(command)
        # Destroy the dialog
        dialog.Destroy()
        

