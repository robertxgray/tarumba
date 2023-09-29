#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Echo.py
# Purpose:      Custom echo.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Echo.py $
# Copyright:    (c) 2012 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# This isn't very useful for now, but it allows us to avoid checking echo's availability
# and it could be improved with more functionality if needed

import sys

def main():
    "Custom echo."
    
    nargv = len(sys.argv)
    idx = 1
    while idx < nargv:
        sys.stdout.write((sys.argv[idx]+"\n").encode(sys.getfilesystemencoding()))
        idx += 1
        
    sys.exit(0)

if __name__ == '__main__':
    main()
    
