#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         RenameTar.py
# Purpose:      Script to rename the contents in a tar file.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: RenameTar.py $
# Copyright:    (c) 2012 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# The GNU ././@LongLink extension is not supported because filenames longer than
# 100 characters cannot be handled without affecting the file size.

import sys
import os

import GettextLoader 

def printstdout(mensaje):
    "Write to the standart output"
    sys.stdout.write(mensaje.encode(sys.getfilesystemencoding(),'replace')+'\n')

def printstderr(mensaje):
    "Write to the error output"
    sys.stderr.write(mensaje.encode(sys.getfilesystemencoding(),'replace')+'\n')

def main():
    "Rename contents in tar files"

    # Check the input parameters
    if len(sys.argv) != 5:
        printstderr(_(u'Enter the tarfile to be modified, the content to be renamed, ' \
            u'it\'s occurrence and the new name/path for the content.'))
        sys.exit(1)
    
    # Decode the input parameters
    tarfileName = sys.argv[1].decode(sys.getfilesystemencoding(),'replace')
    oldName = sys.argv[2].decode(sys.getfilesystemencoding(),'replace')
    occurrence = int(sys.argv[3].decode(sys.getfilesystemencoding(),'replace'))
    newName = sys.argv[4].decode(sys.getfilesystemencoding(),'replace')
    
    # If oldName is a directory, newName must be a directory
    if (oldName[-1] == '/') and (newName[-1] != '/'):
        newName = newName + '/'

    # "Magic" pattern to detect inside the tar file
    src = (ord('u'),ord('s'),ord('t'),ord('a'),ord('r'),ord(' '), ord(' '),0);
    
    # Show information about the program
    printstdout(_(u'Tar renamer for Tarumba.'))
    printstdout(_(u'Renaming %(oldname)s to %(newname)s in %(tarfile)s')
        % {'oldname':oldName, 'newname':newName, 'tarfile':tarfileName})

    try:
        # Open the tar file for reading/writing
        tarfile = open(tarfileName, 'rb+')
    except IOError, e:
        printstderr(_(u'Error when opening the file %s') % 
            tarfileName + ': ' + unicode(e))
        sys.exit(1)
    
    success = 0
    occurrenceIndex = 1
    renamingCompleted = False
   
    byte = ''
    header = ''
    # Read the next byte until the end of the file is reached
    while not renamingCompleted:
        byte = tarfile.read(1)
        if byte == '':
            break

        # Compare with the magic string
        if (ord(byte) != src[success]):
            success = 0
            continue
        success += 1
        
        # If the magic string is found
        if (success == len(src)):
            # We have a posible header in (position - 265)!
            position = tarfile.tell() - 265;
            try:
                tarfile.seek(position,0)
            except IOError, e:
                printstderr(_(u'Error when going to the position ' \
                    u'%(position)i of the file %(file)s') % 
                    {'position':position, 'file':tarfileName}+': '+unicode(e))
                exit(1) 

            # Try to get 512 bytes from the header
            header = tarfile.read(512)
	    
            if (len(header) < 512):
                printstderr(_(u'Cannot read 512 bytes of header' \
                    u' in the position %(position)i of the file %(file)s') %
                    {'position':position, 'file':tarfileName})
                exit(1)
            
            # The 100 first bytes of the header are the file name
            name = header[0:100].decode(sys.getfilesystemencoding(),'replace')
            # Remove the null characters
            name = name.replace('\x00', '')
            # The 12 bytes before the 124 is the size ended by a null byte,
            # omitted by reading one less. The size is given in octal base
            size = long(header[124:135],8)
            
            # Check if the content must be renamed
            rename = False
            # Oldname is a directory
            if oldName[-1] == '/':
                if name.startswith(oldName):
                    rename = True
            # Oldname is a file
            else:
                if name == oldName:
                    # Only rename the selected ocurrence of the file
                    if occurrenceIndex == occurrence:
                        rename = True
                        renamingCompleted = True
                    occurrenceIndex += 1
            
            # Perform the renaming operation
            if rename:
                # Get the name of the renamed content
                nameAux = name.replace(oldName, newName, 1)
                nameAuxEnc = nameAux.encode(sys.getfilesystemencoding(),'replace')
                # Check the 100 characters limit
                if len(nameAux) > 100:
                    printstderr(_(u'Error: The name %s is longer than 100 characters')%nameAux)
                    exit(1)
                # Add the null characters again
                nameAuxEnc = nameAuxEnc.ljust(100,'\x00')
                # Write the new name
                try:
                    tarfile.seek(position,0)
                    tarfile.write(nameAuxEnc)
                except IOError, e:
                    printstderr(_(u'Error when writing in the position ' \
                        u'%(position)i of the file %(file)s') % 
                        {'position':position, 'file':tarfileName}+': '+unicode(e))
                    exit(1)
                # Re-calculate the checksum
                checksum = 0
                # The checksum is calculated by taking the sum of the unsigned
                # byte values of the header block
                for i in range(512):
                    if i < 100:
                        checksum += ord(nameAuxEnc[i])
                    # With the eight checksum bytes taken to be ascii spaces
                    elif (i>=148) and (i<=155):
                        checksum += 32
                    else:
                        checksum += ord(header[i])
                # Write the new checksum
                try:
                    tarfile.seek(position+148,0)
                    # It is stored as a six digit octal number with leading zeroes
                    # followed by a NUL and then a space
                    tarfile.write(('%o\x00 '%checksum).rjust(8,'0'))
                except IOError, e:
                    printstderr(_(u'Error when writing in the position ' \
                        u'%(position)i of the file %(file)s') % 
                        {'position':position+148, 'file':tarfileName}+': '+unicode(e))
                    exit(1)
            
            # Advance to the next content
            try:
                tarfile.seek(position+512+size,0)
            except IOError, e:
                printstderr(_(u'Error when going to the position ' \
                    u'%(position)i of the file %(file)s') % 
                    {'position':position+512+size, 'file':tarfileName}+': '+unicode(e))
                exit(1)
            
            success = 0

    # Close the tar file
    try:
        tarfile.close()
    except IOError, e:
        printstderr(_(u'Error when closing the file %s') % 
            tarfileName + ': ' + unicode(e))
        exit(1) 

    sys.exit(0)

if __name__ == '__main__':
    main()
