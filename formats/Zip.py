# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Zip.py
# Purpose:      Zip format support.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Zip.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

# IMPORTANT: In my tests, I found Info-Zip does not handle non-ASCII characters
# properly when locale is set to UTF-8. The locale will be changed to LATIN1
# before executing any utility from Info-Zip

from Compressor import Compressor
import Globals
import Utilities
import Executor
import Temporary

import os
import os.path
import wx.gizmos
import locale

class Zip(Compressor):
    
    def prepareTreeListCtrl(self, treeListCtrl):
        "Prepares the TreeListCtrl to show the contents of the file"
        treeListCtrl.AddColumn(_(u'Name'))
        treeListCtrl.AddColumn(_(u'Size'))
        treeListCtrl.AddColumn(_(u'Compressed'))
        treeListCtrl.AddColumn(_(u'Method'))
        treeListCtrl.AddColumn(_(u'Date'))
        treeListCtrl.AddColumn(_(u'Time'))
        treeListCtrl.AddColumn(_(u'Permisions'))
        treeListCtrl.AddColumn(_(u'Version'))
    
    def processOutputInTreeListCtrl(self, filename, output, treeListCtrl):
        "Add the contents of the compressed file to the TreeListCtrl"            
        # Declare the function that fills the information
        def aux(items, addedItem):
            treeListCtrl.SetItemText(addedItem, long(items[3]), 1)
            treeListCtrl.SetItemText(addedItem, long(items[5]), 2)
            treeListCtrl.SetItemText(addedItem, items[6], 3)
            treeListCtrl.SetItemText(addedItem, items[7], 4)
            treeListCtrl.SetItemText(addedItem, items[8], 5)
            treeListCtrl.SetItemText(addedItem, items[0], 6)
            treeListCtrl.SetItemText(addedItem, items[1]+' '+items[2], 7)
        # Add the root of the tree
        root = treeListCtrl.AddRoot(Utilities.BasenameMod(filename), 
            Globals.itclFile) 
        # Call the auxiliary function
        Utilities.processOutputInTreeListCtrlAux(
            output, 9, treeListCtrl, root, aux)     
            
    def listCommand(self, filename):
        "Command to list the contents of the compressed file"
        # unzip -lv is not used to avoid the comments
        return [(Globals.ZIPINFO_BIN, ['-l','--h-t',filename], _(u'Reading' \
            u' contents of the file %s') % Utilities.BasenameMod(filename))]
    
    def extractCommand(self, filename, contents):
        "Command to extract the contents from the file"
        baseNameCon=[]
        for con in contents:
			baseNameCon.append(con[0])
        # Warning: zip goes crazy when receiving empty parameters
        return [(Globals.UNZIP_BIN, ['-o','--',filename] + baseNameCon, 
                _(u'Uncompressing %s') % Utilities.BasenameMod(filename))]
                
    def extractCommandParseOutput(self, text=''):
        "How to parse one line of programs output when extracting"
        # Messages got during decompression
        if (text and (len(text)>13) and (text[11:13]==': ')):
            return (1, _('Extracting %s') % Utilities.BasenameMod(text[13:]))
        # Messages got during multivolume join
        if (text and (len(text)>10) and (text[8:10]==': ')):
            return (1, _('Reading from volumes: %s') % Utilities.BasenameMod(text[10:]))
        
        return (0, '')
    
    def addCommand(self, filename, contents, options):
        "Command to add the contents to the file"
        output = []
        # Parameters to follow or not follow symbolic links
        if Globals.FOLLOW_LINKS:
            params = ['-r']
        else:
            params = ['-ry']
        # If encryption is requested add the -e option
        if options.password:
            params.append('-e')
        # Add also the compression level
        if options.level:
            params.append('-'+options.level)
        # Multivolume support - only works with zip >= 3.0
        if options.volumes:
            params.append('-sv')
            params.append('-s')
            params.append(options.volumes+'k')
            # Use grep to filter split-related messages only
            return[('Pipelines.py', [Globals.ZIP_BIN]+params+[filename,'--']+ contents +
                ['///', Globals.GREP_BIN, '-v', '^  adding: '],
                _(u'Compressing %s') % Utilities.BasenameMod(filename)),
                # The first text is not translated to look like the zip's output
                ('Echo.py', [u'\t'+u'Closing file %s' % filename, _(u'Done.')], 
                _(u'Compressing %s') % Utilities.BasenameMod(filename))]
        else:
            # Warning: zip goes crazy when receiving empty parameters
            return[(Globals.ZIP_BIN, params+[filename,'--']+contents,
                _(u'Compressing %s') % Utilities.BasenameMod(filename))]
        
    def addCommandParseOutput(self, text=''):
        "How to parse one line of programs output when adding"
        if text and text.startswith('  adding: '):
            endIndex = text.find(' (', 10)
            if endIndex > 0:
                return (1, _('Adding %s') % Utilities.BasenameMod(text[10:endIndex]))
        return (0, '')
    
    def deleteCommand(self, filename, contents, options):
        "Command to delete the contents from the file"
        baseNameCon=[]
        for con in contents:
			baseNameCon.append(con[0])		
        return[(Globals.ZIP_BIN, ['-d',filename] + baseNameCon,
			_(u'Deleting contents from %s') % Utilities.BasenameMod(filename))]
			
    def renameCommand(self, filename, contents, newname, options):
        "Command to rename the contents of the file"
        return [('RenameZip.py', [Globals.ZIPNOTE_BIN, filename, contents[0][0], newname],
             _(u'Renaming %(oldname)s to %(newname)s')
                % {'oldname':contents[0][0], 'newname':newname})]
    
    def testCommand(self, filename):
        "Command to test the file integrity"
        # Check for multivolume
        if self.isZipMultivolume(filename):
            tmpFile = self.temporary_testCommand
            return [(Globals.ZIP_BIN,['-s-', '-O', tmpFile, filename], _(u'Reading volumes')),
                (Globals.UNZIP_BIN, ['-tv',tmpFile], _(u'Testing the integrity of the file'))]
        else:
            return [(Globals.UNZIP_BIN, ['-tv',filename], _(u'Testing the integrity of the file'))]
    
    def fixCommand(self, filename, newFilename):
        "Command to fix the file"
        return [(Globals.ZIP_BIN, ['-vFF','-O',newFilename,filename], _(u'Repairing file'))]
        
    def compressionLevels(self):
        "Returns the available compression levels"
        return [('0 '+_(u'Store'),'0',False),
                ('1','1',False),
                ('2','2',False),
                ('3','3',False),
                ('4','4',False),
                ('5','5',False),
                ('6 '+_(u'Default'),'6',True),
                ('7','7',False),
                ('8','8',False),
                ('9 '+_(u'Maximum'),'9',False)]
    
    def canCompress(self):
        "True if we can create or modify archives with this format"
        global CAN_COMPRESS
        return CAN_COMPRESS
    
    def canEncrypt(self):
        "True if the format allows encryption"
        return True

    def canSplit(self):
        "True if the format can be splitted into volumes"
        # Not supported by unzip yet (6.0), but we can give it some use
        return True
    
    def canPack(self):
        "True if the format can store multiple files"
        return True
    
    def canRename(self):
        "True if the format can rename it's content efficiently"
        return True
    
    def canAllowFilesSameName(self):
        "True if the format can store files with the same name"
        return False
    
    def canAllowFileDirSameName(self):
        "True if the format can store files and folders with the same name"
        return True
    
    def extensions(self):
        "Returns the extensions supported by the compression format"
        return ['.zip']
    
    def enabled(self):
        "If not enabled we can't manage files with this format"
        global ENABLED
        return (ENABLED, _(u'Zip support is unavailable. ' \
            u'Check that zip and unzip are installed and that the paths ' \
            u'configured in Tarumba are correct.'))
    
    def list(self, filename):
        "Shows the contents of a file in a treeListCtrl" 
        # Patch to set the locale as described above
        environ = os.environ.copy()
        language, encoding = locale.getdefaultlocale()
        if language:
            environ['LC_CTYPE'] = language+'.ISO8859-1'
        else:
            environ['LC_CTYPE'] = 'en_US.ISO8859-1'
        # Do the job
        error, output = Compressor.list(self, filename, env=environ)
        # Return values 0 and 256 will be accepted
        if error == 256:
            error = 0
            Utilities.Debug('\n'.join(output))
            output = []
        return (error, output)
        
    def extract(self, filename, contents, path): 
        "Extracts the contents to the path"
        # Patch to set the locale as described above
        environ = os.environ.copy()
        language, encoding = locale.getdefaultlocale()
        if language:
            environ['LC_CTYPE'] = language+'.ISO8859-1'
        else:
            environ['LC_CTYPE'] = 'en_US.ISO8859-1'
        # Check for multivolume
        if self.isZipMultivolume(filename):
            try:
                # Use a temporary file
                tmpAux = Utilities.WithoutExtension(filename)
                tmpDir = Temporary.tmpDir()
                tmpFile = os.path.join(tmpDir, Utilities.BasenameMod(tmpAux))
                if not tmpFile.upper().endswith('.ZIP'):
                    tmpFile += '.zip'
                # Join the multivolumes
                command = [(Globals.ZIP_BIN,['-s-', '-O', tmpFile, filename], _(u'Reading volumes'))]
                error, output = Executor.execute(command, _(u'Reading volumes'),
                    parser=self.extractCommandParseOutput, totalProgress=Globals.file_num_elements)
                if error:
                    return (error, output)
                # Extract the contents from the temporary file
                # Redefine the function to support encrypted files
                error, output = Compressor.extract(self, tmpFile, contents, path, 
                    execFunction=Executor.executeEncryptedZip, env=environ)
            finally:
                # Destroy the temporary folder
                Utilities.DeleteFile(tmpDir)
        else:
            # Redefine the function to support encrypted files
            error, output = Compressor.extract(self, filename, contents, path, 
                execFunction=Executor.executeEncryptedZip, env=environ)
        return (error, output)
        
    def add (self, filename, contents, path, options):
        "Adds the contents to the current compressed file"
        # Because encrypted files can be added, we ask to the user
        # The flag disables asking for password when renaming files
        if (os.path.isfile(filename)) and not options.flagDisableAskPass:
            # Do not ask if only folders are added
            ask = False
            for contentPack in contents:
                for con in contentPack:
                    if (os.path.isfile(con)):
                        ask = True
                        break
            # Show a dialog to the user    
            if ask and (not Globals.NOGUI) and Globals.PARENT and (not Globals.NO_ASK_TO_ENCRYPT):
                answer = Utilities.YesNoDialog(_(u'You can add ' \
                    u'the files with a passsword.\nDo you want to do it?'))
                if (answer == wx.ID_YES):
                    options.password = Utilities.AskForPassword()
                    Globals.compressionOptions.password = options.password
        # Patch to set the locale as described above
        environ = os.environ.copy()
        language, encoding = locale.getdefaultlocale()
        if language:
            environ['LC_CTYPE'] = language+'.ISO8859-1'
        else:
            environ['LC_CTYPE'] = 'en_US.ISO8859-1'
        # Redefine the function to support encrypted files
        return Compressor.add(self, filename, contents, path,
            options, execFunction=Executor.executeEncryptedZip, env=environ)
            
    def delete (self, filename, contents, options):
        "Deletes the contents from the current compressed file"
        # Patch to set the locale as described above
        environ = os.environ.copy()
        language, encoding = locale.getdefaultlocale()
        if language:
            environ['LC_CTYPE'] = language+'.ISO8859-1'
        else:
            environ['LC_CTYPE'] = 'en_US.ISO8859-1'
        # Do the job
        return Compressor.delete(self, filename, contents, options, env=environ)
        
    def rename (self, filename, contents, newname, options):
        "Renames the content to the newname"
        # Patch to set the locale as described above
        environ = os.environ.copy()
        language, encoding = locale.getdefaultlocale()
        if language:
            environ['LC_CTYPE'] = language+'.ISO8859-1'
        else:
            environ['LC_CTYPE'] = 'en_US.ISO8859-1'
        # Do the job
        return Compressor.rename(self, filename, contents, newname, options, env=environ)
            
    def test (self, filename):
        "Test the integrity of the current compressed file"
        # Patch to set the locale as described above
        environ = os.environ.copy()
        language, encoding = locale.getdefaultlocale()
        if language:
            environ['LC_CTYPE'] = language+'.ISO8859-1'
        else:
            environ['LC_CTYPE'] = 'en_US.ISO8859-1'
        # Check for multivolume
        if self.isZipMultivolume(filename):
            try:
                error = 1
                output = _('The temporary file could not be created.')
                # Use a temporary file
                tmpAux = Utilities.WithoutExtension(filename)
                tmpDir = Temporary.tmpDir()
                tmpFile = os.path.join(tmpDir, Utilities.BasenameMod(tmpAux))
                if not tmpFile.upper().endswith('.ZIP'):
                    tmpFile += '.zip'
                # Save the temporary filename to be retrieved by testCommand
                self.temporary_testCommand = tmpFile
                # Redefine the function to support encrypted files
                error, output = Compressor.test(self, filename,
                    execFunction=Executor.executeEncryptedZipTest, env=environ)
            finally:
                # Destroy the temporary folder
                Utilities.DeleteFile(tmpDir)
                return (error, output)
        else:
            # Redefine the function to support encrypted files
            return Compressor.test(self, filename, 
                execFunction=Executor.executeEncryptedZipTest, env=environ)
            
    def fix (self, filename, newFilename):
        "Fix the current compressed file"
        # Patch to set the locale as described above
        environ = os.environ.copy()
        language, encoding = locale.getdefaultlocale()
        if language:
            environ['LC_CTYPE'] = language+'.ISO8859-1'
        else:
            environ['LC_CTYPE'] = 'en_US.ISO8859-1'
        # Do the job
        return Compressor.fix(self, filename, newFilename, env=environ)
    
    def isZipMultivolume(self, filename):
        # Not in the compressor interface, this function is also used by CompressionManager
        
        "Returns true if the file is a zip multivolume"
        if filename.upper().endswith('.ZIP') and os.path.exists(filename[:-2]+'01'):
            return True
        else:
            return False
            
    # INITIALIZATION
    def isInstalled(self):
        global ENABLED
        global CAN_COMPRESS
        # If we have unzip and zipinfo we can read files
        if Utilities.IsInstalled(Globals.UNZIP_BIN) and Utilities.IsInstalled(Globals.ZIPINFO_BIN):
            Utilities.Debug(_(u'Unzip found in your system, zip read support enabled.'))
            ENABLED = True
        else:
            Utilities.Debug(_(u'WARNING: Unzip not found, zip support disabled.'))
            ENABLED = False
            CAN_COMPRESS = False
        # If zip is also installed, we can create/modify zip files
        if ENABLED:   
            if Utilities.IsInstalled(Globals.ZIP_BIN) and Utilities.IsInstalled(Globals.ZIPNOTE_BIN):
                Utilities.Debug(_(u'Zip found in your system, zip complete support enabled.'))
                CAN_COMPRESS = True
            else:
                Utilities.Debug(_(u'WARNING: Zip not found, zip support set to read only.'))
                CAN_COMPRESS = False
        
Zip().isInstalled()
