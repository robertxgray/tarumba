# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Rar.py
# Purpose:      Rar format support.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Rar.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

from Compressor import Compressor
import Globals
import Utilities
import Executor
import Temporary

import os
import wx.gizmos
import re

class Rar(Compressor):
    
    def prepareTreeListCtrl(self, treeListCtrl):
        "Prepares the TreeListCtrl to show the contents of the file"
        treeListCtrl.AddColumn(_(u'Name'))
        treeListCtrl.AddColumn(_(u'Size'))
        treeListCtrl.AddColumn(_(u'Compressed'))
        #treeListCtrl.AddColumn(_(u'Ratio')) Doesn't work with multivolume
        treeListCtrl.AddColumn(_(u'Method'))
        treeListCtrl.AddColumn(_(u'Date'))
        treeListCtrl.AddColumn(_(u'Time'))
        treeListCtrl.AddColumn(_(u'Permissions'))
        treeListCtrl.AddColumn(_(u'CRC-32'))
        treeListCtrl.AddColumn(_(u'Version'))
    
    def processOutputInTreeListCtrl(self, filename, output, treeListCtrl):
        "Add the contents of the compressed file to the TreeListCtrl"            
        # Declare the function that fills the information
        def aux(items, addedItem):
            treeListCtrl.SetItemText(addedItem, long(items[0]), 1)
            treeListCtrl.SetItemText(addedItem, long(items[1]), 2)
            treeListCtrl.SetItemText(addedItem, items[7], 3)
            treeListCtrl.SetItemText(addedItem, items[3], 4)
            treeListCtrl.SetItemText(addedItem, items[4], 5)
            treeListCtrl.SetItemText(addedItem, items[5], 6)
            treeListCtrl.SetItemText(addedItem, items[6], 7)
            treeListCtrl.SetItemText(addedItem, items[8], 8)
        # Add the root of the tree
        # Getting the name from Globals.file works better with multivolume
        root = treeListCtrl.AddRoot(Utilities.BasenameMod(Globals.file),
            Globals.itclFile)
        # Call to the auxiliary function
        Utilities.processOutputInTreeListCtrlAux(
            output, 9, treeListCtrl, root, aux)     
            
    def listCommand(self, filename):
        "Command to list the contents of the compressed file"
        return [(Globals.RAR_BIN, ['v','-c-','-av-','--',filename], 
            _(u'Reading contents' \
            u' of the file %s') % Utilities.BasenameMod(filename))]
    
    def extractCommand(self, filename, contents):
        "Command to extract the contents from the file"
        baseNameCon=[]
        for con in contents:
            # Supress the slash at the end of folders (previously added)
            # because it produces odd behavior
            if (con[0][-1] == '/'):
                baseNameCon.append(con[0][:-1])
            else:
                baseNameCon.append(con[0])
        return [(Globals.RAR_BIN, ['x', '-idp', '-o+', '-y', 
            '-av-', '--', filename] + baseNameCon,
            _(u'Uncompressing %s') % Utilities.BasenameMod(filename))]
        
    def extractCommandParseOutput(self, text=''):
		"How to parse one line of programs output when extracting"
		if (text and (len(text)>12) and (text.split()[-1]=='OK')):
			return (1, _('Extracting %s') % Utilities.BasenameMod(' '.join(text.split()[1:-1])))
		return (0, '')
    
    def addCommand(self, filename, contents, options):
        "Command to add the contents to the file"
        output = []
        # Follow symbolic links
        follow = ''
        if not Globals.FOLLOW_LINKS:
            follow = '-ol'
        # Add the compression level
        level = ''
        if options.level:
            level += '-m' + options.level
        # Add the -p option if encryption requested
        encrypt = ''
        if options.password:
            encrypt += '-p'
        # If multivolume requested, add the -v option
        volumes = ''
        if options.volumes:
            volumes = '-v' + options.volumes + 'k' 
        output.append(Globals.RAR_BIN, ['a','-idp','-y',follow,level,volumes,encrypt,'-av-','--',filename]+contents,
            _(u'Compressing %s') % Utilities.BasenameMod(filename))    
        return output
        
    def addCommandParseOutput(self, text=''):
		"How to parse one line of programs output when adding"
		if (text and (len(text)>10) and (text.split()[-1]=='OK')):
			return (1, _('Adding %s') % Utilities.BasenameMod(' '.join(text.split()[1:-1])))
		return (0, '')
    
    def deleteCommand(self, filename, contents, options):
        "Command to delete the contents from the file"
        baseNameCon=[]
        for con in contents:
            # Supress the slash at the end of folders (previously added)
            # because it produces odd behavior
            if (con[0][-1] == '/'):
                baseNameCon.append(con[0][:-1])
            else:
                baseNameCon.append(con[0])
        return [(Globals.RAR_BIN, ['d','-idp','-y','-av-','--',
            filename] + baseNameCon, 
            _(u'Deleting contents from %s') % Utilities.BasenameMod(filename))]
    
    def renameCommand(self, filename, contents, newname, options):
        "Command to rename the contents of the file"
        # Supress the slash at the end of folders (previously added)
        # because it produces odd behavior
        if (contents[0][0][-1] == '/'):
            return [(Globals.RAR_BIN, ['rn','-idp','-y','-av-','--',
                filename, contents[0][0][:-1], newname], 
                _(u'Renaming %(oldname)s to %(newname)s')
                    % {'oldname':contents[0], 'newname':newname})]
        else:
            return [(Globals.RAR_BIN, ['rn','-idp','-y','-av-','--',
                filename, contents[0][0], newname], 
                _(u'Renaming %(oldname)s to %(newname)s')
                    % {'oldname':contents[0], 'newname':newname})]
    
    def testCommand(self, filename):
        "Command to test the file integrity"
        return [(Globals.RAR_BIN, ['t','-idp','-av-','--',filename], 
            _(u'Testing the integrity of the file'))]
            
    def test (self, filename):
        "Test the integrity of the current compressed file"
        # If a file is compressed, rar requests the password
        return Compressor.test(self, filename, 
            execFunction=Executor.executeEncryptedRarTest)
    
    def fixCommand(self, filename, newFilename):
        "Command to fix the file"
        return [(Globals.RAR_BIN, ['r','-y','-av-','--',self.__tmpFile], 
                _(u'Repairing file')),
                # I don't know how it will try to fix, so I try to copy both
                ('NoOutput.py', ['mv','-f',self.__rebTmpFile,newFilename], 
                _(u'Repairing file')),
                ('NoOutput.py', ['mv','-f',self.__fixTmpFile,newFilename], 
                _(u'Repairing file'))]    
        
    def compressionLevels(self):
        "Returns the available compression levels"
        return [('0 '+_(u'Store'),'0',False),
                ('1','1',False),
                ('2','2',False),
                ('3 '+_(u'Default'),'3',True),
                ('4','4',False),
                ('5 '+_(u'Maximum'),'5',False)]
    
    def canCompress(self):
        "True if we can create or modify archives with this format"
        return True
    
    def canEncrypt(self):
        "True if the format allows encryption"
        return True

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
        return False
    
    def canAllowFileDirSameName(self):
        "True if the format can store files and folders with the same name"
        return False
    
    def extensions(self):
        "Returns the extensions supported by the compression format"
        return ['.rar']
    
    def list(self, filename):
        "Shows the contents of a file in a treeListCtrl"
        # This function is redefined to support multivolume
        
        output = []
        error = 1
        # Old rar multivolume namespace
        old_multivolume = False
        new_multivolume = False
        if os.path.exists(filename[:-2]+'00'):
            prefix = filename[:-3]
            charcode = ord(filename[-3])
            old_multivolume = True
        else:
            # New multivolume namespace
            volMatch = re.search('\.PART[0-9]+\.RAR$', filename.upper())
            if volMatch:
                dotPos = volMatch.start()
                # 9 is the lenght of the string '.part.rar'
                digits = len(filename)-dotPos-9
                prefix = filename[:dotPos+5]
                suffix = filename[-4:]
                filenameAux = prefix + (('%0'+str(digits)+'i') % 1) + suffix
                # Select the first volume
                if os.path.isfile(filenameAux):
                    new_multivolume = True
                    filename = filenameAux
                    # Set the filename in Globals
                    Globals.file = filename
        # Get the list for every volume
        j = 0
        filenameAux = filename
        while os.path.isfile(filenameAux):
            # Ask the volume information to rar
            command = self.listCommand(filenameAux)
            error, outputAux = Executor.executeEncryptedRar(command, _(u'Processing file'), unknownProgress=True)
            if error:
                output=outputAux
                break
            # Find the line where the information begins
            mark = -1
            k = 1
            for line in outputAux:
                if re.match('----------+', line):
                        mark = k
                        break
                k+=1
            # If information not found, we have a problem
            # This happens ie, when the file is not a rar file
            if mark == -1:
                error=1
                output=outputAux
                break
            # Remove the header and footer
            outputAux = outputAux[mark:-2] 
            # Delete the asterisk that rar adds at the begining of the 
            # file names in the encrypted files
            for i in range (0,len(outputAux),2):
                if ((len(outputAux[i]) > 0) and (outputAux[i][0] == '*')):
                    outputAux[i] = ' ' + outputAux[i][1:]
            # In rar's output every file is shown in two lines, so we need to
            # join them before calling processOutputInTreeListCtrlAux
            outputAux2 = []
            for i in range(len(outputAux)/2):
                outputAux2.append(outputAux[2*i+1]+outputAux[2*i])
            outputAux = outputAux2
            # Rar doesn't add the final slash to folders so we check the
            # permisions and add it
            for i in range(len(outputAux)):
                if ((outputAux[i].split()[5][0]=='d') or (outputAux[i].split()[5][1]=='D')):
                    outputAux[i]+='/'
            # Join all the chunks for a file
            if (j > 0):
                if (outputAux[0].split()[9:] == output[-1].split()[9:]):
                    # The total size will be the sum of the chunks
                    compressed1 = int(output[-1].split()[1])
                    compressed2 = int(outputAux[0].split()[1])
                    compressed = compressed1 + compressed2
                    fileInfo = output[-1].split()[0] + ' ' + str(compressed)
                    # Join the chuncks again
                    output[-1] =  fileInfo + ' ' + ' '.join(output[-1].split()[2:])
                    # It's deleted from the other list to avoid duplicates
                    del outputAux[0]
            output = output + outputAux
            j += 1
            # Get the file name of the next chunk
            if old_multivolume:
                filenameAux = prefix + chr(charcode + (j/100)) + '%02i' % (j%100)
            elif new_multivolume:
                filenameAux = prefix + (('%0'+str(digits)+'i') % (j+1)) + suffix
            else:
                break
        return (error, output)
        
    def extract(self, filename, contents, path): 
        "Extracts the contents to the path"
        # Redefined to support encrypted files
        return Compressor.extract(self, filename, contents, path, 
            execFunction=Executor.executeEncryptedRar)
        
    def add (self, filename, contents, path, options):
        "Adds the contents to the current compressed file"
        # Ask to the user about adding the files with a password
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
        # Redefine the function to support encrypted files
        output = Compressor.add(self, filename, contents, path,
            options, execFunction=Executor.executeEncryptedRar)
        # Calculate the new file name
        if options.volumes:
            pathAux = os.path.dirname(filename)
            content1 = os.listdir(pathAux)
            for i in range(len(content1)):
                content1[i] = os.path.join(pathAux,content1[i])
            content2 = []
            for con in content1:
                # The exists save us from the broken links
                if ((os.path.lexists(con)) and (re.match(filename[:-4]+'\.part0*1\.rar',con))):
                    content2.append(con)
            # If there is more than one candidate, get the younger
            if len(content2) > 1:
                content2.sort(key = os.path.getctime)
                Globals.file = content2[-1]
            # If lenght == 1, get the only one
            elif len(content2) == 1:
                Globals.file = content2[0]
            # We can't use the standart output here
            if output[0]:
                return (output[0], _(u'Error when creating rar multivolume file.'))
            else:
                return (output[0], _(u'Rar multivolume file created.'))
        return output  
    
    def fix (self, filename, newFilename):
        "Fix the current compressed file"
        # Redefined because we need a temporary folder
        currDir = os.getcwd()
        try:
            tmpDir = Temporary.tmpDir()
            os.chdir(tmpDir)
            # Create a link to the temporary folder
            nomAux = Utilities.BasenameMod(filename)
            self.__tmpFile = os.path.join(tmpDir,nomAux)
            self.__rebTmpFile = os.path.join(tmpDir,('rebuilt.'+nomAux))
            self.__fixTmpFile = os.path.join(tmpDir,('fixed.'+nomAux))
            os.symlink(filename, self.__tmpFile)
            # Call to the parent fix function
            output = Compressor.fix(self,filename,newFilename,execFunction)
        finally:
            # Delete the temporary folder
            Utilities.DeleteFile(tmpDir)
            # Restore the working directory
            os.chdir(currDir)
        return output
    
    def enabled(self):
        "If not enabled we can't manage files with this format"
        global ENABLED
        return (ENABLED, _(u'Rar support is unavailable. ' \
            u'Check that rar is installed and that the rar\'s binary path ' \
            u'configured in Tarumba is correct.'))
            
    def isRarMultivolume(self, filename):
        "Returns true if the file is a rar multivolume"
        # Not in the compressor interface, this function is also used by CompressionManager
        
        # New format
        if re.match('.*\.PART[0-9]+\.RAR$', filename.upper()):
            return True
        # Old format
        elif filename.upper().endswith('.RAR') and os.path.exists(filename[:-2]+'00'):
            return True
        else:
            return False
            
    # INITIALIZATION
    def isInstalled(self):
        global ENABLED
        if Utilities.IsInstalled(Globals.RAR_BIN):
            Utilities.Debug(_(u'Rar found in your system, rar support enabled.'))
            ENABLED = True
        else:
            Utilities.Debug(_(u'WARNING: Rar not found, rar support disabled.'))
            ENABLED = False
        
Rar().isInstalled()
    
    
