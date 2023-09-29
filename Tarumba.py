#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Boa:App:BoaApp

#----------------------------------------------------------------------------
# Name:         Tarumba.py
# Purpose:      The tarumba compressor.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Tarumba.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wxversion
wxversion.select('2.8')
import os

# Globals depends on gettext intialization
import GettextLoader
import Globals

import TextInterface

modules ={u'AlternativeDirCtrl1': [0,
                          'DirCtrl composed of a dir-tree and a file-list.',
                          u'moreControls/AlternativeDirCtrl1.py'],
 u'AlternativeTreeList1': [0,
                           u'TreeList composed of a dir-tree and a file-list.',
                           u'moreControls/AlternativeTreeList1.py'],
 u'Clipboard': [0, u"Tarumba's clipboard support.", u'Clipboard.py'],
 u'ColorLogCtrl': [0,
                   u'Shows the log of the application with colors.',
                   u'moreControls/ColorLogCtrl.py'],
 u'CompressionDialog': [0,
                        u'Shows the compression options.',
                        u'CompressionDialog.py'],
 u'CompressionManager': [0,
                         u'Manages the available compressors.',
                         u'CompressionManager.py'],
 u'Compressor': [0,
                 u'Common interface for the compressors.',
                 u'formats/Compressor.py'],
 u'ConfigurationManager': [0,
                           u'Manages the configuration variables.',
                           u'ConfigurationManager.py'],
 u'CustomProgressDialog': [0,
                           u'Custom progress dialog because original does not fit our needs.',
                           u'moreControls/CustomProgressDialog.py'],
 u'CustomTreeListCtrl': [0,
                         'Custom TreeListCtrl with additional functions.',
                         u'moreControls/CustomTreeListCtrl.py'],
 u'DecryptDialog': [0, u'Dialog used to decrypt files.', u'DecryptDialog.py'],
 u'DragNDrop': [0, u"Tarumba's drag and drop support.", u'DragNDrop.py'],
 u'DummyTreeList': [0,
                    u'TreeList data storage to use when wx.App is not available.',
                    u'moreControls/DummyTreeList.py'],
 u'Echo': [0, 'Custom echo.', u'scripts/Echo.py'],
 u'EncryptDialog': [0, u'Dialog used to encrypt files.', u'EncryptDialog.py'],
 u'Executor': [0, u'Performs the compression commands.', u'Executor.py'],
 u'FixDialog': [0, u'Tries to fix a damaged file.', u'FixDialog.py'],
 u'FixGz': [0, u'Script to fix gzip files.', u'scripts/FixGz.py'],
 u'FixTar': [0, u'Script to fix tar files', u'scripts/FixTar.py'],
 u'GettextLoader': [0,
                    u'Imports and loads the gettext resources.',
                    u'GettextLoader.py'],
 'Globals': [0, u'Global variables and constants.', u'Globals.py'],
 u'Gzip': [0, u'Gzip format support.', u'formats/Gzip.py'],
 u'JoinDialog': [0,
                 u'Can re-join chunks previously splitted.',
                 u'JoinDialog.py'],
 u'JoinZipDialog': [0,
                    u'Used to join multivolume zip files.',
                    u'JoinZipDialog.py'],
 u'MainFrame': [1, u"Tarumba's GUI.", u'MainFrame.py'],
 u'MainFrameMenu': [0,
                    u"Functions used in the main frame's menu",
                    u'MainFrameMenu.py'],
 u'MimeIcons': [0,
                u'Manages the icons shown in the TreeListCtrl.',
                u'MimeIcons.py'],
 u'MultiSelectionDirCtrl': [0,
                            u'DirCtrl that allows multiple selection.',
                            u'moreControls/MultiSelectionDirCtrl.py'],
 u'NoOutput': [0, u'Executes in silent mode.', u'scripts/NoOutput.py'],
 u'OutputTextDialog': [0,
                       u"Dialog with a TextCtrl to show program's output.",
                       u'moreControls/OutputTextDialog.py'],
 u'PathDialog': [0, u'Dialog used to configure file paths.', u'PathDialog.py'],
 u'Pipelines': [0,
                'Simulates the behaviour of pipelines without a shell.',
                u'scripts/Pipelines.py'],
 u'Rar': [0, u'Rar format support.', u'formats/Rar.py'],
 u'RenameTar': [0,
                u'Script to rename the contents in a tar file.',
                u'scripts/RenameTar.py'],
 u'RenameZip': [0,
                u'Script to rename the contents in a zip file.',
                u'scripts/RenameZip.py'],
 u'SearchTools': [0,
                  u'Provides search capabilities to the main frame.',
                  u'SearchTools.py'],
 u'SplitDialog': [0,
                  u'Dialog used to split a file into smaller volumes.',
                  u'SplitDialog.py'],
 u'StdoutToFile': [0,
                   u'Redirects the output of a program to a file.',
                   u'scripts/StdoutToFile.py'],
 u'Tar': [0, u'Tar format support.', u'formats/Tar.py'],
 u'TarGzip': [0, u'Support for the tar.gz files.', u'formats/TarGzip.py'],
 u'Temporary': [0, u'Manages the temporary files.', u'Temporary.py'],
 u'TestDialog': [0,
                 u'Can test the integrity of an compressed file.',
                 u'TestDialog.py'],
 u'TextInterface': [0,
                    u'Manages tarumba from the command line.',
                    u'TextInterface.py'],
 u'TipOfTheDay': [0, u'Random tip of the day generator.', u'TipOfTheDay.py'],
 u'Utilities': [0, u'Set of useful functions.', u'Utilities.py'],
 u'Zip': [0, u'Zip format support.', u'formats/Zip.py']}


if __name__ == '__main__':
    # Set the flag for the gettext resources availibility
    Globals.LOCALE_AVAILABLE = GettextLoader.isLocaleAvailable()
    # Start the Tarumba interface
    TextInterface.main()
    
