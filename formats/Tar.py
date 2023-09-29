# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Tar.py
# Purpose:      Tar format support.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Tar.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

from Compressor import Compressor
import Globals
import Utilities
import Executor

import os
import os.path
import wx.gizmos
import pwd
import grp

class Tar(Compressor):
    
    def prepareTreeListCtrl(self, treeListCtrl):
        "Prepares the TreeListCtrl to show the contents of the file"
        treeListCtrl.AddColumn(_(u'Name'))
        treeListCtrl.AddColumn(_(u'Size'))
        treeListCtrl.AddColumn(_(u'Date'))
        treeListCtrl.AddColumn(_(u'Time'))
        treeListCtrl.AddColumn(_(u'User'))
        treeListCtrl.AddColumn(_(u'Group'))
        treeListCtrl.AddColumn(_(u'Permissions'))
    
    def processOutputInTreeListCtrl(self, filename, output, treeListCtrl):
        "Add the contents of the compressed file to the TreeListCtrl"            
        # Declare the function that fills the information
        def aux(items, addedItem):
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
        root = treeListCtrl.AddRoot(Utilities.BasenameMod(filename), Globals.itclFile)
        # Call the auxiliary function
        Utilities.processOutputInTreeListCtrlAux(output, 5, treeListCtrl, root, aux)
            
    def listCommand(self, filename):
        "Command to list the contents of the compressed file"
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:
            # Numeric owner to avoid problems with odd user and group names
            return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                ['///', Globals.TAR_BIN, '--numeric-owner', '-tv'],
                _(u'Reading contents of the file %s') % Utilities.BasenameMod(filename))]
        else:
            # Numeric owner to avoid problems with odd user and group names
            return [(Globals.TAR_BIN, ['--numeric-owner',
                '-tvf',filename], _(u'Reading contents ' \
                u'of the file %s') % Utilities.BasenameMod(filename))]
    
    def extractCommand(self, filename, contents):
        "Command to extract the contents from the file"
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:
            # When extracting a single file, include it's ocurrence
            if len(contents) == 1:
                return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                    ['///', Globals.TAR_BIN, '-xv', '--occurrence='+`contents[0][1]`, '--',
                     contents[0][0]], _(u'Unpacking %s')%Utilities.BasenameMod(filename))]
            # Ocurrence does not apply for full directories becase we cannot
            # extract multiple files with the same name anyway
            else:
                baseNameCon=[]
                for con in contents:
                    baseNameCon.append(con[0])
                return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                    ['///', Globals.TAR_BIN, '-xv', '--'] + baseNameCon, 
                    _(u'Unpacking %s') % Utilities.BasenameMod(filename))]
        else:
            # When extracting a single file, include it's ocurrence
            if len(contents) == 1:
                return [(Globals.TAR_BIN, ['-xvf', filename, '--occurrence='+`contents[0][1]`, '--',
                    contents[0][0]], _(u'Unpacking %s')%Utilities.BasenameMod(filename))]
            # Ocurrence does not apply for full directories becase we cannot
            # extract multiple files with the same name anyway
            else:
                baseNameCon=[]
                for con in contents:
                    baseNameCon.append(con[0])
                return [(Globals.TAR_BIN, ['-xvf', filename, '--'] + baseNameCon, 
                    _(u'Unpacking %s') % Utilities.BasenameMod(filename))]
            
    def extractCommandParseOutput(self, text=''):
        "How to parse one line of programs output when extracting"
        if text:
            return (1, _('Extracting %s') % Utilities.BasenameMod(text))
        else:
            return (0, '')
    
    def addCommand(self, filename, contents, options):
        "Command to add the contents to the file"
        # Check for multivolumes
        if options.volumes:
            # Converto kilobytes to bytes
            size = str(int(options.volumes) * 1024)
            # Parameters to follow or not follow symbolic links
            if Globals.FOLLOW_LINKS:
                params = '-ch'
            else:
                params = '-c'
            return [('Pipelines.py', [Globals.TAR_BIN, params, '--'] + contents +
                ['///',Globals.SPLIT_BIN,'--verbose','-d','-b',size,'-a','3','-',filename+'.'], 
                _(u'Packing %s') % Utilities.BasenameMod(filename)),
                # Tell the user when the process is finished
                ('Echo.py', [_(u'Done.')], 
                _(u'Packing %s') % Utilities.BasenameMod(filename))]
        else:
            # Parameters to follow or not follow symbolic links
            if Globals.FOLLOW_LINKS:
                params = '-rvhf'
            else:
                params = '-rvf'
            return [(Globals.TAR_BIN, [params, filename, '--'] + contents, 
                _(u'Packing %s') % Utilities.BasenameMod(filename))]
            
    def addCommandParseOutput(self, text=''):
        "How to parse one line of programs output when adding"
        if text:
            return (1, _('Adding %s') % Utilities.BasenameMod(text))
        else:
            return (0, '')
    
    def deleteCommand(self, filename, contents, options):
        "Command to delete the contents from the file"
        # When deleting a single file, include it's ocurrence
        if len(contents) == 1:
            return [(Globals.TAR_BIN,
                ['--delete', '-vf', filename, '--occurrence='+`contents[0][1]`,
                 '--', contents[0][0]],
                 _(u'Deleting contents from %s')%Utilities.BasenameMod(filename))]
        # Ocurrence does not apply for full directories becase we always
        # want to delete all of them
        else:
            baseNameCon=[]
            for con in contents:
                baseNameCon.append(con[0])
            return [(Globals.TAR_BIN,
                ['--delete', '-vf', filename, '--'] + baseNameCon, 
                _(u'Deleting contents from %s')%Utilities.BasenameMod(filename))]
                
    def renameCommand(self, filename, contents, newname, options):
        "Command to rename the contents of the file"
        return [('RenameTar.py',
            [filename, contents[0][0], str(contents[0][1]), newname],
             _(u'Renaming %(oldname)s to %(newname)s')
                % {'oldname':contents[0][0], 'newname':newname})]
    
    def testCommand(self, filename):
        "Command to test the file integrity"
        # Like list but more verbose? there should be something better...
        
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:
            # Numeric owner to avoid problems with odd user and group names
            return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                ['///', Globals.TAR_BIN, '--numeric-owner', '-tvv'],
                _(u'Testing the integrity of the file'))]
        else:
            # Numeric owner to avoid problems with odd user and group names
            return [(Globals.TAR_BIN, ['--numeric-owner', '-tvvf', filename],
                _(u'Testing the integrity of the file'))]
    
    def fixCommand(self, filename, newFilename):
        "Command to fix the file"
        # Check for multivolume
        volumes = Utilities.GetGenericVolumes(filename)
        if volumes:
            # When only one file is given, FixTar reads from stdin
            return [('Pipelines.py', ['!', Globals.CAT_BIN] + volumes + 
                ['///', 'FixTar.py', newFilename], _(u'Repairing file'))]
        else:
            # When 2 files are give, FixTar uses them as input-output
            return [('FixTar.py', [filename, newFilename], _(u'Repairing file'))]
        
    def compressionLevels(self):
        "Returns the available compression levels"
        return[(_(u'None'),'',True)]
    
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
        return ['.tar']

    def enabled(self):
        "If not enabled we can't manage files with this format"
        global ENABLED
        return (ENABLED, _(u'Tar support is unavailable. ' \
            u'Check that tar is installed and that the tar\'s binary path ' 
            u'configured in Tarumba is correct.'))
            
    def rename(self, filename, contents, newname, options, execFunction=Executor.execute, env=None):
        "Renames the content to the newname"
        # This function is redefined to avoid dealing with filenames longer than 100
        
        oldname = contents[0][0]
        # Process every content
        for con in contents:
            name = con[0]
            if len(name) > 100:
                return (1, _(u'The renaming operation cannot be performed because %s is ' \
                    'longer than 100 characters.\nThis limitation is particular to the ' \
                    'tar format.') % name)
            # Check if the content must be renamed
            rename = False
            # Oldname is a directory
            if oldname[-1] == '/':
                if name.startswith(oldname):
                    rename = True
            # Oldname is a file
            else:
                if name == oldname:
                    rename = True
            
            # Perform the renaming operation
            if rename:
                # Get the name of the renamed content
                nameAux = name.replace(oldname, newname, 1)
                if len(nameAux) > 100:
                    return (1, _(u'The renaming operation cannot be performed because %s is ' \
                        'longer than 100 characters.\nThis limitation is particular to the ' \
                        'tar format.') % nameAux)
        
        return Compressor.rename(self, filename, contents, newname, options, execFunction)
            
    # INITIALIZATION
    def isInstalled(self):
        global ENABLED
        if Utilities.IsInstalled(Globals.TAR_BIN):
            Utilities.Debug(_(u'Tar found in your system, tar support enabled.'))
            ENABLED = True
        else:
            Utilities.Debug(_(u'WARNING: Tar not found, tar support disabled.'))
            ENABLED = False
        
Tar().isInstalled()
