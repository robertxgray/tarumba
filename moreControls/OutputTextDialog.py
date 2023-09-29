#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boa:Dialog:Dialog1

#----------------------------------------------------------------------------
# Name:         OutputTextDialog.py
# Purpose:      Dialog with a TextCtrl to show program's output.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: OutputTextCtrl.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wxversion
wxversion.select('2.8')

import wx
import sys
import os
import select
import signal

import GettextLoader  

def create(parent_pid, title):
    return Dialog1(parent_pid, title)

[wxID_DIALOG1, wxID_DIALOG1PANEL1, wxID_DIALOG1TEXTCTRL1, wxID_DIALOG1BUTTON1,
 wxID_DIALOG1TIMER1
] = [wx.NewId() for _init_ctrls in range(5)]

class Dialog1(wx.Dialog):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.textCtrl1, 1, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.button1, 0, border=0, flag=wx.CENTER)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.panel1.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt, titl=''):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              size=wx.Size(600, 400),
              style=wx.CAPTION | wx.RESIZE_BORDER, title=titl)
        self.SetClientSize(wx.Size(600, 400))

        self.panel1 = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel1',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1,
              style=wx.TE_MULTILINE | wx.TE_READONLY, value='')

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=_(u'Abort'),
              name='button1', parent=self.panel1, style=0)

        self._init_sizers()

    def __init__(self, parent_pid, title):
        self._init_ctrls(None, title)
        self._parent_pid = parent_pid
        # Events
        wx.EVT_BUTTON(self.button1, wxID_DIALOG1BUTTON1, self.OnButton1Button)
        wx.EVT_TIMER(self, wxID_DIALOG1TIMER1, self.ProgressUpdate)
        self.Bind(wx.EVT_CLOSE, self.NoClose)
        # Flag to know if the process finishes
        self._finished = False
        
        # Add a Timer to update the progress dialog
        self._timer = wx.Timer(self, wxID_DIALOG1TIMER1)
        self._timer.Start(100)
        
        # Capture the SIGTERM signals. The log can be closed
        signal.signal(signal.SIGINT, self.End)
        # The dialog can be shown/hidden with the SIGUSR1 and SIGUSR2 signals
        signal.signal(signal.SIGUSR1, self.UserShow)
        signal.signal(signal.SIGUSR2, self.UserHide)
        
        # Set the icon for the window
        TARUMBA_ICONS = os.getenv('TARUMBA_ICONS')
        if not(TARUMBA_ICONS):
            TARUMBA_ICONS = os.path.join(os.path.dirname(sys.argv[0]), '../icons')
        bundle = wx.IconBundle() 
        bundle.AddIconFromFile(TARUMBA_ICONS+'/64x64.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(TARUMBA_ICONS+'/48x48.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(TARUMBA_ICONS+'/32x32.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(TARUMBA_ICONS+'/22x22.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIconFromFile(TARUMBA_ICONS+'/16x16.png',
            wx.BITMAP_TYPE_PNG)
        self.SetIcons(bundle)

########################
## PERSONAL FUNCTIONS ##
########################
               
    def End(self, signum, frame):
        "Allows the dialog to be closed"
        self.button1.SetLabel(_(u'Close'))
        self._finished = True
        
    def ProgressUpdate(self, event):
        "Updates the progress dialog"
        # If None event we called it
        if event:
            event.StopPropagation()
        # Search for input
        input = ''
        (rr, wr, er) = select.select([sys.stdin], [], [],0)
        if rr:
            input = sys.stdin.readline()
            if input:
                self.textCtrl1.AppendText(input)
        
    def OnButton1Button(self, event):
        "Close the dialog from the close button"
        # If null event we have called it
        if event:
            event.StopPropagation()
        # If the process has finished, close the dialog
        if self._finished:
            self.Destroy()
        # Else terminate the process
        else:
            # The comunication is set via the SIGUSR1
            # See Executor for more details
            os.kill(self._parent_pid, signal.SIGUSR1)
        
    def NoClose(self, event):
        "Avoids the dialog to be closed"
        event.Veto(True)
        
    def UserShow(self, signum, frame):
        "Shows the dialog when SIGUSR1 is received"
        self.Show(True)
        
    def UserHide(self, signum, frame):
        "Hides the dialog when SIGUSR2 is received"
        self.Show(False)
        
    def Destroy(self):
        "Class destructor"
        self._timer.Stop()
        wx.Dialog.Destroy(self)

if __name__ == '__main__':
    # Init a new wx.App and show the dialog   
    args = sys.argv 
    application = wx.App(redirect=False,clearSigInt=False)
    gui = create(int(args[1]), args[2])
    application.SetTopWindow(gui)
    gui.CentreOnScreen(wx.BOTH)
    gui.Show()
    application.MainLoop()
        
