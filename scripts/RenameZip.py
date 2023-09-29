#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         RenameZip.py
# Purpose:      Script to rename the contents in a zip file.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: RenameZip.py $
# Copyright:    (c) 2012 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import sys
import os
import subprocess

import GettextLoader 

def printstdout(mensaje):
    "Write to the standart output"
    sys.stdout.write(mensaje.encode(sys.getfilesystemencoding(),'replace')+'\n')

def printstderr(mensaje):
    "Write to the error output"
    sys.stderr.write(mensaje.encode(sys.getfilesystemencoding(),'replace')+'\n')

def main():
    "Rename contents in zip files"

    # Check the input parameters
    if len(sys.argv) != 5:
        printstderr(_(u'Enter the path to the zipnote binary, the zip file to be modified, ' \
            'the content to be renamed and the new name/path for the content.'))
        sys.exit(1)
    
    # Decode the input parameters
    zipnote = sys.argv[1].decode(sys.getfilesystemencoding(),'replace')
    zipfile = sys.argv[2].decode(sys.getfilesystemencoding(),'replace')
    oldName = sys.argv[3].decode(sys.getfilesystemencoding(),'replace')
    newName = sys.argv[4].decode(sys.getfilesystemencoding(),'replace')
    
    # If oldName is a directory, newName must be a directory
    if (oldName[-1] == '/') and (newName[-1] != '/'):
        newName = newName + '/'
    
    # Show information about the program
    printstdout(_(u'Zip renamer for Tarumba.'))
    printstdout(_(u'Renaming %(oldname)s to %(newname)s in %(zipfile)s')
        % {'oldname':oldName, 'newname':newName, 'zipfile':zipfile})
        
    # Get the file information via zipnote
    subProc = subprocess.Popen([zipnote, zipfile], bufsize=-1,
        stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procOutput, stderr = subProc.communicate()
    procOutput = procOutput.decode(sys.getfilesystemencoding(),'replace')
    procStatus = subProc.returncode
    # Exit if zipnote fails
    if procStatus != 0:
        printstderr(_(u'Error when reading the file with zipnote') + ': ' + procOutput)
        sys.exit(1)
        
    # Convert the zipnote output to an array for better handling
    notes = procOutput.split('\n')
        
    # Process the zipnote output
    i = 1
    for line in notes:
        # Check if the content must be renamed
        rename = False
        # Oldname is a directory
        if oldName[-1] == '/':
            if line.startswith('@ '+oldName):
                rename = True
        # Oldname is a file
        else:
            if line == '@ '+oldName:
                rename = True
                   
        # Perform the renaming operation
        # For more details, see the manpage of zipnote
        if rename:
            zipnoteInput = '@='+line[2:]  
            # Get the name of the renamed content
            zipnoteInput = zipnoteInput.replace(oldName, newName, 1)
            # Add the line to the file
            notes.insert(i, zipnoteInput)
        i += 1
        
    # Use zipnote again, to apply the changes
    subProc = subprocess.Popen([zipnote, '-w', zipfile], bufsize=-1,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    procOutput, stderr = subProc.communicate(
        '\n'.join(notes).encode(sys.getfilesystemencoding(),'replace'))
    procOutput = procOutput.decode(sys.getfilesystemencoding(),'replace')
    procStatus = subProc.returncode
    # Exit if zipnote fails
    if procStatus != 0:
        printstderr(_(u'Error when applying the changes with zipnote') + ': ' + procOutput)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
