# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         CompressionManager.py
# Purpose:      Manages the available compressors.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: CompressionManager.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
from formats.Tar import Tar
from formats.Gzip import Gzip
from formats.TarGzip import TarGzip
from formats.Zip import Zip
from formats.Rar import Rar
from formats.Compressor import Compressor

import wx.gizmos
import os

#####################
## CONSTANT VALUES ##
#####################

# Known compression formats
TAR = 'TAR'
GZIP = 'GZIP'
BZIP2 = 'BZIP2'
TAR_BZIP2 = 'TAR.BZ2'
TAR_GZIP = 'TAR.GZ'
ZIP = 'ZIP'
RAR = 'RAR'
ARJ = 'ARJ'
ACE = 'ACE'

# Archive status
ARCHIVE_NORMAL = 0          # All operations allowed
ARCHIVE_NOPACK = 1          # Archive format can't pack
ARCHIVE_NOCOMPRESSOR = 2    # Compressor not available (read only)
ARCHIVE_MULTIVOLUME = 3     # Multivolume (read only)
ARCHIVE_NOWRITE = 4         # No write permissions for file (read only)


######################
## GLOBAL VARIABLES ##
######################

archiveStatus = ARCHIVE_NORMAL


###############
## FUNCTIONS ##
###############

def checkAvailableCompressors():
    "Re-check the compressor's availability"
    Tar().isInstalled()
    Gzip().isInstalled()
    Zip().isInstalled()
    Rar().isInstalled()

def compressorNames():
    "Returns a list with the supported compressor names"
    # Actually, it's used only in the CompressionDialog
    # Preferrend formats should be on the top
    list = []
    if TarGzip().enabled()[0] and TarGzip().canCompress():
        list.append(('Tar+Gzip', TAR_GZIP))
    if Tar().enabled()[0] and Tar().canCompress():
        list.append(('Tar', TAR))
    if Zip().enabled()[0] and Zip().canCompress():
        list.append(('Zip', ZIP))
    if Rar().enabled()[0] and Rar().canCompress():
        list.append(('Rar', RAR))
    # Formats with no packing suppor in the bottom of the list
    if Gzip().enabled()[0] and Gzip().canCompress():
        list.append(('Gzip', GZIP))
    return list

def compressorByFormat(format):
    "Returns the compressor associated with the format"
    if format == TAR_GZIP:
        return TarGzip()
    if format == GZIP:
        return Gzip()
    if format == TAR:
        return Tar()
    if format == ZIP:
        return Zip()
    if format == RAR:
        return Rar()
    
def formatByExtension(filename):
    "Chooses a compressor based in the filename's extension"
    basename = Utilities.BasenameMod(filename)
    # Get the base name for multivolumes
    multiBasename = ''
    if Utilities.IsGenericMultivolume(basename):
        multiBasename = Utilities.WithoutExtension(basename)
    # Generic multivoume support for tar-based files
    if (basename.upper().endswith('.TAR.GZ') or basename.upper().endswith('.TGZ') or
        multiBasename.upper().endswith('.TAR.GZ') or multiBasename.upper().endswith('.TGZ')):
        return TAR_GZIP
    if (basename.upper().endswith('.GZ') or basename.upper().endswith('-GZ')):
        return GZIP
    # Generic multivoume support for tar-based files
    if (basename.upper().endswith('.TAR') or multiBasename.upper().endswith('.TAR')):
        return TAR
    if (basename.upper().endswith('.ZIP')):
        return ZIP
    if (basename.upper().endswith('.RAR')):
        return RAR

def compressorByExtension(filename):
    "Returns a format based in the filename's extension"
    format = formatByExtension(filename)
    return compressorByFormat(format)
    
def checkFilename(filename, format):
    "Checks if the filename is valid for it's format"
    compressor = compressorByFormat(format)
    basename = Utilities.BasenameMod(filename)
    for i in compressor.extensions():
        # If the extension is valid, return input filename
        if (filename.upper().endswith(i.upper())):           
            return filename
    # If invalid extension return input filename.<default extension>
    return filename + compressor.extensions()[0]
    
def list(filename, treeListCtrl, compressor=None):
    "Shows the contents of a file in a treeListCtrl"
    global __compressor
    # Check for multivolumes
    multivolume = False
    # Zip
    if Zip().isZipMultivolume(filename):
        multivolume = True
    # Rar
    if Rar().isRarMultivolume(filename):
        multivolume = True
    # Tar-based formats
    if Utilities.IsGenericMultivolume(filename):
        multivolume = True
        # Switch to the first one
        dotPos = filename.rfind('.')+1
        lenSuffix = len(filename[dotPos:])
        filename = filename[:dotPos] + ('0'*lenSuffix)
        # Set the new filename in Globals
        Globals.file = filename
    # Check if the file exists
    if not os.path.isfile(filename):
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The file does not exist.' \
            '') % Utilities.BasenameMod(filename))
    # Choose compressor
    if compressor:
        __compressor = compressor
    else:
        __compressor = compressorByExtension(filename)
    # If not a known file returns error message
    if not __compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if the format's support is available
    enabled, message = __compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    # Changes to the default compression level
    for level in __compressor.compressionLevels():
        if level[2]:
            Globals.compressionOptions.level = level[1]
    # Clean the wxTreeListCtrl
    # Probably is not optimal, something like DeleteAll should exist
    treeListCtrl.DeleteAllItems()
    for i in range(treeListCtrl.GetColumnCount(),0,-1):
        treeListCtrl.RemoveColumn(i-1)
        
    # Updates the archive and menu status
    global archiveStatus
    archiveStatus = ARCHIVE_NORMAL
    if Globals.PARENT:
        Globals.PARENT.MenusSetFull()
    # Check if the archive format can pack
    if not __compressor.canPack():
        archiveStatus = ARCHIVE_NOPACK
        if Globals.PARENT:
            Globals.PARENT.MenusSetNopack()
    # Check if the compression is available
    elif not __compressor.canCompress():
        archiveStatus = ARCHIVE_NOCOMPRESSOR
        if Globals.PARENT:
            Globals.PARENT.MenusSetReadonly()
    # Multivolumes can't be modified
    elif multivolume:
        archiveStatus = ARCHIVE_MULTIVOLUME
        if Globals.PARENT:
            Utilities.Log(_(u'Multivolume detected, the file cannot be modified.'), Utilities.INFO)
            Globals.PARENT.MenusSetReadonly()
    # Check if we can write the file or set readonly
    elif not os.access(filename, os.W_OK):
        archiveStatus = ARCHIVE_NOWRITE
        if Globals.PARENT:
            Utilities.Log(_(u'Your user has no write permissions on this file.'), Utilities.WARN)
            Globals.PARENT.MenusSetReadonly()
            
    # Add new colums to the TreeListCtrl
    __compressor.prepareTreeListCtrl(treeListCtrl)
    # Update the TreeListCtrl
    error, outputAux = __compressor.list(filename)
    # If everything seems Ok
    if not error:
        # Shows the information in the TreeListCtrl
        try:
            __compressor.processOutputInTreeListCtrl(filename, outputAux, treeListCtrl)
        except Exception, e:
            return (1, _('Error when reading the archive:')+' '+unicode(e))
        # Resize the width of the colums
        treeListCtrl.SetColumnWidth(0,200)
        for i in range(1, treeListCtrl.GetColumnCount()):
            treeListCtrl.SetColumnWidth(i,100)
        # Returns with a Ok message
        output = _(u'File %s loaded.' % Utilities.BasenameMod(filename))
    # If there is a problem, return an errror message
    else:
        # Set the menus to no-file status
        if Globals.PARENT:
            Globals.PARENT.MenusSetNofile()
        output = _(u'Error when loading file %s' \
            '') % Utilities.BasenameMod(filename) + ': ' + '\n'.join(outputAux)
    Utilities.Beep()
    return (error, output)

def listText(filename, compressor=None):
    "Returns the contents of the file in text format"
    global __compressor
    # Checks if the file exists
    if not os.path.isfile(filename):
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The file does not exists.' \
            '') % Utilities.BasenameMod(filename))
    # Choose compressor
    if compressor:
        __compressor = compressor
    else:
        __compressor = compressorByExtension(filename)
    # If not valid return a message error
    if not __compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if the format's support is available
    enabled, message = __compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    # Returns the contents of the file
    error, outputAux = __compressor.list(filename)
    # Prepare the return message
    if error:
        output= _(u'Error when loading file %s' \
            '') % Utilities.BasenameMod(filename) + ': ' + '\n'.join(outputAux)
    else:
        output = '\n'.join(outputAux)
    Utilities.Beep()
    return (error, output)

def extract(filename, treeCtrl, path, compressor=None):
    "Extracts the contents to the path"
    # Choose compressor
    global __compressor
    if not compressor:
        compressor = __compressor
    if not compressor:
        compressor = compressorByExtension(filename)
    # If not a valid file returns error message
    if not compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if the format's support is available
    enabled, message = compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    # Get the selected items
    selection = treeCtrl.GetSelections()
    # Used to avoid extracting files with the same path
    extracted = set()
    # Use recursion to get the full list of contents to be extracted
    firstConfirmOverwriteCall = True
    contents = []
    for sel in selection:
        subContents = Utilities.RecursiveSelection(treeCtrl, sel)
        # Check if two files/folders with the same name have been selected
        contentName = Utilities.BasenameMod(subContents[0][0])
        if contentName in extracted:
            return (1, _(u'You cannot extract more than one file or folder with the name %s to the same path.')%contentName)
        else:
            extracted.add(contentName)
        # Remove duplicates. See Tar.extractCommand for more details
        # The set is eficient when dealing with duplicates
        uniqList = set()
        i = len(subContents)-1
        while (i >= 0):
            # Delete the content if duplicated
            if subContents[i][0] in uniqList:
                del subContents[i]
            # Update the unique list otherwise
            else:
                uniqList.add(subContents[i][0])
            i-=1
        # Ask for confirmation to overwrite files
        subContents = Utilities.ConfirmOverwriteFilesLocal(subContents, path, firstConfirmOverwriteCall)
        firstConfirmOverwriteCall = False
        # None value means the user pressed "Cancel"
        if not subContents:
            return (0, '')
        # Save the selection if it still contains files
        # The funny options are for the root (empty) content
        if subContents and ((len(subContents) > 1) or (subContents[0][0])):
            contents.append(subContents)   
    # Use the compressor to extract the files
    error, output = compressor.extract(filename, contents, path)
    Utilities.Beep()
    return (error, output)

def add(filename, contents, path, treeCtrl, options, compressor=None):
    "Adds the contents to the current compressed file"
    # Choose compressor
    global __compressor
    if not compressor:
        compressor = __compressor
    if not compressor:
        compressor = compressorByExtension(filename)
    # If not a valid file returns error message
    if not compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if the format's support is available
    enabled, message = compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    
    # Check the archive status
    global archiveStatus
    if archiveStatus == ARCHIVE_NOPACK:
        errMessage = _(u'This archive format can store only one file.')
    elif archiveStatus == ARCHIVE_NOCOMPRESSOR:
        errMessage = _(u'Can\'t change files with this format. Check that you have all the necessary programs installed.')
    elif archiveStatus == ARCHIVE_MULTIVOLUME:
        errMessage = _(u'Multivolume detected, the file cannot be modified.')
    elif archiveStatus == ARCHIVE_NOWRITE:
        errMessage = _(u'Your user has no write permissions on this file.')
    if archiveStatus != ARCHIVE_NORMAL:
        Utilities.Beep()
        return (1, errMessage)
        
    # Translate min, max and def compression levels
    if options.level == 'min':
        options.level = compressor.compressionLevels()[0][1]
    elif options.level == 'max':
        options.level = compressor.compressionLevels()[-1][1]
    elif options.level == 'def':
        for op in compressor.compressionLevels():
            if op[2]:
                options.level = op[1]
    # Used to avoid adding files with the same name
    added = set()
    # Process ever selected file
    totalFiles = []
    for content in contents:
        # Check if two files/folders with the same name have been selected
        contentName = Utilities.BasenameMod(content)
        if contentName in added:
            return (1, _(u'You cannot compress more than one file or folder with the name %s at the same time.')%contentName)
        else:
            added.add(contentName)
        # Select the contents recursively      
        filesAux = Utilities.RecursiveSelectionInFileSys(content)
        # Add the contents to the total
        totalFiles.append(filesAux)
    # See if any content already exists in the archive
    # Does not have sense if the archive allows duplicates
    if treeCtrl and (not compressor.canAllowFilesSameName()):
        totalFiles = Utilities.ConfirmOverwriteFilesArchive(totalFiles, path, treeCtrl, compressor.canAllowFileDirSameName())
    # Stop if none overwrited
    if not totalFiles:
        return (0,'0 files compressed.')
    # Use the compressor to add the files
    error, output = compressor.add(filename, totalFiles, path, options)
    Utilities.Beep()
    return (error, output)

def delete(filename, treeCtrl, options, compressor=None):
    "Deletes the contents from the current compressed file"
    # Choose compressor
    global __compressor
    if not compressor:
        compressor = __compressor
    if not compressor:
        compressor = compressorByExtension(filename)
    # If not a valid file returns error message
    if not compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if the format's support is available
    enabled, message = compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    
    # Check the archive status
    global archiveStatus
    if archiveStatus == ARCHIVE_NOPACK:
        errMessage = _(u'This archive cannot be emptied. Remove the archive file instead.')
    elif archiveStatus == ARCHIVE_NOCOMPRESSOR:
        errMessage = _(u'Can\'t change files with this format. Check that you have all the necessary programs installed.')
    elif archiveStatus == ARCHIVE_MULTIVOLUME:
        errMessage = _(u'Multivolume detected, the file cannot be modified.')
    elif archiveStatus == ARCHIVE_NOWRITE:
        errMessage = _(u'Your user has no write permissions on this file.')
    if archiveStatus != ARCHIVE_NORMAL:
        Utilities.Beep()
        return (1, errMessage)
    
    # Show a confirmation dialog
    nomSelected = ''
    ids = treeCtrl.GetSelections()
    for id in ids:
        nomSelected += '\n' + treeCtrl.GetPyData(id)[0]
    answer = Utilities.YesNoDialog(_(u'Are you sure you want to delete the following ' \
        u'files and folders?') + nomSelected)
    if (answer != wx.ID_YES):
        return (1, _(u'Process aborted by the user.'))
    # Get the selected items
    selection = treeCtrl.GetSelections()
    # The set is eficient when dealing with duplicates
    uniqList = set()
    # Use recursion to get the full list of contents to be deleted
    contents = []
    for sel in selection:
        subContents = Utilities.RecursiveSelection(treeCtrl, sel)
        # Remove duplicates
        i = len(subContents)-1
        while (i >= 0):
            # If the contents exists in the archive
            if subContents[i][2]:
                # Delete the content if duplicated
                if subContents[i][0] in uniqList:
                    del subContents[i]
                # Update the unique list otherwise
                else:
                    uniqList.add(subContents[i][0])
            # Omit implicit folders not present in the archive
            else:
                del subContents[i]
            i-=1
        # Add the subContents to the final list
        contents.extend(subContents)
    # Some compressors prefer the list in the reverse order
    contents.reverse()
    # Use the compressor to delete the files
    error, output = compressor.delete(filename, contents, options)
    Utilities.Beep()
    return (error, output)

def rename(filename, treeCtrl, newName, options, compressor=None):
    "Renames or moves a file or folder inside the archive"
    # Choose compressor
    global __compressor
    if not compressor:
        compressor = __compressor
    if not compressor :
        compressor = compressorByExtension(filename)
    # If not a valid file returns error message
    if not compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if the format's support is available
    enabled, message = compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    
    # Check the archive status
    global archiveStatus
    if archiveStatus == ARCHIVE_NOPACK:
        errMessage = _(u'Operation nos supported by the archive format. Please rename the archive file instead.')
    elif archiveStatus == ARCHIVE_NOCOMPRESSOR:
        errMessage = _(u'Can\'t change files with this format. Check that you have all the necessary programs installed.')
    elif archiveStatus == ARCHIVE_MULTIVOLUME:
        errMessage = _(u'Multivolume detected, the file cannot be modified.')
    elif archiveStatus == ARCHIVE_NOWRITE:
        errMessage = _(u'Your user has no write permissions on this file.')
    if archiveStatus != ARCHIVE_NORMAL:
        Utilities.Beep()
        return (1, errMessage)
    
    # Check if this format can rename
    elif not compressor.canRename():
        Utilities.Beep()
        return (1, _(u'Sorry. This format does not support renaming operations. ' \
            u'You can try to extract and re-compress the contents with a new name.'))  
    # Get the selected items
    selection = treeCtrl.GetSelections()
    # The set is eficient when dealing with duplicates
    uniqList = set()
    # Use recursion to get the full list of contents affected
    contents = []
    for sel in selection:
        subContents = Utilities.RecursiveSelection(treeCtrl, sel)
        # Remove duplicates
        i = len(subContents)-1
        while (i >= 0):
            # If the contents exists in the archive
            if subContents[i][2]:
                # Delete the content if duplicated
                if subContents[i][0] in uniqList:
                    del subContents[i]
                # Update the unique list otherwise
                else:
                    uniqList.add(subContents[i][0])
            i-=1
        # Add the subContents to the final list
        contents.extend(subContents)
    # Use the compressor to rename the files
    error, output = compressor.rename(filename, contents, newName, options)
    Utilities.Beep()
    return (error, output)
    
def test(filename, compressor=None):
    "Test the integrity of the current compressed file"
    # Choose compressor
    global __compressor
    if not compressor:
        compressor = __compressor
    if not compressor:
        compressor = compressorByExtension(filename)
    # If not a valid file returns error message
    if not compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if format's support is available
    enabled, message = compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    error, output = compressor.test(filename)
    Utilities.Beep()
    return (error, output)

def fix(filename, newFilename, compressor=None):
    "Fix the current compressed file"
    # Choose compressor
    global __compressor
    if not compressor:
        compressor = __compressor
    if not compressor:
        compressor = compressorByExtension(filename)
    # If not a valid file returns error message
    if not compressor:
        Utilities.Beep()
        return (1, _(u'Can\'t load the file %s: The selected file' \
            u' has an unknown format.') % Utilities.BasenameMod(filename))
    # Check if format's support is available
    enabled, message = compressor.enabled()
    if not enabled:
        Utilities.Beep()
        return(1, message)
    # Check if we are able to change the file
    if not compressor.canCompress():
        Utilities.Beep()
        return (1, _(u'Can\'t change files with this format ' \
            u'check that you have all the necessary programs installed.'))
    error, output = compressor.fix(filename, newFilename)
    Utilities.Beep()
    return (error, output)
    
def compressionLevels(format=None):
    "Returns the compression levels for the selected format"
    global __compressor
    if not format:
        compressorAux = __compressor
    else:
        compressorAux = compressorByFormat(format)
    return compressorAux.compressionLevels()

def canCompress(format=None):
    "Return True if we can compress with the format"
    global __compressor
    if not format:
        compressorAux = __compressor
    else:
        compressorAux = compressorByFormat(format)
    return compressorAux.canCompress()

def canEncrypt(format=None):
    "Returns True if the format allows encryption"
    global __compressor
    if not format:
        compressorAux = __compressor
    else:
        compressorAux = compressorByFormat(format)
    return compressorAux.canEncrypt()

def canSplit(format=None):
    "Return True if the format can be splitted into volumes"
    global __compressor
    if not format:
        compressorAux = __compressor
    else:
        compressorAux = compressorByFormat(format)
    return compressorAux.canSplit()

def canPack(format=None):
    "Return True if the format can store multiple files"
    global __compressor
    if not format:
        compressorAux = __compressor
    else:
        compressorAux = compressorByFormat(format)
    return compressorAux.canPack()

def extensions(format=None):
    "Returns the extensions supported by the compression format"
    global __compressor
    if not format:
        compressorAux = __compressor
    else:
        compressorAux = compressorByFormat(format)
    return compressorAux.extensions()

def setFormat(format):
    "Changest the current compressor"
    global __compressor
    __compressor = compressorByFormat(format)
    


###############
## VARIABLES ##
###############

# Current compressor
__compressor = None
        
