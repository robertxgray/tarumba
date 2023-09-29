#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         EncryptDialog.py
# Purpose:      Dialog used to encrypt files.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: EncryptDialog.py $
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
 wxID_DIALOG1PANEL3, wxID_DIALOG1PANEL4, wxID_DIALOG1PANEL5, 
 wxID_DIALOG1PANEL6, wxID_DIALOG1PANEL7, 
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, wxID_DIALOG1STATICTEXT3,
 wxID_DIALOG1STATICTEXT4, wxID_DIALOG1TEXTCTRL1, wxID_DIALOG1CHOICE1,
 wxID_DIALOG1BUTTON2, wxID_DIALOG1TEXTCTRL2, wxID_DIALOG1TEXTCTRL3,
 wxID_DIALOG1TEXTCTRL4, wxID_DIALOG1STATICTEXT5, wxID_DIALOG1STATICTEXT6,
 wxID_DIALOG1STATICTEXT7, wxID_DIALOG1STATICTEXT8
] = [wx.NewId() for _init_ctrls in range(23)]

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

        parent.AddWindow(self.staticText2, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)
              
    def _init_coll_gridSizer5_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText4, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)
              
    def _init_coll_gridSizer6_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText5, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)
              
    def _init_coll_gridSizer7_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText7, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)

    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel4, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.choice1, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.staticText3, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddSizer(self.boxSizer2, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer5, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer6, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer7, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer3, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer4, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

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

        parent.AddWindow(self.panel5, 1, border=0,
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

        parent.AddWindow(self.panel6, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.textCtrl3, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.staticText6, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        
    def _init_coll_boxSizer7_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel7, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.textCtrl4, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.staticText8, 1, border=0,
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
        
        self.gridSizer5 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)
        
        self.gridSizer6 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)
        
        self.gridSizer7 = wx.GridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_boxSizer3_Items(self.boxSizer3)
        self._init_coll_boxSizer4_Items(self.boxSizer4)
        self._init_coll_boxSizer5_Items(self.boxSizer5)
        self._init_coll_boxSizer6_Items(self.boxSizer6)
        self._init_coll_boxSizer7_Items(self.boxSizer7)
        self._init_coll_gridSizer1_Items(self.gridSizer1)
        self._init_coll_gridSizer2_Items(self.gridSizer2)
        self._init_coll_gridSizer3_Items(self.gridSizer3)
        self._init_coll_gridSizer4_Items(self.gridSizer4)
        self._init_coll_gridSizer5_Items(self.gridSizer5)
        self._init_coll_gridSizer6_Items(self.gridSizer6)
        self._init_coll_gridSizer7_Items(self.gridSizer7)

        self.SetSizer(self.boxSizer1)
        self.panel1.SetSizer(self.gridSizer1)
        self.panel2.SetSizer(self.gridSizer2)
        self.panel3.SetSizer(self.gridSizer3)
        self.panel4.SetSizer(self.gridSizer4)
        self.panel5.SetSizer(self.gridSizer5)
        self.panel6.SetSizer(self.gridSizer6)
        self.panel7.SetSizer(self.gridSizer7)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              style=wx.DEFAULT_DIALOG_STYLE, title=_(u'Encrypt file'))

        self.panel1 = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel1',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_DIALOG1PANEL2, name='panel2',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel3 = wx.Panel(id=wxID_DIALOG1PANEL3, name='panel3',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel4 = wx.Panel(id=wxID_DIALOG1PANEL4, name='panel4',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel5 = wx.Panel(id=wxID_DIALOG1PANEL5, name='panel5',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel6 = wx.Panel(id=wxID_DIALOG1PANEL6, name='panel6',
              parent=self, style=wx.TAB_TRAVERSAL)
              
        self.panel7 = wx.Panel(id=wxID_DIALOG1PANEL7, name='panel7',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=_(u'Original file'), name='staticText1', parent=self.panel3,
              style=wx.ALIGN_RIGHT)

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=_(u'Algorithm'), name='staticText2', parent=self.panel4,
              style=wx.ALIGN_RIGHT)
              
        self.staticText3 = wx.StaticText(id=wxID_DIALOG1STATICTEXT3,
              label='', name='staticText3', parent=self,
              style=wx.ALIGN_RIGHT)
              
        self.staticText4 = wx.StaticText(id=wxID_DIALOG1STATICTEXT4,
              label=_(u'Encrypted file'), name='staticText4', parent=self.panel5,
              style=wx.ALIGN_RIGHT)
              
        self.staticText5 = wx.StaticText(id=wxID_DIALOG1STATICTEXT5,
              label=_(u'Password'), name='staticText5', parent=self.panel6,
              style=wx.ALIGN_RIGHT)
              
        self.staticText6 = wx.StaticText(id=wxID_DIALOG1STATICTEXT6,
              label='', name='staticText6', parent=self,
              style=wx.ALIGN_RIGHT)
              
        self.staticText7 = wx.StaticText(id=wxID_DIALOG1STATICTEXT7,
              label=_(u'Repeat password'), name='staticText7', parent=self.panel7,
              style=wx.ALIGN_RIGHT)
              
        self.staticText8 = wx.StaticText(id=wxID_DIALOG1STATICTEXT8,
              label='', name='staticText8', parent=self,
              style=wx.ALIGN_RIGHT)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value='')
              
        self.textCtrl2 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL2, name='textCtrl2',
              parent=self, style=0, value='')
              
        self.textCtrl3 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL3, name='textCtrl3',
              parent=self, style=wx.TE_PASSWORD, value='')
              
        self.textCtrl4 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL4, name='textCtrl4',
              parent=self, style=wx.TE_PASSWORD, value='')

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=_(u'&Examine'),
              name='button1', parent=self, style=0)
              
        self.button2 = wx.Button(id=wxID_DIALOG1BUTTON2, label=_(u'&Examine'),
              name='button2', parent=self, style=0)

        self.buttonOk = wx.Button(id=wx.ID_OK, parent=self.panel1, style=0)

        self.buttonCancel = wx.Button(id=wx.ID_CANCEL, parent=self.panel2, 
              style=0)
              
        self.choice1 = wx.Choice(choices=[], id=wxID_DIALOG1CHOICE1,
              name='choice1', parent=self, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Add the encryption algorithms
        for i in Globals.ALGORITHMS_ENC:
            self.choice1.Append(i[0], i[1])
        self.choice1.Select(Globals.ALGORITHM_ENC_DEF)
        
        # Events
        wx.EVT_BUTTON(self.button1, wxID_DIALOG1BUTTON1, self.OnButton1Button)
        wx.EVT_BUTTON(self.button2, wxID_DIALOG1BUTTON2, self.OnButton2Button)
        wx.EVT_BUTTON(self.buttonOk, wx.ID_OK, self.OnOK)
        self.textCtrl1.Bind(wx.EVT_KILL_FOCUS, self.OnText1Input)
        
        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 50
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
            sample = text1 + '.enc'
            self.textCtrl2.SetValue(sample)
            # Select the base name of the auto-generated path
            self.textCtrl2.SetSelection(sample.rfind('/')+1, -1)
        
    def OnButton1Button(self, event):
        "Shows the file explorer dialog"
        # If None event we called it
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
        "Shows the file explorer dialog"
        # If None event we called it
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
        nomAux1 = self.textCtrl1.GetValue()
        nomAux2 = self.textCtrl2.GetValue()
        password = self.textCtrl3.GetValue()
        password2 = self.textCtrl4.GetValue()
        # If the file name is empty we can't continue
        if not nomAux1:
            Utilities.ErrorDialog( 
            _(u'Input the name of the file that you want to encrypt.'),
            _(u'Missing parameters'))
            return False
        # If the file name is empty we can't continue
        if not nomAux2:
            Utilities.ErrorDialog(
            _(u'Input the name of the encrypted file.'),
            _(u'Missing parameters'))
            return False
        # If the password is empty we can't continue
        if not password:
            Utilities.ErrorDialog(
            _(u'Input the password for the file.'), 
            _(u'Missing parameters'))
            return False
        # The password must be input the same twice
        if (password != password2):
            Utilities.ErrorDialog( 
                _(u'You must input the same password twice, try again.'))
            # Delete input passwords
            self.textCtrl3.SetValue('')
            self.textCtrl4.SetValue('')
            return
        # Source and destination files can't be the same
        if (nomAux1 == nomAux2):
            Utilities.ErrorDialog(
                _(u'Original and encrypted files cannot be the same.'))
            return
        # If destination file exists ask to overwrite
        if os.path.lexists(nomAux2):
            answer = Utilities.YesNoDialog(_(u'The file %s' \
                u' already exists. Overwrite it?') % nomAux2)
            if (answer == wx.ID_YES):
                try:
                    os.remove(nomAux2)
                except OSError, e:
                    Utilities.ErrorDialog(_(u'Cannot overwrite %s' % nomAux2)) 
                    return
            else:
                return
        # Hide the dialog
        self.EndModal(wx.ID_OK)
        # Encrypt the file
        algorithm = self.choice1.GetClientData(self.choice1.GetSelection())
        baseNameAux = Utilities.BasenameMod(nomAux1)
        baseNameAux2 = Utilities.BasenameMod(nomAux2)
        command = [(Globals.OPENSSL_BIN, ['enc','-e',algorithm,'-salt','-in',nomAux1,
            '-out',nomAux2], _(u'Encrypting %s') % baseNameAux)]
        try:
            # Change the cursor to BusyCursor
            self.busy = wx.BusyCursor()
            error, output = Executor.executeOpenssl(command, 
                _(u'Encrypting file'), password)
        finally :
            # Stop the busy cursor
            if self.busy:
                del self.busy
        # If there is a problem show error message
        if error:
            Utilities.Log(_(u'Can\'t encrypt %s') % baseNameAux + ': ' \
                '\n'.join(output),Utilities.ERRO)
        # Otherwise show Ok message
        else:
            Utilities.Log(_(u'The file %s has been created.') % baseNameAux2,
                Utilities.INFO)
