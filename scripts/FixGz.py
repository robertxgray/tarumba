#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         FixGZ.py
# Purpose:      Script to fix gzip files.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: FixGz.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# This script is inspired in the fixgz.c by Jean-loup Gailly

import sys
import os

import GettextLoader 

def printstdout(message):
    "Write in the standart output"
    sys.stdout.write(message.encode(sys.getfilesystemencoding(),'replace')+'\n')

def printstderr(message):
    "Write in the error output"
    sys.stderr.write(message.encode(sys.getfilesystemencoding(),'replace')+'\n')

def main():
    "Repair gzip files"

    # Check the input parameters
    if (len(sys.argv) < 2) or (len(sys.argv) > 3):
        printstderr(_(u'Enter the original filename and the name of the new file ' \
         u'after the reparation. If no original file is given, stdin will be used.'))
        sys.exit(1)
    
    # Show information about the program
    printstdout(_(u'Gzip file fixer for Tarumba.'))
    
    # Decode the input parameters
    if len(sys.argv) == 3:
        originalName = sys.argv[1].decode(sys.getfilesystemencoding(),'replace')
        repairedName = sys.argv[2].decode(sys.getfilesystemencoding(),'replace')
        printstdout(_(u'Input file') + ': ' + originalName)
    else:
        repairedName = sys.argv[1].decode(sys.getfilesystemencoding(),'replace')
    printstdout(_(u'Output file') + ': ' + repairedName + '\n')
    
    # Read the orginal file, if given
    if len(sys.argv) == 3:
        try:
            # Open the original file for reading
            original = open(originalName, 'rb')
        except IOError, e:
            printstderr(_(u'Error when opening the file %s') % 
                originalName + ': ' + unicode(e))
            sys.exit(1)
    # Else use the standart input
    else:
        original = sys.stdin
    
    try:
        # Open the repaired file for writing
        repaired = open(repairedName, 'wb')
    except IOError, e:
        printstderr(_(u'Error when opening the file %s') % 
            repairedName + ': ' + unicode(e))
        sys.exit(1)
        
    byte1 = original.read(1)
    byte2 = ''
    i = 1
    # Read the next byte until the end of the file is reached
    while True:
        byte2 = original.read(1)
        if byte2 == '':
            break
        # Send to the repaired file without the \r\n characters
        if ((byte1 != '\r') or (byte2 != '\n')):
            repaired.write(byte1)
        else:
            printstdout(_(u'Possibly incorrect end of line deleted ' \
                u'in the position %i') % i)
        byte1 = byte2
        i += 1
    # Write the last byte
    repaired.write(byte1)
    
    printstdout('')

    # Close the original file
    try:
        original.close()
    except IOError, e:
        printstderr(_(u'Error when closing the file %s') %
            originalName + ': ' + unicode(e))
        exit(1) 

    # Close the repaired file
    try:
        repaired.close()
    except IOError, e:
        printstderr(_(u'Error when closing the file %s') %
            repairedName + ': ' + unicode(e))
        exit(1) 

    sys.exit(0)

if __name__ == '__main__':
    main()
