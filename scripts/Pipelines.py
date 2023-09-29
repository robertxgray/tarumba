#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Pipelines.py
# Purpose:      Simulates the behaviour of pipelines without a shell.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Pipelines.py $
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
    if len(sys.argv) < 2:
        sys.stderr.write((_(u'Usage: Pipelines.py [!] prog1 [parameters] /// [!] prog 2 [parameters] [///] [!] [prog3] ...' \
            '')+'\n').encode(sys.getfilesystemencoding()))
        sys.stderr.write((_(u'       The ! symbol means to ignore the error output for this program.' \
            '')+'\n').encode(sys.getfilesystemencoding()))
        sys.exit(1)
        
    # Decode the input parameters
    argvAux = []
    for argv in sys.argv[1:]:
        argvAux.append(argv.decode(sys.getfilesystemencoding(),'replace'))
        
    # Cycle through the programs to be executed
    numPipes = argvAux.count(u'///')
    currPipe = None
    popen = None
    # There should be 1 program more than pipes
    for i in range(numPipes+1):
        # Find the next pipe until no more left
        if i < numPipes:
            nPipeIdx = argvAux.index(u'///')
            procArgs = argvAux[:nPipeIdx]
        else:
            procArgs = argvAux
        # Check if the error output must be ignored
        if procArgs[0] == u'!':
            del procArgs[0]
            errorPipe = subprocess.PIPE
        # This is needed for the use of "communicate"
        elif i == numPipes:
            errorPipe = subprocess.STDOUT
        # Other errors will just be dumped to stderr
        else:
            errorPipe = None
        # Associate the current pipe with the standart input, except for the first one
        inputPipe = None
        if i > 0:
            inputPipe = currPipe
        # Execute the program and get the output pipe
        try:
            popen = subprocess.Popen(procArgs, bufsize=4096, stdin=inputPipe, stdout=subprocess.PIPE, stderr=errorPipe)
            # This is needed for the SIGPIPE signal to work properly
            if currPipe:
                currPipe.close()
            currPipe = popen.stdout
            # Close the error output to ignore it
            if procArgs[0] == u'!':
                popen.stderr.close()
        # Error handling. Terminate the running processes and exit
        except Exception, e:
            sys.stderr.write((unicode(e)).encode(sys.getfilesystemencoding()))
            sys.exit(1)
        # Remove the processed items from the list
        argvAux = argvAux[nPipeIdx+1:]
    # Get the output of the last process
    comm = popen.communicate()
    # The end
    sys.stdout.write(comm[0])
    sys.exit(popen.returncode)

if __name__ == '__main__':
    main()
    
