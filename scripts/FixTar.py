#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         FixTar.py
# Purpose:      Script to fix tar files
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: FixTar.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# This script is inspired in the find_tar_headers.pl by Tore Skjellnes

import sys
import os
import collections

import GettextLoader 

def printstdout(mensaje):
    "Write to the standart output"
    sys.stdout.write(mensaje.encode(sys.getfilesystemencoding(),'replace')+'\n')

def printstderr(mensaje):
    "Write to the error output"
    sys.stderr.write(mensaje.encode(sys.getfilesystemencoding(),'replace')+'\n')

def main():
    "Repair tar files"

    # Check the input parameters
    if (len(sys.argv) < 2) or (len(sys.argv) > 3):
        printstderr(_(u'Enter the original filename and the name of the new file ' \
         u'after the reparation. If no original file is given, stdin will be used.'))
        sys.exit(1)

    # "Magic" pattern to detect inside the tar file
    src = (ord('u'),ord('s'),ord('t'),ord('a'),ord('r'),ord(' '), ord(' '),0);
    
    # Show information about the program
    printstdout(_(u'Tar file fixer for Tarumba.'))
    
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
    
    # Buffers to avoid the use of seek when a header is found
    headerBuffer = collections.deque(maxlen=265)
    falseHeader = collections.deque()
    
    anyFound = False
    anyFixed = False
    success = 0
    byte = ''
    bytesRead = 0
    bytesWritten = 0
    header = ''
    # Read the next byte until the end of the file is reached
    while True:
        
        # If a false header was previously found, continue reading what is left
        if falseHeader:
            byte = falseHeader.popleft()
        # Else read the next byte
        else:
            byte = original.read(1)
            if byte == '':
                break
        headerBuffer.append(byte)
        bytesRead += 1

        # Compare with the magic string
        if (ord(byte) != src[success]):
            success = 0
            continue
        success += 1
        
        # If the magic string is found
        if (success == len(src)):
            # We have a posible header in (position - 265)!
            position = bytesRead - 265;
            # Try to get 512 bytes from the header
            header = ''.join(list(headerBuffer)) + original.read(512-265)
            if (len(header) != 512):
                printstderr(_(u'Cannot read 512 bytes of header' \
                    u' in the position %(position)i of the file %(file)s') %
                    {'position':position, 'file':tarfileName})
                success = 0
                continue
            
            # The 100 first bytes of the header are the file name
            name = header[0:100].decode(sys.getfilesystemencoding(),'replace')
            # Remove the null characters
            name = name.replace('\x00', '')
            
            try:
                # The 12 bytes before the 124 is the size ended by a null byte,
                # omitted by reading one less. The size is given in octal base
                size = long(header[124:135],8)
                # Checksum for header block. For better compatibility, ignore leading
                # and trailing whitespace, and get the first six digits
                checksum_head = long(header[148:155].strip()[:6],8)
            # If the octal transformation fails, it is not a header
            except Exception, e:
                falseHeader.extend(list(header[265:]))
                success = 0
                continue
            
            # Calculate the checksum
            checksum_calc = 0
            # The checksum is calculated by taking the sum of the unsigned
            # byte values of the header block
            for i in range(512):
                # With the eight checksum bytes taken to be ascii spaces
                if (i>=148) and (i<=155):
                    checksum_calc += 32
                else:
                    checksum_calc += ord(header[i])
                    
            # Show some info text
            anyFound = True
            printstdout(_(u'Header found in the position %i.') % position)
            printstdout(_(u'Checksum: %(cksum1)o. Expected: %(cksum2)o.')
                % {'cksum1':checksum_head, 'cksum2':checksum_calc})
            
            # The header seems ok
            if checksum_head == checksum_calc:
                anyFixed = True
                printstdout(_(u'Valid header. Recovering information.'))
                printstdout(name + '. ' + str(size) + ' ' + _(u'bytes'))
            
                # Copy the header + file to the restored
                remaining = size
                repaired.write(header)
                dataAvailable = True
                while remaining > 0:
                    # Use a buffer
                    if remaining >= 4096:
                        bufSize = 4096
                    else:
                        bufSize = remaining
                    buffer = original.read(bufSize)
                    # If no data available, fill it with \0
                    if len(buffer) < bufSize:
                        buffer = buffer.ljust(bufSize,'\x00')
                        # Show an error message
                        if dataAvailable:
                            dataAvailable = False
                            printstderr(
                                _(u'WARNING: Missing data. Filling the empty space with zeros.'))
                    repaired.write(buffer)
                    remaining -= bufSize
                # Fill with zeros the block until get 512
                if (size % 512 != 0):
                    remaining2 = 512 - (size % 512)
                    repaired.write('\0' * remaining2)
                # Remember the number of bytes written for blocking size
                bytesWritten += 512 + size + remaining2
                printstdout('')
            
            # The header is damaged
            else:
                printstdout(_(u'The header is damaged and must be discarded.')+'\n')
                falseHeader.extend(list(header[265:]))
                
            success = 0
            
    # Fill with zeros until the standar record size is reached
    if (bytesWritten % 10240 != 0):
        remaining3 = 10240 - (bytesWritten % 10240)
        repaired.write('\0' * remaining3)

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

        # Give some feedback when done
    if anyFound:
        printstdout(_(u'Process completed. See the previous log for details.'))
    else:
        printstdout(_(u'No valid tar headers found. This is not a tar file or it is too damaged.'))
    
    # Return success if we were able to recover anything
    if anyFixed:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
