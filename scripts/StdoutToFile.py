#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         StdoutToFile.py
# Purpose:      Redirects the output of a program to a file.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: StdoutToFile.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import sys
import os
import subprocess

import GettextLoader 

def main():
    "Execute and redirect the output to a file"

    # Check the input parameters
    if len(sys.argv) < 3:
        sys.stderr.write((_(u'Usage: StdoutToFile.py file exec [parameters]' \
            '')+'\n').encode(sys.getfilesystemencoding()))
        sys.exit(1)
        
    # Decode the input parameters
    argvAux = []
    for argv in sys.argv:
        argvAux.append(argv.decode(sys.getfilesystemencoding(),'replace'))

    try:
        # Open the file
        file = open(argvAux[1], 'w')
    except IOError, e:
        sys.stderr.write((_(u'Error when creating the file %s') % 
            argvAux[1] + ': ' + unicode(e)).encode(sys.getfilesystemencoding()))
        sys.exit(1)
        
    # Execute the command
    try:
        popen = subprocess.Popen(argvAux[2:], bufsize=4096, stdout=file, stderr=subprocess.PIPE)
        errMessage = popen.communicate()
        # Check the subprocess status
        if popen.returncode:
            sys.stderr.write(errMessage[1])
            sys.exit(1)
    # Error handling for unexpected errors
    except Exception, e:
        file.close()
        sys.stderr.write((unicode(e)).encode(sys.getfilesystemencoding()))
        sys.exit(1)
        
    file.close()

if __name__ == '__main__':
    main()
    
