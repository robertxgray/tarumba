#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boa:Dialog:Dialog1

#----------------------------------------------------------------------------
# Name:         CustomProgressDialog.py
# Purpose:      Custom progress dialog because original does not fit our needs.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: CustomProgressDialog.py $
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

def create(parent_pid, title, message, maximum, unknownProgress, logFile):
    return Dialog1(parent_pid, title, message, maximum, unknownProgress, logFile)

[wxID_DIALOG1, wxID_DIALOG1BUTTON1, wxID_DIALOG1GAUGE1, 
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1TIMER1
] = [wx.NewId() for _init_ctrls in range(5)]

class Dialog1(wx.Dialog):
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)

        self.SetSizer(self.boxSizer1)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit
        
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddSizer(self.boxSizer2, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.gauge1, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.button1, 0, border=0, flag=wx.CENTER)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        
    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit
        
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)
        parent.AddWindow(self.staticText1, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(10, 10), border=0, flag=0)

    def _init_ctrls(self, prnt, title, message, maximum, unknownProgress):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              style=wx.CAPTION, title=title)

        self.gauge1 = wx.Gauge(id=wxID_DIALOG1GAUGE1, name='gauge1',
              parent=self, range=maximum, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=_(u'Abort'),
              name='button1', parent=self, style=0)

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=self._message, name='staticText1', parent=self,
              style=wx.ALIGN_LEFT)

        self._init_sizers()

    def __init__(self, parent_pid, title, message, maximum, unknownProgress,
        logfile):
        "Class constructor"
        # Init the variables
        self._message = message
        self._current = 0
        self._maximum = maximum
        self._increase = True
        self._unknownProgress = unknownProgress
        self._parent_pid = parent_pid
        self._logfile = open(logfile, 'r')
        # Call Boa auto-generated functions
        self._init_ctrls(None, title, message, maximum, unknownProgress)
        # Events
        wx.EVT_BUTTON(self.button1, wxID_DIALOG1BUTTON1, self.OnButton1Button)
        wx.EVT_TIMER(self, wxID_DIALOG1TIMER1, self.ProgressUpdate)
        self.Bind(wx.EVT_CLOSE, self.NoClose)
        
        # The dialog can be shown/hidden with the SIGUSR1 and SIGUSR2 signals
        signal.signal(signal.SIGUSR1, self.UserShow)
        signal.signal(signal.SIGUSR2, self.UserHide)
        
        # Add a Timer to update the progress dialog
        self._timer = wx.Timer(self, wxID_DIALOG1TIMER1)
        self._timer.Start(100)
        
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
        
        # Set the window size
        width = 400 #self.GetBestSize().x
        height = self.GetBestSize().y
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))
        
########################
## PERSONAL FUNCTIONS ##
########################
        
    def OnButton1Button(self, event):
        "Abort the execution of the subprocess"
        # If None event we called it
        if event:
            event.StopPropagation()
        # The comunication is set via the SIGUSR1
        # See Executor for more details
        os.kill(self._parent_pid, signal.SIGUSR1)
        
    def ProgressUpdate(self, event):
        "Updates the progress dialog"
        # If None event we called it
        if event:
            event.StopPropagation()
        # Stop the timer
        self._timer.Stop()
        try:
            # Read the last line of the log file
            self._logfile.seek(0, os.SEEK_END)
            position = self._logfile.tell()
            curChar = ''
            while (position > 0) and (curChar != '\n'):
                self._logfile.seek(-2, os.SEEK_CUR)
                curChar = self._logfile.read(1)
                position -= 1
            input = self._logfile.readline()
            if input:
                self._current = int(input[:input.find(' ')])
                self._message = input[input.find(' ')+1:]
            # If the progress is unknown, autocalculate the next value
            # I have tried with Pulse, but it doesn't work
            if self._unknownProgress:
                if self._increase:
                    self._current += 1
                    if self._current >= self._maximum-1:
                        self._increase = False
                else:
                    self._current -= 1
                    if self._current <= 1:
                        self._increase = True
                self.gauge1.SetValue(self._current)
            # Else use the setted value and update the message
            else: 
                self.gauge1.SetValue(self._current)
                self.staticText1.SetLabel(self._message)
        finally:
            # Resume the timer
            self._timer.Start()
        
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
        self._logfile.close()
        self._timer.Stop()
        wx.Dialog.Destroy(self)
        
if __name__ == '__main__':
    # Init a new wx.App and show the dialog   
    args = sys.argv 
    application = wx.App(redirect=False,clearSigInt=False)
    gui = create(int(args[1]), args[2], args[3], int(args[4]),
            int(args[5]), args[6])
    application.SetTopWindow(gui)
    gui.CentreOnScreen(wx.BOTH)
    gui.Show()
    application.MainLoop()
        
