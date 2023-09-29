#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         CompressionDialog.py
# Purpose:      Shows the compression options.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: CompressionDialog.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import CompressionManager
import ConfigurationManager

import wx
from wx.lib.masked import NumCtrl
import os

def create(parent, severalFiles):
    dialog = Dialog1(parent, severalFiles)
    validador = ValidatorX()
    validador.SetWindow(dialog)
    return dialog

[wxID_DIALOG1, wxID_DIALOG1BUTTON1,
 wxID_DIALOG1CHECKBOX1, wxID_DIALOG1CHECKBOX2, wxID_DIALOG1CHOICE1, 
 wxID_DIALOG1CHOICE2, wxID_DIALOG1CHOICE3, wxID_DIALOG1PANEL1, 
 wxID_DIALOG1PANEL2, wxID_DIALOG1PANEL3, wxID_DIALOG1PANEL4, 
 wxID_DIALOG1PANEL5, wxID_DIALOG1PANEL6, wxID_DIALOG1PANEL7,
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, 
 wxID_DIALOG1STATICTEXT3, wxID_DIALOG1STATICTEXT4, wxID_DIALOG1STATICTEXT5, 
 wxID_DIALOG1TEXTCTRL1, wxID_DIALOG1TEXTCTRL2, wxID_DIALOG1TEXTCTRL3, 
] = [wx.NewId() for _init_ctrls in range(22)]

class ValidatorX(wx.PyValidator):
    def Clone():
        return ValidatorX()
    def Validate():
        return self.GetWindow().Validate()

class Dialog1(wx.Dialog):
        
    def _init_coll_gridSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button3, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.LEFT)

    def _init_coll_boxSizer6_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel1, 1, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.panel2, 1, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizer4_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.checkBox1, 3, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.panel6, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.textCtrl2, 3, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)

    def _init_coll_boxSizer5_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.checkBox2, 3, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.panel7, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.textCtrl3, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.choice3, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)

    def _init_coll_gridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button2, 0, border=5,
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

        parent.AddWindow(self.staticText3, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)
              
    def _init_coll_gridSizer6_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText4, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)
              
    def _init_coll_gridSizer7_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticText5, 0, border=5,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT)

    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel4, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.choice1, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.panel5, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.choice2, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizer2, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer3, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer5, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer4, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.boxSizer6, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.panel3, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.textCtrl1, 2, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.button1, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer3 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer4 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer5 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer6 = wx.BoxSizer(orient=wx.HORIZONTAL)

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
            style=wx.DEFAULT_DIALOG_STYLE, 
            title=_(u'Compression Options'))  

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
              label=_(u'File name'), name='staticText1', parent=self.panel3,
              style=0)

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=_(u'Compressor'), name='staticText2', parent=self.panel4,
              style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value=Globals.file)

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=_(u'&Examine'),
              name='button1', parent=self, style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_DIALOG1CHOICE1,
              name='choice1', parent=self, style=0)

        self.choice2 = wx.Choice(choices=[], id=wxID_DIALOG1CHOICE2,
              name='choice2', parent=self, style=0)

        self.staticText3 = wx.StaticText(id=wxID_DIALOG1STATICTEXT3,
              label=_(u'Compression level'), name='staticText3', 
              parent=self.panel5, style=0)

        self.checkBox1 = wx.CheckBox(id=wxID_DIALOG1CHECKBOX1,
              label=_(u'Encrypt'), name='checkBox1', parent=self, style=0)

        self.checkBox2 = wx.CheckBox(id=wxID_DIALOG1CHECKBOX2,
              label=_(u'Split into volumes'), name='checkBox2', parent=self,
              style=0)

        self.staticText4 = wx.StaticText(id=wxID_DIALOG1STATICTEXT4,
              label=_(u'Password'), name='staticText4', parent=self.panel6,
              style=0)

        self.staticText5 = wx.StaticText(id=wxID_DIALOG1STATICTEXT5,
              label=_(u'Size'), name='staticText5', parent=self.panel7,
              style=0)

        self.textCtrl2 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL2, name='textCtrl2',
              parent=self, style=wx.TE_PASSWORD, value='')

        self.textCtrl3 = NumCtrl(id=wxID_DIALOG1TEXTCTRL3, name='textCtrl3',
              parent=self, style=0, allowNone=True, value=None, groupDigits=False)

        self.choice3 = wx.Choice(choices=[], id=wxID_DIALOG1CHOICE3,
              name='choice3', parent=self, style=0)

        self.button2 = wx.Button(id=wx.ID_OK, 
              name='button2', parent=self.panel1, style=0)

        self.button3 = wx.Button(id=wx.ID_CANCEL, 
              name='button3', parent=self.panel2, style=0)

        self._init_sizers()

    def __init__(self, parent, severalFiles):
        "Dialog's constructor"
        
        # Save the severalFiles variable
        self.severalFiles = severalFiles
        
        # Call BOA's init functions
        self._init_ctrls(parent)
        
        # Add the formats that we can manage
        last = None
        j = 0
        for i in CompressionManager.compressorNames():
            if CompressionManager.canCompress(i[1]):
                self.choice1.Append(i[0],i[1])
                # Try to select the last choosen
                if Globals.lastCompressor:
                    if Globals.lastCompressor == i[1]:
                        last = j
                j += 1
        if last:
            self.choice1.Select(last)
        else:
            self.choice1.Select(0)
        # Emulates the manual choose (needed)
        self.oldExtension = None
        self.OnChoice1Choice(None)
        
        # Adds the KB/MB check
        self.choice3.Append(
            'KB',
            1)
        self.choice3.Append(
            'MB',
            1024)
        self.choice3.Append(
            'GB',
            1024*1024)
        self.choice3.Select(1)
        
        # Events
        wx.EVT_BUTTON(self.button1, wxID_DIALOG1BUTTON1, self.OnButton1Button)
        wx.EVT_BUTTON(self.button2, wx.ID_OK, self.OnOK)
        wx.EVT_CHECKBOX(self.checkBox1, wxID_DIALOG1CHECKBOX1,
              self.OnCheckBox1Checkbox)
        wx.EVT_CHECKBOX(self.checkBox2, wxID_DIALOG1CHECKBOX2,
              self.OnCheckBox2Checkbox)
        wx.EVT_CHOICE(self.choice1, wxID_DIALOG1CHOICE1, self.OnChoice1Choice)
        
        # Set the window size
        width = self.GetBestSize().x + 30
        height = self.GetBestSize().y + 40
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))

    def OnButton1Button(self, event):
        "Shows the file dialog"
        # If None event we called it
        if event:
            event.StopPropagation()
        dialog = wx.FileDialog(self, style=wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl1.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def OnCheckBox1Checkbox(self, event):
        "Enables the password input"
        # If None event we called it
        if event:
            event.StopPropagation()
        self.textCtrl2.Enable(self.checkBox1.IsChecked())

    def OnCheckBox2Checkbox(self, event):
        "Enables the volume's size input"
        # If None event we called it
        if event:
            event.StopPropagation()
        self.textCtrl3.Enable(self.checkBox2.IsChecked())
        self.choice3.Enable(self.checkBox2.IsChecked())

    def OnChoice1Choice(self, event):
        "Change compressor. Updates the compression levels and enables options"
        # If None event we called it
        if event:
            event.StopPropagation()
        format = self.choice1.GetClientData(self.choice1.GetSelection())
        
        # Can't add several files to a non-packable (gz and bz2 without tar)
        if ((not CompressionManager.canPack(format)) 
            and (self.severalFiles)):
            Utilities.ErrorDialog(
                _(u'The choosen format can store only one file.') + '\n' \
                '' + _(u'We advise you to use a tar-based format.'))
            self.choice1.Select(0)
            self.OnChoice1Choice(None)
            return
        
        self.choice2.Clear()
        levels = CompressionManager.compressionLevels(format)
        i=0
        for level in levels:
            self.choice2.Append(level[0],level[1])
            # Check if it's default
            if level[2]: 
                self.choice2.Select(i)
            i=i+1
        # Update the checkboxs
        if (not CompressionManager.canEncrypt(format)):
            self.checkBox1.SetValue(False)
        self.checkBox1.Enable(CompressionManager.canEncrypt(format))
        # Emulates the OnCheck event
        self.OnCheckBox1Checkbox(None)
        if (not CompressionManager.canSplit(format)):
            self.checkBox2.SetValue(False)
        self.checkBox2.Enable(CompressionManager.canSplit(format))
        # Emulates the OnCheck event
        self.OnCheckBox2Checkbox(None)
        
        # Add an extension to the file
        forExtensions = CompressionManager.extensions(format)
        fileNameAux = self.textCtrl1.GetValue()
        extOk = False
        for ext in forExtensions:
            if fileNameAux.upper().endswith(ext.upper()):
                if (not self.oldExtension) or (not fileNameAux.upper().endswith(self.oldExtension.upper())):
                    extOk = True
                    self.oldExtension = ext
        if not extOk:
            if self.oldExtension:
                if fileNameAux.upper().endswith(self.oldExtension.upper()):
                    fileNameAux = fileNameAux[:-len(self.oldExtension)]
            self.textCtrl1.SetValue(fileNameAux + forExtensions[0])
            self.oldExtension = forExtensions[0]
    
    # Because wx.ID_OK is a special button we need a function with this name
    def OnOK( self, event ):
        "Manages the ID_OK OnClick event"
        if self.Validate():
            self.EndModal(wx.ID_OK)
        
    def Validate(self):
        "Validates and changes the compression options"
        # Get filename and it's format
        nomAux = self.textCtrl1.GetValue()
        forAux = self.choice1.GetClientData(self.choice1.GetSelection())
        # If empty name we can't continue
        if not nomAux:
            Utilities.ErrorDialog(
            _(u'Input the of the file that you want to create.'), 
            _(u'Missing parameters'))
            return False

        # If no proper extension for filename we show a warning and add it
        name = CompressionManager.checkFilename(nomAux, forAux)
        if nomAux != name:
            renameOk = Utilities.YesNoDialog(
                _(u'Filename will be changed to %s') % name, 
                _(u'Invalid extension'))
            if renameOk != wx.ID_YES:
                return False
        # Check if the file already exists. If it's a folder we can't continue
        if os.path.isdir(name):             
            Utilities.ErrorDialog(
                _(u'Cannot create a file with this name because') + '\n' \
                '' + _(u'a folder with the same name already exists.'))
            return False
        # If it's a file we ask about delete it
        elif os.path.isfile(name):
            answer = Utilities.YesNoDialog(_(u'The file %s' \
                u' already exists. Do you want to overwrite it?') % name)
            if (answer == wx.ID_YES):
                try:
                    os.remove(name)
                except OSError, e:
                    Utilities.ErrorDialog(_(u'Can\'t overwrite %s' % name))
                    return False
            else:
                return False
        # Reset the compression options
        Globals.compressionOptions = Globals.CompressionOptions()
        # Name of the file
        Globals.file = name
        # Format
        CompressionManager.setFormat(forAux)
        # Save information about the last used
        Globals.lastCompressor = forAux
        ConfigurationManager.saveValue('lastCompressor', forAux)
        # Compression level
        Globals.compressionOptions.level = self.choice2.GetClientData(
            self.choice2.GetSelection())
        # Password
        if (self.checkBox1.IsChecked() and (self.textCtrl2.GetValue())):
            Globals.compressionOptions.password = self.textCtrl2.GetValue()
        # Volumes, it's size is set in Kilobytes
        multiple = self.choice3.GetClientData(self.choice3.GetSelection())
        if (self.checkBox2.IsChecked() and (self.textCtrl3.GetValue())):
            Globals.compressionOptions.volumes = str(int(self.textCtrl3.GetValue()) * 
                int(multiple))
        return True

