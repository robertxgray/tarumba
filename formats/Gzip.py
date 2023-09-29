# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Gzip.py
# Purpose:      Gzip format support.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Gzip.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

from Compressor import Compressor
import Globals
import Utilities
import Executor

import os
import tempfile
import wx.gizmos

class Gzip(Compressor): 
    
    def prepareTreeListCtrl(self, treeListCtrl):
        "Prepares the TreeListCtrl to show the contents of the file"
        treeListCtrl.AddColumn(_(u'Name'))
        treeListCtrl.AddColumn(_(u'Size'))
        treeListCtrl.AddColumn(_(u'Compressed'))
        treeListCtrl.AddColumn(_(u'Ratio'))
        treeListCtrl.AddColumn(_(u'Date'))
        treeListCtrl.AddColumn(_(u'Time'))
        treeListCtrl.AddColumn(_(u'Method'))
        treeListCtrl.AddColumn(_(u'CRC-32'))
    
    def processOutputInTreeListCtrl(self, file, output, treeListCtrl):
        "Add the contents of the compressed file to the TreeListCtrl"             
        # Declare the function to fill the other information
        def aux(items, itemAdded):
            treeListCtrl.SetItemText(itemAdded, long(items[6]), 1)
            treeListCtrl.SetItemText(itemAdded, long(items[5]), 2)
            treeListCtrl.SetItemText(itemAdded, items[7], 3)
            treeListCtrl.SetItemText(itemAdded, items[2]+' '+items[3], 4)
            treeListCtrl.SetItemText(itemAdded, items[4], 5)
            treeListCtrl.SetItemText(itemAdded, items[0], 6)
            treeListCtrl.SetItemText(itemAdded, items[1], 7)
        # Add the root of the tree
        root = treeListCtrl.AddRoot(Utilities.BasenameMod(file), 
            Globals.itclFile) 
        # Remove the header
        output = output[1:]
        # Call the auxiliar function
        Utilities.processOutputInTreeListCtrlAux(
            output, 8, treeListCtrl, root, aux)  
            
    def listCommand(self, filename):
        "Command to list the contents of the compressed file"
        text = _(u'Reading contents of the file %s') % Utilities.BasenameMod(filename)
        return [(Executor.CHDIR, [os.path.dirname(filename)], text),
            (Globals.GZIP_BIN, ['-lv','--',Utilities.BasenameMod(filename)], text)]
    
    def extractCommand(self, filename, contents):
        "Command to extract the contents from the file"
        nameAux = Utilities.WithoutExtension(Utilities.BasenameMod(filename))
        return [('StdoutToFile.py', [nameAux,Globals.GZIP_BIN,'-dqfc','--',filename], 
            _(u'Uncompressing %s') % nameAux)]
    
    def addCommand(self, filename, contents, options):
        "Command to add the contents to the file"
        # Gzip cannot compress liks
        nameAux = Utilities.BasenameMod(contents[0])
        # Get the compression level
        level = ''
        if options.level:
            level = '-' + options.level
        return [('StdoutToFile.py', [filename, Globals.GZIP_BIN, '-qcf', 
                level, '--', contents[0]], 
                _(u'Compressing %s') % nameAux)]
                
    def testCommand(self, filename):
        "Command to test the file integrity"
        return [(Globals.GZIP_BIN, ['-tv','--',filename], _(u'Testing the integrity of the file'))]
    
    def fixCommand(self, filename, newFilename):
        "Command to fix the file"
        return [('FixGz.py', [filename, newFilename], _(u'Repairing file'))]
            
    def compressionLevels(self):
        "Returns the available compression levels"
        return[ ('1 '+_(u'Minimum'), '1', False),
                ('2', '2', False),
                ('3', '3', False),
                ('4', '4', False),
                ('5', '5', False),
                ('6 '+_(u'Default'), '6', True),
                ('7', '7', False),
                ('8', '8', False),
                ('9 '+_(u'Maximum'), '9', False) ]
                
    def canCompress(self):
        "True if we can create or modify archives with this format"
        return True
    
    def canEncrypt(self):
        "True if the format allows encryption"
        return False

    def canSplit(self):
        "True if the format can be splitted into volumes"
        # Because retrieving the file information from a pipe does not work
        return False
    
    def canPack(self):
        "True if the format can store multiple files"
        return False
    
    def canRename(self):
        "True if the format can rename it's content efficiently"
        return False
    
    def canAllowFilesSameName(self):
        "True if the format can store files with the same name"
        return False
    
    def canAllowFileDirSameName(self):
        "True if the format can store files and folders with the same name"
        return False
    
    def extensions(self):
        "Returns the extensions supported by the compression format"
        return ['.gz', '-gz', '.z', '-z', '_z']
    
    def enabled(self):
        "If not enabled we can't manage files with this format"
        global ENABLED
        return (ENABLED, _(u'gzip support is disabled. ' \
            u'Check that you have gzip installed and that the path ' \
            u'for the executable is correct in the Tarumba\'s configuration.'))

    # INITIALIZATION
    def isInstalled(self):
        global ENABLED
        if Utilities.IsInstalled(Globals.GZIP_BIN):
            Utilities.Debug(_(u'Gzip found in your system, enabling gzip support.'))
            ENABLED = True
        else:
            Utilities.Debug(_(u'WARNING: Gzip not found, disabling gzip support.'))
            ENABLED = False
        
Gzip().isInstalled()
