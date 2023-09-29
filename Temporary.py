# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Temporary.py
# Purpose:      Manages the temporary files.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Temporary.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities

import os
import sys
import random

# Current temporary folder. Initialized via createTmp()
__TMPDIR = None

def RandomName():
    "Returns a random-generated string"
    characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
                    'o','p','q','r','s','t','u','v','w','x','y','z',
                    'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                    'O','P','Q','R','S','T','U','V','W','X','Y','Z',
                    '1','2','3','4','5','6','7','8','9','0','_']
    name = ''
    for i in range(10):
        name += random.choice(characters) 
    return name  
                       
def DeleteTemporaryFolder(top):
    "Function used to empty the temporary folder"
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def tmpFile():
    "Returns a file name that can be used as a temporary file"
    global __TMPDIR
    continues = True
    while continues:
        file = os.path.join(__TMPDIR, RandomName())
        if not os.path.lexists(file):
            continues = False
    return file

def tmpDir():
    "Returns the name of an existing temporary folder"
    global __TMPDIR
    continues = True
    while continues:
        name = os.path.join(__TMPDIR, RandomName())
        if not os.path.lexists(name):
            continues = False
    os.mkdir(name)
    return name

def getFileSysOf(path):
    "Returns the file system where the path is stored"
    aux = os.open(path,os.O_RDONLY)
    fileSys = os.fstat(aux)[2]
    os.close(aux)
    return fileSys

def tmpDirInFilesys(path):
    "Returns the name of a temporary folder in the same file system"
    global __TMPDIR
    # The folder separator at the end of the paths can cause problems
    if path[-1] == '/':
        path = path[:-1]
    # Get the file systems
    fileSysPath = getFileSysOf(path)
    fileSysTmp = getFileSysOf(__TMPDIR)
    # If it's the same, we can use the temporary
    if fileSysPath == fileSysTmp:
        return (tmpDir(), True)
    # Otherwise try to use a hidden temporary in the same path
    else:
        try:
            parent = os.path.dirname(path)
            fileSysParent = getFileSysOf(parent)
            # Surrender if we can't go up one level
            if fileSysParent != fileSysPath:
                raise OSError()
            dirTmpAux = os.path.join(parent, '.tar' + RandomName())
            Utilities.CreateFolder(dirTmpAux)
            return (dirTmpAux, True)
        # If we can't do it, use the temporary but notice it with the "False"
        except OSError, e:
            return (tmpDir(), False)

def deleteTmp():
    "Destroy the temporary folder"
    global __TMPDIR
    Utilities.DeleteFile(__TMPDIR)

def createTmp():
    "Prepare the temporary folder"
    global __TMPDIR
    # Temporary folder
    tmpDirAux = Globals.TMPDIR
    # Create a random folder name in the temporary folder
    name = ''
    # Repeat until find name that doesn't exists  
    continues = True
    while continues:
        name = os.path.join(tmpDirAux, '_tar' + RandomName())
        if not os.path.lexists(name):
            continues = False
    __TMPDIR = name
    Utilities.CreateFolder(__TMPDIR)
    DeleteTemporaryFolder(__TMPDIR)
