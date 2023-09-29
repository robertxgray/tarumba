# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         GettextLoader.py
# Purpose:      Imports and loads the gettext resources.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Globals.py $
# Copyright:    (c) 2011 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import os
import sys
import gettext

# If no env variable defined, assume that i18n files are located below the top directory
__i18n_dir = os.getenv('TARUMBA_I18N')
if not(__i18n_dir):
    __i18n_dir = os.path.join(os.path.dirname(sys.argv[0]), 'i18n')
# gettext will search in default directories if no other path given
if not os.path.isdir(__i18n_dir):
    __i18n_dir = None
                    
# Load the gettext resources
__locale_available = True
if not gettext.find('tarumba', __i18n_dir):
    __locale_available = False
    gettext.install('tarumba', __i18n_dir, unicode=True)
else:
    gettext.translation('tarumba', __i18n_dir).install(unicode=True)
    
def isLocaleAvailable():
    "Returns true if the current language is available"
    return __locale_available
