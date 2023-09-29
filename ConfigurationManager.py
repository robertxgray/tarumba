# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         ConfigurationManager.py
# Purpose:      Manages the configuration variables.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: ConfigurationManager.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities

import ConfigParser
import os

# Private configuration manager
__cp = ConfigParser.SafeConfigParser()

###############
## FUNCTIONS ##
###############

def saveConfig():
    "Stores the configuration in disk"
    try:
        Utilities.CreateFolder(os.path.dirname(Globals.USERFILECONFIG))
        userConfig = open(Globals.USERFILECONFIG,'w')
        __cp.write(userConfig)
        userConfig.close()
    # If it fails, we only show a warning (no fatal)
    except Exception, e:
        Utilities.Log(_(u'Can\'t save user configuration:') + ' ' \
            '' + unicode(e), Utilities.ERRO)
            
def saveValue(variable, value):
    "Updates a configuration value in disk"
    # We need to encode the value to avoid an enconding error
    __cp.set('ALL',variable,Utilities.Encode(value))
    saveConfig()

####################
## INITIALIZATION ##
####################

# Read the configuration file
__cp.read(Globals.FILECONFIG)
    
# If it does not exists we create it, there is only one for now
if not __cp.has_section('ALL'):
    __cp.add_section('ALL')
    
# Temporary directory
if __cp.has_option('ALL', 'TMPDIR'):
    Globals.TMPDIR = Utilities.Decode(__cp.get('ALL','TMPDIR'))
if Globals.TMPDIR:
    __cp.set('ALL','TMPDIR',Utilities.Encode(Globals.TMPDIR))

# Follow symbolic links
if __cp.has_option('ALL', 'FOLLOW_LINKS'):
    Globals.FOLLOW_LINKS = __cp.getboolean('ALL','FOLLOW_LINKS')
if Globals.FOLLOW_LINKS:
    __cp.set('ALL','FOLLOW_LINKS',str(Globals.FOLLOW_LINKS))

# Last compressor used
if __cp.has_option('ALL', 'LAST_COMPRESSOR'):
    Globals.lastCompressor = Utilities.Decode(__cp.get('ALL','LAST_COMPRESSOR'))
if Globals.lastCompressor:
    __cp.set('ALL','LAST_COMPRESSOR',Utilities.Encode(Globals.lastCompressor))

# Last opened files
if __cp.has_option('ALL', 'LAST_OPENED'):
    Globals.lastOpened = Utilities.Decode(__cp.get('ALL','LAST_OPENED'))
if Globals.lastOpened:
    __cp.set('ALL','LAST_OPENED',Utilities.Encode(Globals.lastOpened))

# Last external program used
if __cp.has_option('ALL', 'LAST_EXTERNAL'):
    Globals.lastExternal = Utilities.Decode(__cp.get('ALL','LAST_EXTERNAL'))
if Globals.lastExternal:
    __cp.set('ALL','LAST_EXTERNAL',Utilities.Encode(Globals.lastExternal))

# Beep when execution finished
if __cp.has_option('ALL', 'BEEP'):
    Globals.BEEP = __cp.getboolean('ALL','BEEP')
if Globals.BEEP:
    __cp.set('ALL','BEEP',str(Globals.BEEP))
    
# Remember recently opened files
if __cp.has_option('ALL', 'REMEMBER_RECENTLY'):
    Globals.REMEMBER_RECENTLY = __cp.getboolean('ALL','REMEMBER_RECENTLY')
if Globals.REMEMBER_RECENTLY:
    __cp.set('ALL','REMEMBER_RECENTLY',str(Globals.REMEMBER_RECENTLY))
    
# Show hidden files on file system tree
if __cp.has_option('ALL', 'SHOW_HIDDEN'):
    Globals.SHOW_HIDDEN = __cp.getboolean('ALL','SHOW_HIDDEN')
if Globals.SHOW_HIDDEN:
    __cp.set('ALL','SHOW_HIDDEN',str(Globals.SHOW_HIDDEN))
    
# Show or hide the tool bar
if __cp.has_option('ALL', 'SHOW_TOOLBAR'):
    Globals.SHOW_TOOLBAR = __cp.getboolean('ALL','SHOW_TOOLBAR')
if Globals.SHOW_TOOLBAR:
    __cp.set('ALL','SHOW_TOOLBAR',str(Globals.SHOW_TOOLBAR))
    
# Show or hide the status bar
if __cp.has_option('ALL', 'SHOW_STATUSBAR'):
    Globals.SHOW_STATUSBAR = __cp.getboolean('ALL','SHOW_STATUSBAR')
if Globals.SHOW_STATUSBAR:
    __cp.set('ALL','SHOW_STATUSBAR',str(Globals.SHOW_STATUSBAR))
    
# Show or hide the file system
if __cp.has_option('ALL', 'SHOW_FILESYSTEM'):
    Globals.SHOW_FILESYSTEM = __cp.getboolean('ALL','SHOW_FILESYSTEM')
if Globals.SHOW_FILESYSTEM:
    __cp.set('ALL','SHOW_FILESYSTEM',str(Globals.SHOW_FILESYSTEM))
    
# Change the file-view mode
if __cp.has_option('ALL', 'ALTERNATIVE_TREEVIEW'):
    Globals.ALTERNATIVE_TREEVIEW = __cp.getboolean('ALL','ALTERNATIVE_TREEVIEW')
if Globals.ALTERNATIVE_TREEVIEW:
    __cp.set('ALL','ALTERNATIVE_TREEVIEW',str(Globals.ALTERNATIVE_TREEVIEW))

# Do not confirm to overwrite files
if __cp.has_option('ALL', 'NO_CONFIRM_OVERWRITE'):
    Globals.NO_CONFIRM_OVERWRITE = __cp.getboolean('ALL','NO_CONFIRM_OVERWRITE')
if Globals.NO_CONFIRM_OVERWRITE:
    __cp.set('ALL','NO_CONFIRM_OVERWRITE',str(Globals.NO_CONFIRM_OVERWRITE))
    
# Do not ask to encrypt when adding
if __cp.has_option('ALL', 'NO_ASK_TO_ENCRYPT'):
    Globals.NO_ASK_TO_ENCRYPT = __cp.getboolean('ALL','NO_ASK_TO_ENCRYPT')
if Globals.NO_ASK_TO_ENCRYPT:
    __cp.set('ALL','NO_ASK_TO_ENCRYPT',str(Globals.NO_ASK_TO_ENCRYPT))

# CAT
if __cp.has_option('ALL', 'CAT_BIN'):
    Globals.CAT_BIN = Utilities.Decode(__cp.get('ALL','CAT_BIN'))
if Globals.CAT_BIN:
    __cp.set('ALL','CAT_BIN',Utilities.Encode(Globals.CAT_BIN))
    
# SPLIT
if __cp.has_option('ALL', 'SPLIT_BIN'):
    Globals.SPLIT_BIN = Utilities.Decode(__cp.get('ALL','SPLIT_BIN'))
if Globals.SPLIT_BIN:
    __cp.set('ALL','SPLIT_BIN',Utilities.Encode(Globals.SPLIT_BIN))
    
# GREP
if __cp.has_option('ALL', 'GREP_BIN'):
    Globals.GREP_BIN = Utilities.Decode(__cp.get('ALL','GREP_BIN'))
if Globals.GREP_BIN:
    __cp.set('ALL','GREP_BIN',Utilities.Encode(Globals.GREP_BIN))
    
# OPENSSL
if __cp.has_option('ALL', 'OPENSSL_BIN'):
    Globals.OPENSSL_BIN = Utilities.Decode(__cp.get('ALL','OPENSSL_BIN'))
if Globals.OPENSSL_BIN:
    __cp.set('ALL','OPENSSL_BIN',Utilities.Encode(Globals.OPENSSL_BIN))

# TAR
if __cp.has_option('ALL', 'TAR_BIN'):
    Globals.TAR_BIN = Utilities.Decode(__cp.get('ALL','TAR_BIN'))
if Globals.TAR_BIN:
    __cp.set('ALL','TAR_BIN',Utilities.Encode(Globals.TAR_BIN))

# GZIP
if __cp.has_option('ALL', 'GZIP_BIN'):
    Globals.GZIP_BIN = Utilities.Decode(__cp.get('ALL','GZIP_BIN'))
if Globals.GZIP_BIN:
    __cp.set('ALL','GZIP_BIN',Utilities.Encode(Globals.GZIP_BIN))

# RAR
if __cp.has_option('ALL', 'RAR_BIN'):
    Globals.RAR_BIN = Utilities.Decode(__cp.get('ALL','RAR_BIN'))
if Globals.RAR_BIN:
    __cp.set('ALL','RAR_BIN',Utilities.Encode(Globals.RAR_BIN))

# ZIP
if __cp.has_option('ALL', 'ZIP_BIN'):
    Globals.ZIP_BIN = Utilities.Decode(__cp.get('ALL','ZIP_BIN'))
if Globals.ZIP_BIN:
    __cp.set('ALL','ZIP_BIN',Utilities.Encode(Globals.ZIP_BIN))
    
if __cp.has_option('ALL', 'ZIPNOTE_BIN'):
    Globals.ZIPNOTE_BIN = Utilities.Decode(__cp.get('ALL','ZIPNOTE_BIN'))
if Globals.ZIPNOTE_BIN:
    __cp.set('ALL','ZIPNOTE_BIN',Utilities.Encode(Globals.ZIPNOTE_BIN))

if __cp.has_option('ALL', 'UNZIP_BIN'):
    Globals.UNZIP_BIN = Utilities.Decode(__cp.get('ALL','UNZIP_BIN'))
if Globals.UNZIP_BIN:
    __cp.set('ALL','UNZIP_BIN',Utilities.Encode(Globals.UNZIP_BIN))

if __cp.has_option('ALL', 'ZIPINFO_BIN'):
    Globals.ZIPINFO_BIN = Utilities.Decode(__cp.get('ALL','ZIPINFO_BIN'))
if Globals.ZIPINFO_BIN:
    __cp.set('ALL','ZIPINFO_BIN',Utilities.Encode(Globals.ZIPINFO_BIN))

# Store the configuration
saveConfig()
