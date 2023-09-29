#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         JoinDialog.py
# Purpose:      Can re-join chunks previously splitted.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: JoinDialog.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import Executor

import wx
import os

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BUTTON1, wxID_DIALOG1PANEL1, wxID_DIALOG1PANEL2, 
 wxID_DIALOG1PANEL3 ,wxID_DIALOG1PANEL4, wxID_DIALOG1STATICTEXT1,
 wxID_DIALOG1STATICTEXT4, wxID_DIALOG1TEXTCTRL1,
 wxID_DIALOG1BUTTON2, wxID_DIALOG1TEXTCTRL2
] = [wx.NewId() for _init_ctrls in range(11)]

class Dialog1(wx.Dialog):
    def _init_coll_gridSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.buttonCancel, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.LEFT)

    def _init_coll_boxSizer4_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel1, 1, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.panel2, 1, border=0, flag=wx.EXPAND)

    def _init_coll_gridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.buttonOk, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)
              
    def _init_coll_gridSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText1, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)
              
    def _init_coll_gridSizer4_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText4, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddSizer(self.boxSizer2, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer5, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer4, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.panel3, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.textCtrl1, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.button1, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        
    def _init_coll_boxSizer5_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.panel4, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.textCtrl2, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.button2, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer3 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        self.boxSizer5 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.gridSizer1 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self.gridSizer2 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)
        
        self.gridSizer3 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)
        
        self.gridSizer4 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_boxSizer4_Items(self.boxSizer4)
        self._init_coll_boxSizer5_Items(self.boxSizer5)
        self._init_coll_gridSizer1_Items(self.gridSizer1)
        self._init_coll_gridSizer2_Items(self.gridSizer2)
        self._init_coll_gridSizer3_Items(self.gridSizer3)
        self._init_coll_gridSizer4_Items(self.gridSizer4)

        self.SetSizer(self.boxSizer1)
        self.panel1.SetSizer(self.gridSizer1)
        self.panel2.SetSizer(self.gridSizer2)
        self.panel3.SetSizer(self.gridSizer3)
        self.panel4.SetSizer(self.gridSizer4)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              style=wx.DEFAULT_DIALOG_STYLE, title=_(u'Join Volumes'))

        self.panel1 = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel1',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_DIALOG1PANEL2, name='panel2',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel3 = wx.Panel(id=wxID_DIALOG1PANEL3, name='panel3',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel4 = wx.Panel(id=wxID_DIALOG1PANEL4, name='panel4',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=_(u'Select a volume'), name='staticText1', 
              parent=self.panel3, style=wx.ALIGN_RIGHT)
              
        self.staticText4 = wx.StaticText(id=wxID_DIALOG1STATICTEXT4,
              label=_(u'File to generate'), name='staticText4', 
              parent=self.panel4, style=wx.ALIGN_RIGHT)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value='')
              
        self.textCtrl2 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL2, name='textCtrl2',
              parent=self, style=0, value='')

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=_(u'&Examine'),
              name='button1', parent=self, style=0)
              
        self.button2 = wx.Button(id=wxID_DIALOG1BUTTON2, label=_(u'&Examine'),
              name='button2', parent=self, style=0)

        self.buttonOk = wx.Button(id=wx.ID_OK, parent=self.panel1, style=0)

        self.buttonCancel = wx.Button(id=wx.ID_CANCEL, parent=self.panel2, 
              style=0)

        self._init_sizers()

    def __init__(self, parent):
        
        # Call BOA's init functions
        self._init_ctrls(parent)  
        
        # Events
        wx.EVT_BUTTON(self.button1, wxID_DIALOG1BUTTON1, self.OnButton1Button)
        wx.EVT_BUTTON(self.button2, wxID_DIALOG1BUTTON2, self.OnButton2Button)
        wx.EVT_BUTTON(self.buttonOk, wx.ID_OK, self.OnOK)
        self.textCtrl1.Bind(wx.EVT_KILL_FOCUS, self.OnText1Input)
        
        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))
        
    def OnText1Input(self, event):
        "Shows the file manager dialog"
        # If null event, we have called it
        if event:
            event.StopPropagation()
        # Get the text in both controls
        text1 = self.textCtrl1.GetValue()
        text2 = self.textCtrl2.GetValue()
        # If valid filename in the first and no value in the second, auto-generate a valid sample
        if text1 and os.path.isfile(text1) and (not text2):
            if Utilities.IsGenericMultivolume(text1):
                sample = Utilities.WithoutExtension(text1)
                self.textCtrl2.SetValue(sample)
                # Select the base name of the auto-generated path
                self.textCtrl2.SetSelection(sample.rfind('/')+1, -1)
        
    def OnButton1Button(self, event):
        "Shows the file manager dialog"
        # If null event, we have called it
        if event:
            event.StopPropagation()
        dialog = wx.FileDialog(self, style=wx.OPEN,
            defaultDir = Globals.lastUsedPath)
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl1.SetValue(dialog.GetPath())
            # Force the text focus event
            self.OnText1Input(None)
            # Remember the last used path
            Globals.lastUsedPath = os.path.dirname(dialog.GetPath())
        dialog.Destroy()
        
    def OnButton2Button(self, event):
        "Shows the file manager dialog"
        # If null event, we have called it
        if event:
            event.StopPropagation()
        dialog = wx.FileDialog(self, style=wx.SAVE,
            defaultDir = Globals.lastUsedPath)
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl2.SetValue(dialog.GetPath())
            # Remember the last used path
            Globals.lastUsedPath = os.path.dirname(dialog.GetPath())
        dialog.Destroy()
        
    def OnOK( self, event ):
        "Process the event over the OK button"
        volAux = self.textCtrl1.GetValue()
        nomAux = self.textCtrl2.GetValue()
        # If empty volume we can't continue
        if not volAux:
            Utilities.ErrorDialog(
            _(u'Input the path for one of the volumes that you want to join.'), 
            _(u'Missing parameters'))
            return False
        # Check the volume filename extension
        if not Utilities.IsGenericMultivolume(volAux):
            Utilities.ErrorDialog(
            _(u'The filename of the volume is not valid.') + '\n' \
            ''+_(u'A numeric suffix of any lenght is expected: .4, .00, .298, etc.'),
            _(u'Unknown extension'))
            return False
        # Check if the volume exists
        if not os.path.isfile(volAux):
            Utilities.ErrorDialog( 
            _(u'The volume %s does not exist or is inaccessible.') % volAux)
            return False
        # If empty name we can't continue
        if not nomAux:
            Utilities.ErrorDialog(
            _(u'Insert the name of the file that you want to generate.'), 
            _(u'Missing parameters'))
            return False
        # If the new file already exists, ask to overwrite
        if os.path.lexists(nomAux):
            answer = Utilities.YesNoDialog(_(u'The file %s ' \
                u'already exists. Overwrite it?') % nomAux)
            if (answer != wx.ID_YES):
                return False     
        # Search for available volumes
        volumes = Utilities.GetGenericVolumes(volAux)
        numVol = len(volumes)
        # If there is only one, don't continue
        if (numVol <= 1):
            Utilities.ErrorDialog(
            _(u'The other volumes could not be found.\nVerify that all of them are in the same folder.'))
            return False
        # Ask to the user before performing the join
        answer = Utilities.YesNoDialog(_(u'A total of %i volumes have been detected.\nIs this correct?') % numVol)
        if (answer != wx.ID_YES):
            return False
        # Hide the dialog
        self.EndModal(wx.ID_OK)
        # Join the volumes
        command = [('StdoutToFile.py', [nomAux,Globals.CAT_BIN] + volumes, 
            _(u'Generating %s') % Utilities.BasenameMod(nomAux))]
        try:
            # Change the cursor to BusyCursor  
            self.busy = wx.BusyCursor()
            error, output = Executor.execute(command, _(u'Joining volumes'), unknownProgress=True)
        finally :
            # Stop the BusyCursor
            if self.busy:
                del self.busy
        if error:
            Utilities.Log(_(u'Error when joining the volumes') + ': ' \
                '\n'.join(output), Utilities.ERRO)
        else:
            Utilities.Log(_(u'The file %s has been created.') % nomAux,Utilities.INFO)

