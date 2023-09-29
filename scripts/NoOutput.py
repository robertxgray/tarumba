#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         NoOutput.py
# Purpose:      Executes in silent mode.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: NoOutput.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import sys
import subprocess

def main():
    "Executes a command in silent mode."

    # Exit if no parameters found
    if len(sys.argv) < 1:
        sys.exit(0)
        
    # Decode the input parameters
    argvAux = []
    for argv in sys.argv:
        argvAux.append(argv.decode(sys.getfilesystemencoding(),'replace'))

    # Execute the given command
    try:
        subprocess.Popen(argvAux[1:], stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    except Exception, e:
        pass
        
    sys.exit(0)

if __name__ == '__main__':
    main()
    
