#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         SplitDialog.py
# Purpose:      Dialog used to split a file into smaller volumes.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: SplitDialog.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import Executor

import wx
from wx.lib.masked import NumCtrl
import os

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BUTTON1, wxID_DIALOG1PANEL1, wxID_DIALOG1PANEL2, 
 wxID_DIALOG1PANEL3, wxID_DIALOG1PANEL4, wxID_DIALOG1STATICTEXT1,
 wxID_DIALOG1STATICTEXT4, wxID_DIALOG1TEXTCTRL1,
 wxID_DIALOG1BUTTON2, wxID_DIALOG1TEXTCTRL2, wxID_DIALOG1TEXTCTRL3, 
 wxID_DIALOG1STATICTEXT5, wxID_DIALOG1RADIO1, wxID_DIALOG1RADIO2, 
 wxID_DIALOG1CHOICE2, wxID_DIALOG1TEXTCTRL4
] = [wx.NewId() for _init_ctrls in range(17)]

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
        parent.AddSizer(self.boxSizer6, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer7, 1, border=0, flag=wx.EXPAND)
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
        
    def _init_coll_boxSizer6_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.radio1, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.textCtrl3, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.staticText5, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        
    def _init_coll_boxSizer7_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.radio2, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.textCtrl4, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.choice2, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer3 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        self.boxSizer5 = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        self.boxSizer6 = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        self.boxSizer7 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.gridSizer1 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self.gridSizer2 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)
        
        self.gridSizer3 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)
        
        self.gridSizer4 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_boxSizer4_Items(self.boxSizer4)
        self._init_coll_boxSizer5_Items(self.boxSizer5)
        self._init_coll_boxSizer6_Items(self.boxSizer6)
        self._init_coll_boxSizer7_Items(self.boxSizer7)
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
              style=wx.DEFAULT_DIALOG_STYLE, title=_(u'Split file'))

        self.panel1 = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel1',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_DIALOG1PANEL2, name='panel2',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel3 = wx.Panel(id=wxID_DIALOG1PANEL3, name='panel3',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel4 = wx.Panel(id=wxID_DIALOG1PANEL4, name='panel4',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=_(u'Original file'), name='staticText1', 
              parent=self.panel3, style=wx.ALIGN_RIGHT)
              
        self.staticText4 = wx.StaticText(id=wxID_DIALOG1STATICTEXT4,
              label=_(u'Destination folder'), name='staticText4', 
              parent=self.panel4, style=wx.ALIGN_RIGHT)
              
        self.staticText5 = wx.StaticText(id=wxID_DIALOG1STATICTEXT5,
              label='', name='staticText5', parent=self,
              style=wx.ALIGN_RIGHT)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value='')
              
        self.textCtrl2 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL2, name='textCtrl2',
              parent=self, style=0, value='')
              
        self.textCtrl3 = NumCtrl(id=wxID_DIALOG1TEXTCTRL3, name='textCtrl3',
              parent=self, style=0, allowNone=True, value=None, groupDigits=False)
              
        self.textCtrl4 = NumCtrl(id=wxID_DIALOG1TEXTCTRL4, name='textCtrl4',
              parent=self, style=0, allowNone=True, value=None, groupDigits=False)

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=_(u'&Examine'),
              name='button1', parent=self, style=0)
              
        self.button2 = wx.Button(id=wxID_DIALOG1BUTTON2, label=_(u'&Examine'),
              name='button2', parent=self, style=0)

        self.buttonOk = wx.Button(id=wx.ID_OK, parent=self.panel1, style=0)

        self.buttonCancel = wx.Button(id=wx.ID_CANCEL, parent=self.panel2, 
              style=0)
              
        self.choice2 = wx.Choice(choices=[], id=wxID_DIALOG1CHOICE2,
              name='choice2', parent=self, style=0)
              
        self.radio1 = wx.RadioButton(parent=self, id=wxID_DIALOG1RADIO1, 
              label=_(u'Option A: Input the number of volumes.'), style=wx.RB_GROUP )
        
        self.radio2 = wx.RadioButton(parent=self, id=wxID_DIALOG1RADIO2, 
              label=_(u'Option B: Input the size of the volumes.'))

        self._init_sizers()

    def __init__(self, parent):
        
        # Call the auto-generated BOA functions
        self._init_ctrls(parent)  
        
        # Add the KB/MB check
        self.choice2.Append(
            'KB',
            1024)
        self.choice2.Append(
            'MB',
            1024*1024)
        self.choice2.Append(
            'GB',
            1024*1024*1024)
        self.choice2.Select(0)
        
        # Emulate the click over the radio1
        self.OnRadio1Radio(None)
        
        # Events
        wx.EVT_BUTTON(self.button1, wxID_DIALOG1BUTTON1, self.OnButton1Button)
        wx.EVT_BUTTON(self.button2, wxID_DIALOG1BUTTON2, self.OnButton2Button)
        wx.EVT_BUTTON(self.buttonOk, wx.ID_OK, self.OnOK)
        wx.EVT_RADIOBUTTON(self.radio1, wxID_DIALOG1RADIO1, self.OnRadio1Radio)
        wx.EVT_RADIOBUTTON(self.radio2, wxID_DIALOG1RADIO2, self.OnRadio2Radio)
        self.textCtrl1.Bind(wx.EVT_KILL_FOCUS, self.OnText1Input)
        
        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 40
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
            sample = os.path.dirname(text1)
            self.textCtrl2.SetValue(sample)
            # Select the base name of the auto-generated path
            self.textCtrl2.SetSelection(sample.rfind('/')+1, -1)
        
    def OnButton1Button(self, event):
        "Show the file manager dialog"
        # If null event we have called it
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
        "Show the file manager dialog"
        # If null event we have called it
        if event:
            event.StopPropagation()
        dialog = wx.DirDialog(self, style=0,
            defaultPath = Globals.lastUsedPath)
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl2.SetValue(dialog.GetPath())
            # Remember the last used path
            Globals.lastUsedPath = dialog.GetPath()
        dialog.Destroy()
        
    def OnRadio1Radio(self, event):
        "Enables the number of volumes and disables the size"
        # If null event we have called it
        if event:
            event.StopPropagation()
        self.textCtrl3.Enable(True)
        self.textCtrl4.Enable(False)
        self.choice2.Enable(False)

    def OnRadio2Radio(self, event):
        "Enables the size and disables the number of volumes"
        # If null event we have called it
        if event:
            event.StopPropagation()
        self.textCtrl3.Enable(False)
        self.textCtrl4.Enable(True)
        self.choice2.Enable(True)
        
    def OnOK( self, event ):
        "Process the Ok button event"
        nomAux = self.textCtrl1.GetValue()
        baseNameAux = Utilities.BasenameMod(nomAux)
        folderAux = self.textCtrl2.GetValue()
        # If empty name we can't continue
        if not nomAux:
            Utilities.ErrorDialog(
            _(u'Input the path of the file that you want to split.'), 
            _(u'Missing parameters'))
            return False
        # Get the size of the file
        try:
            sizeOri = os.path.getsize(nomAux)
        except os.error:
            Utilities.ErrorDialog(
            _(u'The file %s does not exist or cannot be accessed.')%nomAux)
            return False
        # If empty folder we can't continue
        if not folderAux:
            Utilities.ErrorDialog(
            _(u'Input the path of the destination folder.'), 
            _(u'Missing parameters'))
            return False
        # If we are splitting by the number of volumes
        if (self.textCtrl3.IsEnabled()):
            numVolumesAux = self.textCtrl3.GetValue()
            if not numVolumesAux:
                Utilities.ErrorDialog(
                _(u'Input the number of volumes where to split the file.'), 
                _(u'Missing parameters'))
                return False
            # Calculate the required size for the volumes
            numVolumes = numVolumesAux
            size, aux = divmod(sizeOri, numVolumes)
            if aux > 0:
                size += 1
        # If we are splitting by size
        else:
            multiple = self.choice2.GetClientData(self.choice2.GetSelection())
            sizeAux = self.textCtrl4.GetValue() * int(multiple)
            if not sizeAux:
                Utilities.ErrorDialog(
                _(u'Input the size for the volumes that you want to create.'), 
                _(u'Missing parameters'))
                return False
            # Calculate the required number of volumes
            size = sizeAux
            numVolumes, aux = divmod(sizeOri, size)
            if aux > 0:
                numVolumes += 1
        # Calculate the name for the files to generate
        lenSuffix = len(str(numVolumes))
        preffix = os.path.join(folderAux, baseNameAux) + '.'
        i = 0
        while i < numVolumes:
            j = str(i)
            while len(j) < lenSuffix:
                j = '0' + j
            destinationName = preffix + j
            # If the new file exists, ask to overwrite
            if os.path.lexists(destinationName):
                answer = Utilities.YesNoDialog(_(u'The file %s already exists\nDo you want to overwrite ' \
                    u'all the existing files?') % destinationName)
                if (answer != wx.ID_YES):
                    return False
                else:
                    i = numVolumes
            i += 1
        # Hide the dialog
        self.EndModal(wx.ID_OK)
        # Split the file
        size = str(size)
        lenSuffix = str(lenSuffix)
        command = [(Globals.SPLIT_BIN, ['--verbose','-d','-b',size,'-a',
            lenSuffix,nomAux,preffix], _(u'Splitting %s') % baseNameAux)]
        try:
            # Change the cursor to busy cursor 
            self.busy = wx.BusyCursor()
            error, output = Executor.execute(command, _(u'Splitting file'), unknownProgress=True)
        finally :
            # Set the normal cursor again
            if self.busy:
                del self.busy
        if error:
            Utilities.Log(_(u'Error when splitting the file %s') % nomAux +'' \
                ': ' + '\n'.join(output), Utilities.ERRO)
        else:
            Utilities.Log(_(u'The file %s has been splitted into %i ' \
                u'volumes.') % (nomAux,numVolumes), Utilities.INFO)

