# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Globals.py
# Purpose:      Global variables and constants.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Globals.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import os
import wx

#################
## ESTRUCTURES ##
#################

class CompressionOptions:
    
    def __init__(self):
        self.level = None
        self.password = None
        self.volumes = None
        # Used to disable the password request when renaming files
        self.flagDisableAskPass = False

###############
## CONSTANTS ##
###############

# Tarumba's version
VERSION = 'alpha 0'

# Title used when no file is loaded
NO_FILE = _(u'<New File>')

# THE NEXT CONSTANTS ARE INIT IN BY OTHER MODULES

# Icon for the compressed file
itclFile = 0

# Flag to check if the gettext resources for the current locale are available
LOCALE_AVAILABLE = False

# Debug mode
VERBOSE = False

# Window for the program log
OUTPUT_LOG = None
# Parent for the dialogs (main frame)
PARENT = None

# Supported encryption algorithms
# IDEA and RC5 are disabled due to the license
# http://www.openssl.org/support/faq.html#LEGAL1
ALGORITHMS_ENC = ((_(u'AES 128 bits'),'-aes-128-cbc'),
                  (_(u'AES 192 bits'),'-aes-192-cbc'),
                  (_(u'AES 256 bits'),'-aes-256-cbc'),
                  (_(u'Blowfish'),    '-bf-cbc'),
                  (_(u'CAST'),        '-cast-cbc'),
                  (_(u'CAST5'),       '-cast5-cbc'),
                  (_(u'DES'),         '-des-cbc'),
                  (_(u'Triple DES'),  '-des-ede3-cbc'),
                  (_(u'DESX'),        '-desx-cbc'),
                  (_(u'RC2 40 bits'), '-rc2-40-cbc'),
                  (_(u'RC2 64 bits'), '-rc2-64-cbc')) 
# Default algorithm
ALGORITHM_ENC_DEF = 0

# Fixed input strings
INPUT_YES = _(u'YES')
INPUT_NO = _(u'NO')
INPUT_CANCEL = _(u'CANCEL')

###############
## VARIABLES ##
###############

# File in use
file = NO_FILE

# Number of elements in the file
file_num_elements = 0

# Compression options
compressionOptions = CompressionOptions()

# Disable the X interface
NOGUI = False

# Last used path (for file dialogs)
lastUsedPath = ''

###################
## CONFIGURATION ##
###################

# Configuration files
FILECONFIG = [os.path.expanduser('~/.config/tarumba/config.ini')]
# User config file
USERFILECONFIG = FILECONFIG[0]

# Temporary directory
TMPDIR = os.path.expanduser('/tmp')

# Last compressor used
lastCompressor = None

# Last external program
lastExternal = None

# Last opened files
lastOpened = None
lastOpenedList = None

# Enable beep sounds
BEEP = False

# Remember last opened files
REMEMBER_RECENTLY = True

# Follow symbolic links
FOLLOW_LINKS = False

# Do not confirm to overwrite files
NO_CONFIRM_OVERWRITE = False

# Do not ask to encrypt when adding
NO_ASK_TO_ENCRYPT = False

# Show hidden files on file system tree
SHOW_HIDDEN = False

# Show the tool bar
SHOW_TOOLBAR = True

# Show the status bar
SHOW_STATUSBAR = True

# Show the file system
SHOW_FILESYSTEM = True

# Support for alternative file-manager trees
ALTERNATIVE_TREEVIEW = True

# CAT
CAT_BIN = 'cat'
# SPLIT
SPLIT_BIN = 'split'
# GREP
GREP_BIN = 'grep'
# OPENSSL
OPENSSL_BIN = 'openssl'

# TAR
TAR_BIN = 'tar'
# GZIP
GZIP_BIN = 'gzip'
# RAR
RAR_BIN = 'rar'
# ZIP
ZIP_BIN = 'zip'
ZIPNOTE_BIN = 'zipnote'
UNZIP_BIN = 'unzip'
ZIPINFO_BIN = 'zipinfo'

import ConfigurationManager

