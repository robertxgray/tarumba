# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         TarGzip.py
# Purpose:      Support for the tar.gz files.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: TarGzip.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

from Compressor import Compressor 
import Globals
import Utilities
import Executor
import Temporary
from formats.Tar import Tar
from formats.Gzip import Gzip

import os
import tempfile
import random
import wx.gizmos
import pwd
import grp

class TarGzip(Compressor): 
    
    def __init__(self):
        # Constructor Class
        self.gzip = Gzip()
        self.tar = Tar()
    
    def prepareTreeListCtrl(self, treeListCtrl):
        "Prepares the TreeListCtrl to show the contents of the file"
        treeListCtrl.AddColumn(_(u'Name'))
        treeListCtrl.AddColumn(_(u'Size'))
        # Only in root - provided by gzip - incompatible con multivolume
        if treeListCtrl.CanShowRootDetails() and (not Utilities.IsGenericMultivolume(Globals.file)):
            treeListCtrl.AddColumn(_(u'Compressed'))
            treeListCtrl.AddColumn(_(u'Ratio'))
        treeListCtrl.AddColumn(_(u'Date'))
        treeListCtrl.AddColumn(_(u'Time'))
        treeListCtrl.AddColumn(_(u'User'))
        treeListCtrl.AddColumn(_(u'Group'))
        treeListCtrl.AddColumn(_(u'Permisions'))
        # Only in root - provided by gzip - incompatible con multivolume
        if treeListCtrl.CanShowRootDetails() and (not Utilities.IsGenericMultivolume(Globals.file)):
            treeListCtrl.AddColumn(_(u'Method'))
            treeListCtrl.AddColumn(_(u'CRC-32'))
    
    def processOutputInTreeListCtrl(self, filename, output, treeListCtrl):
        "Add the contents of the compressed file to the TreeListCtrl"
        # Declare the function that fills the information - gzip version
        def aux_infogz(items, addedItem):
            treeListCtrl.SetItemText(addedItem, long(items[2]), 1)
            treeListCtrl.SetItemText(addedItem, items[3], 4)
            treeListCtrl.SetItemText(addedItem, items[4], 5)
            # Split user and group identifiers
            userId, groupId = items[1].split('/')
            # Try to resolve the user name
            try:
                user = pwd.getpwuid(int(userId)).pw_name
            except Exception, e:
                user = userId
            treeListCtrl.SetItemText(addedItem, user, 6)
            # Try to resolve the group name
            try:
                group = grp.getgrgid(int(groupId)).gr_name
            except Exception, e:
                group = groupId
            treeListCtrl.SetItemText(addedItem, group, 7)
            treeListCtrl.SetItemText(addedItem, items[0], 8)
            
        # Declare the function that fills the information - no gzip version
        def aux_noinfogz(items, addedItem):
            treeListCtrl.SetItemText(addedItem, long(items[2]), 1)
            treeListCtrl.SetItemText(addedItem, items[3], 2)
            treeListCtrl.SetItemText(addedItem, items[4], 3)
            # Split user and group identifiers
            userId, groupId = items[1].split('/')
            # Try to resolve the user name
            try:
                user = pwd.getpwuid(int(userId)).pw_name
            except Exception, e:
                user = userId
            treeListCtrl.SetItemText(addedItem, user, 4)
            # Try to resolve the group name
            try:
                group = grp.getgrgid(int(groupId)).gr_name
            except Exception, e:
                group = groupId
            treeListCtrl.SetItemText(addedItem, group, 5)
            treeListCtrl.SetItemText(addedItem, items[0], 6)

        # Add the root of the tree
        root = treeListCtrl.AddRoot(Utilities.BasenameMod(filename), 
            Globals.itclFile) 
        # Add the aditional info provided by gzip - incompatible con multivolumes
        if treeListCtrl.CanShowRootDetails() and (not Utilities.IsGenericMultivolume(filename)):
            infoGz = self.infoCompressionGzip(filename)
            treeListCtrl.SetItemText(root, infoGz[0], 9)
            treeListCtrl.SetItemText(root, infoGz[1], 10)
            treeListCtrl.SetItemText(root, long(infoGz[5]), 2)
            treeListCtrl.SetItemText(root, infoGz[6], 1)
            treeListCtrl.SetItemText(root, infoGz[7], 3)
            
        # Call to the auxiliary function
        if treeListCtrl.CanShowRootDetails() and (not Utilities.IsGenericMultivolume(filename)):
            Utilities.processOutputInTreeListCtrlAux(
                output, 5, treeListCtrl, root, aux_infogz)
        else:
            Utilities.processOutputInTreeListCtrlAux(
                output, 5, treeListCtrl, root, aux_noinfogz)
            
    def listCommand(self, filename):
        "Command to list the contents of the compressed file"
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:
            # Numeric owner to avoid problems with odd user and group names
            return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                ['///', Globals.TAR_BIN, '--numeric-owner', '-ztv'],
                _(u'Reading contents of the file %s') % Utilities.BasenameMod(filename))]
        else:
            # Numeric owner to avoid groups with spaces
            return [(Globals.TAR_BIN, ['--numeric-owner',
                '-ztvf',filename], _(u'Reading contents ' \
                u'of the file %s') % Utilities.BasenameMod(filename))]
    
    def extractCommand(self, filename, contents):
        "Command to extract the contents from the file"
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:
            # When extracting a single file, include it's ocurrence
            if len(contents) == 1:
                return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                    ['///', Globals.TAR_BIN, '-zxv', '--occurrence='+`contents[0][1]`, '--',
                     contents[0][0]], _(u'Uncompressing %s')%Utilities.BasenameMod(filename))]
            # Ocurrence does not apply for full directories becase we cannot
            # extract multiple files with the same name anyway
            else:
                baseNameCon=[]
                for con in contents:
                    baseNameCon.append(con[0])
                return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                    ['///', Globals.TAR_BIN, '-zxv', '--'] + baseNameCon, 
                    _(u'Uncompressing %s') % Utilities.BasenameMod(filename))]
        else:
            # When extracting a single file, include it's ocurrence
            if len(contents) == 1:
                return [(Globals.TAR_BIN, ['-zxvf', filename, '--occurrence='+`contents[0][1]`, '--',
                    contents[0][0]], _(u'Uncompressing %s')%Utilities.BasenameMod(filename))]
            # Ocurrence does not apply for full directories becase we cannot
            # extract multiple files with the same name anyway
            else:
                baseNameCon=[]
                for con in contents:
                    baseNameCon.append(con[0])
                return [(Globals.TAR_BIN, ['-zxvf', filename, '--'] + baseNameCon, 
                    _(u'Uncompressing %s') % Utilities.BasenameMod(filename))]
                
    def extractCommandParseOutput(self, text=''):
        "How to parse one line of programs output when extracting"
        if text:
            return (1, _('Extracting %s') % Utilities.BasenameMod(text))
        else:
            return (0, '')
        
    def addCommand(self, filename, contents, options):
        "Command to add the contents to the file"
        # Only works for new files, see "add" for details
        
        # Get the compression level
        level = ''
        if options.level:
            level = '-' + options.level
        # Parameters to follow or not follow symbolic links
        if Globals.FOLLOW_LINKS:
            params = '-ch'
        else:
            params = '-c'
        # Check for multivolumes
        if options.volumes:
            # Converto kilobytes to bytes
            size = str(int(options.volumes) * 1024)
            return [('Pipelines.py', [Globals.TAR_BIN, params, '--'] + contents +
                ['///', Globals.GZIP_BIN, '-qcf', level, 
                 '///' ,Globals.SPLIT_BIN,'--verbose','-d','-b',size,'-a','3','-',filename+'.'], 
                _(u'Packing %s') % Utilities.BasenameMod(filename)),
                # Tell the user when the process is finished
                ('Echo.py', [_(u'Done.')], 
                _(u'Compressing %s') % Utilities.BasenameMod(filename))]
        else:
            return [('StdoutToFile.py', [filename, 'Pipelines.py', Globals.TAR_BIN, params, '--'] + 
                contents + ['///', Globals.GZIP_BIN, '-qcf', level], 
                _(u'Compressing %s') % Utilities.BasenameMod(filename))]
                
    def testCommand(self, filename):
        "Command to test the file integrity"
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:
            return [('Echo.py', [_(u'Testing %s... ') % filename], _(u'Testing the integrity of the file')),
                ('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                ['///', Globals.GZIP_BIN, '-tv'], _(u'Testing the integrity of the file'))]
        else:
            return [(Globals.GZIP_BIN, ['-tv','--',filename], _(u'Testing the integrity of the file'))]
    
    def fixCommand(self, filename, newFilename):
        "Command to fix the file"
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:          
            return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                ['///', 'FixGz.py', newFilename], _(u'Repairing file'))]
        else:
            return [('FixGz.py', [filename, newFilename], _(u'Repairing file'))]
        
    def compressionLevels(self):
        "Returns the available compression levels"
        return self.gzip.compressionLevels()
                
    def canCompress(self):
        "True if we can create or modify archives with this format"
        return True
    
    def canEncrypt(self):
        "True if the format allows encryption"
        return False

    def canSplit(self):
        "True if the format can be splitted into volumes"
        return True
    
    def canPack(self):
        "True if the format can store multiple files"
        return True
    
    def canRename(self):
        "True if the format can rename it's content efficiently"
        return True
    
    def canAllowFilesSameName(self):
        "True if the format can store files with the same name"
        return True
    
    def canAllowFileDirSameName(self):
        "True if the format can store files and folders with the same name"
        return True
    
    def extensions(self):
        "Returns the extensions supported by the compression format"
        return ['.tar.gz', '.tgz']
    
    def infoCompressionGzip(self, filename):
        "Get the file information provided by gzip"
        command = [(Globals.GZIP_BIN, ['-lv','--',filename], 
            _(u'Reading contents of the file'))]
        error, output = Executor.execute(command)
        return output[1].split()
    
    def add (self, filename, contents, path, options, execFunction=Executor.execute):
        "Adds the contents to the current compressed file"
        # Creating a new file - mandatory for multivolume
        if not os.path.lexists(filename) or options.volumes:
            return Compressor.add(self, filename, contents, path, options, execFunction)
        # Updating an existing file
        else:
            try:
                # Tar file without compression
                tmpAux = Utilities.WithoutExtension(filename)
                tmpDir = Temporary.tmpDir()
                tmpFile = os.path.join(tmpDir, Utilities.BasenameMod(tmpAux))
                if not tmpFile.upper().endswith('.TAR'):
                    tmpFile += '.tar'
                # Decompress the file 
                self.gzip.extract(filename, [[(Utilities.BasenameMod(tmpFile),1,True)]], tmpDir)
                # Add the contents to the temporary tar
                error, output = self.tar.add(tmpFile, contents, path, options)
                # Compress it with gzip again
                Utilities.DeleteFile(filename)
                self.gzip.add(filename, [[tmpFile]], './', options)
            finally:
                # Destroy the temporary folder
                Utilities.DeleteFile(tmpDir)
            return error, output
        
    def delete (self, filename, contents, options, execFunction=Executor.execute):
        "Deletes the contents from the current compressed file"
        try:
            # Tar file without compression
            tmpAux = Utilities.WithoutExtension(filename)
            tmpDir = Temporary.tmpDir()
            tmpFile = os.path.join(tmpDir, Utilities.BasenameMod(tmpAux))
            if not tmpFile.upper().endswith('.TAR'):
                tmpFile += '.tar'
            # Decompress the file
            self.gzip.extract(
                filename, [[(Utilities.BasenameMod(tmpFile),1,True)]], tmpDir)
            # Delete the contents from the tar file
            error, output = self.tar.delete(tmpFile, contents, options)
            # Compress it with gzip again
            Utilities.DeleteFile(filename)
            self.gzip.add(filename, [[tmpFile]], './', options)
        finally:
            # Destroy the temporary folder
            Utilities.DeleteFile(tmpDir)
        return error, output
    
    def rename (self, filename, contents, newname, options, execFunction=Executor.execute):
        "Renames the content to the newname"
        try:
            # Tar file without compression
            tmpAux = Utilities.WithoutExtension(filename)
            tmpDir = Temporary.tmpDir()
            tmpFile = os.path.join(tmpDir, Utilities.BasenameMod(tmpAux))
            if not tmpFile.upper().endswith('.TAR'):
                tmpFile += '.tar'
            # Decompress the file
            self.gzip.extract(
                filename, [[(Utilities.BasenameMod(tmpFile),1,True)]], tmpDir)
            # Delete the contents from the tar file
            error, output = self.tar.rename(tmpFile, contents, newname, options)
            # Compress it with gzip again
            Utilities.DeleteFile(filename)
            self.gzip.add(filename, [[tmpFile]], './', options)
        finally:
            # Destroy the temporary folder
            Utilities.DeleteFile(tmpDir)
        return error, output
    
    def enabled(self):
        "If not enabled we can't manage files with this format"
        tarEnabled = self.tar.enabled()
        gzipEnabled = self.tar.enabled()
        if not tarEnabled[0]:
            return tarEnabled
        if not gzipEnabled[0]:
            return gzipEnabled
        return (True,'')
            
