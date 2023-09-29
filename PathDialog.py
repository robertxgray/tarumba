#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         PathDialog.py
# Purpose:      Dialog used to configure file paths.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: PathDialog.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import ConfigurationManager
import CompressionManager
import MainFrameMenu
import Temporary

import wx
import wx.lib.filebrowsebutton
import wx.lib.scrolledpanel
import os

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1DIRBROWSEBUTTON1, wxID_DIALOG1FILEBROWSEBUTTON1, 
 wxID_DIALOG1FILEBROWSEBUTTON2, wxID_DIALOG1FILEBROWSEBUTTON3, 
 wxID_DIALOG1FILEBROWSEBUTTON4, wxID_DIALOG1FILEBROWSEBUTTON5,
 wxID_DIALOG1FILEBROWSEBUTTON6, wxID_DIALOG1FILEBROWSEBUTTON7,
 wxID_DIALOG1FILEBROWSEBUTTON8, wxID_DIALOG1FILEBROWSEBUTTON9,
 wxID_DIALOG1FILEBROWSEBUTTON10, wxID_DIALOG1FILEBROWSEBUTTON11,
 wxID_DIALOG1PANEL1, wxID_DIALOG1PANEL2, wxID_DIALOG1PANEL3,
 wxID_DIALOG1SCROLLEDPANEL1, wxID_DIALOG1STATICTEXT1
] = [wx.NewId() for _init_ctrls in range(18)]

class Dialog1(wx.Dialog):

    def _init_coll_gridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button1, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)

    def _init_coll_gridSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button2, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.LEFT)

    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.dirBrowseButton1, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton1, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton2, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton11, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton3, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton4, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton5, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton6, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton7, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton8, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton9, 0, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.fileBrowseButton10, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.panel3, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.scrolledPanel1, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddSizer(self.boxSizer2, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel1, 1, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.panel2, 1, border=0, flag=wx.EXPAND)
        
    def _init_coll_boxSizer4_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.staticText1, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.gridSizer1 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self.gridSizer2 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self.boxSizer3 = wx.BoxSizer(orient=wx.VERTICAL)
        
        self.boxSizer4 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_gridSizer1_Items(self.gridSizer1)
        self._init_coll_gridSizer2_Items(self.gridSizer2)
        self._init_coll_boxSizer3_Items(self.boxSizer3)
        self._init_coll_boxSizer4_Items(self.boxSizer4)

        self.SetSizer(self.boxSizer1)
        self.panel1.SetSizer(self.gridSizer1)
        self.panel2.SetSizer(self.gridSizer2)
        self.panel3.SetSizer(self.boxSizer4)
        self.scrolledPanel1.SetSizer(self.boxSizer3)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              size=wx.Size(600, 400), 
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
              title=_(u'Edit Paths'))

        self.scrolledPanel1 = wx.lib.scrolledpanel.ScrolledPanel(
              id=wxID_DIALOG1SCROLLEDPANEL1,
              name='scrolledPanel1', parent=self, style=0)

        self.panel1 = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel1',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_DIALOG1PANEL2, name='panel2',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel3 = wx.Panel(id=wxID_DIALOG1PANEL3, name='panel3',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=_(u'If the full path for the binary files is not set, ' \
                u'they must be available via the PATH.'), name='staticText1',
              parent=self.panel3, style=0)

        self.button1 = wx.Button(id=wx.ID_OK, parent=self.panel1, style=0)

        self.button2 = wx.Button(id=wx.ID_CANCEL, parent=self.panel2, style=0)

        self.dirBrowseButton1 = wx.lib.filebrowsebutton.DirBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a folder'), 
              id=wxID_DIALOG1DIRBROWSEBUTTON1,
              labelText=_(u'Temporary folder'), newDirectory=True,
              parent=self.scrolledPanel1, startDirectory='.', 
              style=wx.TAB_TRAVERSAL, toolTip='')
        self.dirBrowseButton1.SetValue(Globals.TMPDIR)

        self.fileBrowseButton1 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON1, initialValue=Globals.CAT_BIN,
              labelText=_(u'Cat binary'), parent=self.scrolledPanel1, 
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')

        self.fileBrowseButton2 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON2, initialValue=Globals.SPLIT_BIN,
              labelText=_(u'Split binary'), parent=self.scrolledPanel1, 
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')

        self.fileBrowseButton3 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON3, initialValue=Globals.OPENSSL_BIN,
              labelText=_(u'OpenSSL binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')

        self.fileBrowseButton4 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON4, initialValue=Globals.TAR_BIN,
              labelText=_(u'Tar binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')

        self.fileBrowseButton5 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON5, initialValue=Globals.GZIP_BIN,
              labelText=_(u'Gzip binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')
              
        self.fileBrowseButton6 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON6, initialValue=Globals.RAR_BIN,
              labelText=_(u'Rar binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')
              
        self.fileBrowseButton7 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON7, initialValue=Globals.ZIP_BIN,
              labelText=_(u'Zip binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')
              
        self.fileBrowseButton8 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON8, initialValue=Globals.ZIPNOTE_BIN,
              labelText=_(u'Zipnote binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')
              
        self.fileBrowseButton9 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON9, initialValue=Globals.UNZIP_BIN,
              labelText=_(u'Unzip binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')
              
        self.fileBrowseButton10 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON10, initialValue=Globals.ZIPINFO_BIN,
              labelText=_(u'Zipinfo binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')
              
        self.fileBrowseButton11 = wx.lib.filebrowsebutton.FileBrowseButton(
              buttonText=_(u'Browse'),
              dialogTitle=_(u'Choose a file'), fileMask='*.*',
              id=wxID_DIALOG1FILEBROWSEBUTTON11, initialValue=Globals.GREP_BIN,
              labelText=_(u'Grep binary'), parent=self.scrolledPanel1,
              startDirectory='.', style=wx.TAB_TRAVERSAL, toolTip='')

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Enable the scroll bar
        self.scrolledPanel1.SetupScrolling()
        
        # Events
        wx.EVT_BUTTON(self.button1, wx.ID_OK, self.OnOK)
        
    def OnOK( self, event ):
        "Process the event over the OK button"
        
        # The program cannot start if the temporary file is unusable
        # so we will check it before aplying changes
        if not os.access(self.dirBrowseButton1.GetValue(),os.W_OK):
            Utilities.ErrorDialog(_(u'The selected temporary folder is not writable, please select another one.'))
            return
        
        # Cat must be available
        if not Utilities.IsInstalled(self.fileBrowseButton1.GetValue()):
            Utilities.ErrorDialog(_(u'The path you selected for the cat binary is not valid, please correct it.'))
            return
        
        # Split must be available
        if not Utilities.IsInstalled(self.fileBrowseButton2.GetValue()):
            Utilities.ErrorDialog(_(u'The path you selected for the split binary is not valid, please correct it.'))
            return
        
        # Grep must be available
        if not Utilities.IsInstalled(self.fileBrowseButton11.GetValue()):
            Utilities.ErrorDialog(_(u'The path you selected for the grep binary is not valid, please correct it.'))
            return
        
        # Temporary folder
        # Allow the use of ~ as the home folder
        Globals.TMPDIR = os.path.expanduser(self.dirBrowseButton1.GetValue())
        ConfigurationManager.saveValue('TMPDIR',Globals.TMPDIR)
        
        # CAT
        Globals.CAT_BIN = self.fileBrowseButton1.GetValue()
        ConfigurationManager.saveValue('CAT_BIN',Globals.CAT_BIN)
        
        # SPLIT
        Globals.SPLIT_BIN = self.fileBrowseButton2.GetValue()
        ConfigurationManager.saveValue('SPLIT_BIN',Globals.SPLIT_BIN)
        
        # OPENSSL
        Globals.OPENSSL_BIN = self.fileBrowseButton3.GetValue()
        ConfigurationManager.saveValue('OPENSSL_BIN',Globals.OPENSSL_BIN)
        
        # TAR
        Globals.TAR_BIN = self.fileBrowseButton4.GetValue()
        ConfigurationManager.saveValue('TAR_BIN',Globals.TAR_BIN)
        
        # GZIP
        Globals.GZIP_BIN = self.fileBrowseButton5.GetValue()
        ConfigurationManager.saveValue('GZIP_BIN',Globals.GZIP_BIN)
        
        # RAR
        Globals.RAR_BIN = self.fileBrowseButton6.GetValue()
        ConfigurationManager.saveValue('RAR_BIN',Globals.RAR_BIN)
        
        # ZIP
        Globals.ZIP_BIN = self.fileBrowseButton7.GetValue()
        ConfigurationManager.saveValue('ZIP_BIN',Globals.ZIP_BIN)
        
        # ZIPNOTE
        Globals.ZIPNOTE_BIN = self.fileBrowseButton8.GetValue()
        ConfigurationManager.saveValue('ZIPNOTE_BIN',Globals.ZIPNOTE_BIN)
        
        # UNZIP
        Globals.UNZIP_BIN = self.fileBrowseButton9.GetValue()
        ConfigurationManager.saveValue('UNZIP_BIN',Globals.UNZIP_BIN)
        
        # ZIPINFO
        Globals.ZIPINFO_BIN = self.fileBrowseButton10.GetValue()
        ConfigurationManager.saveValue('ZIPINFO_BIN',Globals.ZIPINFO_BIN)
        
        # GREP
        Globals.GREP_BIN = self.fileBrowseButton11.GetValue()
        ConfigurationManager.saveValue('GREP_BIN',Globals.GREP_BIN)
        
        # Re-check for available programs
        CompressionManager.checkAvailableCompressors()
        MainFrameMenu.DisableUnavailableOptions()
        
        # Relocate the temporary folder
        Temporary.deleteTmp()
        Temporary.createTmp()
        
        # Hide the dialog
        self.EndModal(wx.ID_OK)

