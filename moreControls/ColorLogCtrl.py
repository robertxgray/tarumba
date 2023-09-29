# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         ColorLogCtrl.py
# Purpose:      Shows the log of the application with colors.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: ColorLogCtrl.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx
import wx.stc

class ColorLogCtrl(wx.stc.StyledTextCtrl):
    "Shows the log of the application with colors."
    
    def __init__(self, parent, id, name):
        wx.stc.StyledTextCtrl.__init__(self, parent, id, name=name)
        
        # Log level definition
        self.INFO = 1
        self.WARN = 2
        self.ERRO = 3
        self.SPAM = 4
        
        # Don't show the horizontal scrollbar
        self.SetUseHorizontalScrollBar(False)
        self.SetWrapMode(wx.stc.STC_WRAP_WORD)
        # The log can't be modified
        self.SetReadOnly(True)
        # Style definition
        self.StyleSetSpec(self.INFO, 'bold,fore:#007000')
        self.StyleSetSpec(self.WARN, 'bold,fore:#D38A04')
        self.StyleSetSpec(self.ERRO, 'bold,fore:#BB0000')
        self.StyleSetSpec(self.SPAM, 'bold,fore:#0000BB')

        # Markers definition
        self.SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL)
        flecha = wx.stc.STC_MARK_SHORTARROW
        self.MarkerDefine(self.INFO, flecha, '#007000', '#007000')
        self.MarkerDefine(self.WARN, flecha, '#D38A04', '#D38A04')
        self.MarkerDefine(self.ERRO, flecha, '#BB0000', '#BB0000')
        self.MarkerDefine(self.SPAM, flecha, '#0000BB', '#0000BB')
        
    def Log(self, text, level):
        "Adds a message to the log window"
        linea = self.GetLineCount()-1
        caracter = self.GetLength()
        # We need to turn off the readonly
        # Maybe not the best way of doing this...
        self.SetReadOnly(False)
        # Add text
        self.AddText(text)
        # Add style
        self.StartStyling(caracter,0xff)
        # Multiply by 4 because of the unicode characters (4 bits max)
        self.SetStyling(len(text)*4, level)
        # Add marker
        self.MarkerAdd(linea, level)
        self.SetReadOnly(True)
        # Go to the end of the log
        self.DocumentEnd()
        
