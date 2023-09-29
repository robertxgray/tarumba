# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         TextInterface.py
# Purpose:      Manages tarumba from the command line.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: TextInterface.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import Temporary
#import CompressionManager Will be imported after checking the verbose mode
import Executor
from moreControls.DummyTreeList import DummyTreeList

import getopt
import sys
import os
import wx
import signal
        
def message(message):
    "Shows the message in the standart output"
    sys.stdout.write((message+'\n').encode(sys.getfilesystemencoding()))
    
def meserror(message):
    "Shows the message in the standart error output"
    sys.stderr.write((message+'\n').encode(sys.getfilesystemencoding()))

def help(opts, args):
    "Shows the help for the program"
    # It has a "man" like format... maybe it can be reused
    # The compressor options is disabled. Some compressors can't manage files
    # without standart extension. Autodetect is now the only option.
    message(_(u"""NAME

    tarumba - interface to manage compressed files

SYNOPSIS

    tarumba [options] [files]

DESCRIPTION

    Tarumba is a graphic user interface to work with compressed files.
    It can also work in text mode when a X server is not available, this also
    allows Tarumba to be easily integrated with other programs, being
    file managers a good example.

    If no options are given, tarumba will be executed in standart graphic
    mode. It also will try to open a file (if especified) on startup.
    
    The available actions in text mode are the following. If an X server is
    available, you can request the use of X dialogs to show progress and to
    request information to the user with the --use_dialogs option.

    List the contents of a file:
        tarumba -l FILE

    Extract contents from a file:
        tarumba -x FILE [CONTENT1] [CONTENT2] [CONTENT3] ...
    If no contents are specified, all will be extracted with full path.
    
    Add contents to the file:
        tarumba -a FILE CONTENT1 [CONTENT2] [CONTENT3] ...

    Delete contents from the file:
        tarumba -d FILE CONTENT1 [CONTENT2] [CONTENT3] ...
        
    Move or rename a file's content:
        tarumba -r FILE CONTENT CONTENT_NEWNAME

    Test the integrity of a file:
        tarumba -t FILE

    Repair (fix) a file:
        tarumba -f ORIGINAL_FILE REPAIRED_FILE

OPTIONS

    -a  Add contents to the specified file.
  
    --add_to
        Add contents with extended options. Can no be used to add files to
        an existing archive (you will be asked to delete it).
        It must be used together with -a.
        It will be only available in X mode, in text mode the options
        --comp_level, --encode and --volume can be used.

    --comp_level
        Compression level used, it accepts 3 levels:
            min -> faster compression level
            def -> default compression level
            max -> higher compression level
        The values used depend on the compressor used.

    -d  Delete contents from the specified file.
  
    --encode
        Request the added contents to be encoded (if available by format).
  
    -f  Fixes the specified file.
  
    -h, --help
        Show this help message and exit.
  
    -l  Show the contents of the specified file.
    
    --ocurrence
        On formats that support multiple files with the same name, as tar,
        you can set the number of ocurrence to be processed. Be aware that
        it will apply to all the files affected by the action requested.
        
    -r  Move or rename a file's content. It can be used with folders, and the
        path for all the files or folders inside it, will be updated.
  
    -t  Test the integrity of the specified file.
  
    --use_dialogs
        When possible, X dialogs will be used to show progress and to request
        information to the user.
  
    --verbose
        Shows aditional information useful for debugging.
        This is too much information for most users.
  
    --volume
        Request the file to be splitted into volumes (if available by format). 
        In example:
            Split into volumes of 100KB:       --volume 100K
            Split into volumes of 50MB:        --volume 50M
            Split into volumes of 1GB:         --volume 1G
            
    -x  Extract contents from the specified file. Folder contents are extracted
        in a recursive way.

VERSION

    %s

BUGS
    
    Tarumba is a very young proyect and it will probably contain a lot
    of bugs waiting to be discovered by nice people like you. Please write
    to xukosky at yahoo.es if you discover a bug.""") % Globals.VERSION)
    return (0,'')

def launchGUI(opts,args):
    "Start the program in standart X mode"
    # Error if more than one file is given
    if len(args) > 1:
        meserror(_(u'ERROR: Excessive number of files, please specify one.') +
            ' ' + _(u'Run "tarumba -h" for help.'))
        sys.exit(2)
    # If there is only one, we open it
    if len(args) == 1:
        Globals.file = args[0]
        
    # Check if the X server is available
    if Globals.NOGUI:
        return (1, _(u'Tarumba cannot be started in GUI mode.' \
            u' You can still use Tarumba by parsing options, see tarumba -h.'))
    
    # Start the Main GUI     
    import MainFrame
    global application
    gui = MainFrame.create(None)
    application.SetTopWindow(gui)
    gui.Show()
    
    # Open the given file, if any
    if Globals.file != Globals.NO_FILE:
        if os.path.lexists(Globals.file):
            Globals.PARENT.multiSelectionDirCtrl1.SetPath(Globals.file)
            Globals.PARENT.OpenFile(None)
        else:
            Utilities.Log(_(u'The file %s does not exist.')%Globals.file,
                Utilities.ERRO)
            Globals.file = Globals.NO_FILE
            Globals.PARENT.staticText2.SetLabel(Globals.NO_FILE)
         
    # Start the main loop
    application.MainLoop()
    return (0,'')

def add(opts, args):
    "Add contents to the specified file"
    
    import CompressionManager
    # Remove empty namefiles on contents
    argsAux=[]
    for arg in args[1:]:
        if arg:
            argsAux.append(arg)
    args = args[0:1] + argsAux
    # Error if less than 2 files are given
    if len(args) < 2:
        meserror(_(u'ERROR: You need to specify the compressed file and ' \
            ' then the contents to add.')+' '+_(u'Run "tarumba -h" for help.'))
        sys.exit(2) 
    # Input value for the compression dialog
    Globals.file = args[0]
    # Get the extension of the file to be used in the dialog
    forCompAux = CompressionManager.formatByExtension(Globals.file)
    if forCompAux:
        Globals.lastCompressor = forCompAux
    # If the add_to option is given, show the compression dialog
    if ('--add_to','') in opts:
        if Globals.NOGUI:
            return(1, _(u'The option --add_to needs a working X server. You can instead use the ' \
                'options --comp_level, --encode and --volume.')+' '+_(u'Run "tarumba -h" for help.'))
        else:
            # Load the compression dialog
            import CompressionDialog
            dialog = CompressionDialog.create(None,
                ((len(args[1:])>1) or os.path.isdir(args[1])))
            # End if other than the Ok button us used
            if dialog.ShowModal() != wx.ID_OK:
                dialog.Destroy()
                return (0,'')
            dialog.Destroy()
    else:
        # If encryption is requested, ask for the password
        if ('--encode','') in opts:
            # Ask for the password twice
            password1 = Utilities.AskForPassword(u'Enter the password')
            password2 = Utilities.AskForPassword(u'Enter the password again')
            if password1 != password2:
                return(1,_(u'You must enter the same password twice.'))
            Globals.compressionOptions.password = password1
        # Check if multivolume is requested
        for o in opts:
            if o[0] == '--volume':
                sizeAux = o[1].upper()
                size = 0
                try:
                    if sizeAux[-1] == 'K':
                        size = int(sizeAux[:-1],10)
                    elif sizeAux[-1] == 'M':
                        size = int(sizeAux[:-1],10) * 1024
                    elif sizeAux[-1] == 'G':
                        size = int(sizeAux[:-1],10) * 1024 * 1024
                    else:
                        raise TypeError()
                    Globals.compressionOptions.volumes = str(size)
                except TypeError, e:
                    meserror(_(u'ERROR: Invalid size for volumes.')+' '+_(u'Run "tarumba -h" for help.'))
                    sys.exit(2) 
    # Check if the file already exists. If it's a folder we can't continue
    if os.path.isdir(Globals.file):             
        return(1, _(u'Cannot create a file with this name because a folder ' \
            u'with the same name already exists.'))
    # Create a dummy treeList
    treeListCtrl = DummyTreeList()
    # If the file exists, and not multivolume, set the file contents into a dummy tree
    if os.path.isfile(Globals.file) and (not Globals.compressionOptions.volumes):
        error, output = CompressionManager.list(Globals.file, treeListCtrl)
        # In case of error, ask to overwrite the existing file
        if error:
            overwrite = Utilities.YesNoDialog(_(u'Cannot read the file %s. Do ' \
            u'you want to overwrite it?') % Globals.file, title=_(u'WARNING'))
            if overwrite == wx.ID_YES:
                Utilities.DeleteFile(Globals.file)
            else:
                return (0,'')
    # Add the contents to the file
    return CompressionManager.add(Globals.file, args[1:], '', treeListCtrl, Globals.compressionOptions) 
                    
def delete(opts, args):
    "Delete contents from the specified file"
    import CompressionManager
    # Remove empty namefiles on contents
    argsAux=[]
    for arg in args[1:]:
        if arg:
            argsAux.append(arg)
    args = args[0:1] + argsAux
    # Error if less than 2 files are given
    if len(args) < 2:
        meserror(_(u'ERROR: You need to specify the compressed file and  then the ' \
            u'contents to delete.')+' '+_(u'Run "tarumba -h" for help.'))
        sys.exit(2)
    # Get the ocurrence param if set
    ocurrence = None
    for o in opts:
        if o[0] == '--ocurrence':
            ocurrence = o[1]
            break 
    # Get the file contents into a dummy tree
    treeListCtrl = DummyTreeList()
    error, output = CompressionManager.list(args[0], treeListCtrl)
    if error:
        return (error, _(u'ERROR: Archive %s cannot be opened:')%args[0]+' ' + output)
    # Select the requested contents
    selectedNodes = []
    for arg in args[1:]:
        # Call the tree search function
        exists, nodeId = Utilities.CheckFileExistsOnTree(arg, treeListCtrl, ocurrence)
        # If the content does not exist, end with error
        if not nodeId:
            meserror(_(u'ERROR: %(content)s does not exist in %(archive)s.') % 
                {'content':arg,'archive':args[0]})
            sys.exit(1)
        # Else select the node with the content
        else:
            selectedNodes.append(nodeId)
    treeListCtrl.SetSelections(selectedNodes)
    # Extract the contents from the file
    return CompressionManager.delete(args[0], treeListCtrl, Globals.compressionOptions)            
    
def extract(opts, args):
    "Extract contents from the specified file"
    import CompressionManager
    # Remove empty namefiles on contents
    argsAux=[]
    for arg in args[1:]:
        if arg:
            argsAux.append(arg)
    args = args[0:1] + argsAux
    # Error if less than 1 files are given
    if len(args) < 1:
        meserror(_(u'ERROR: You need to specify the compressed file and ,optionally, the ' \
            u'contents to extract.')+' '+_(u'Run "tarumba -h" for help.'))
        sys.exit(2)
    # Get the ocurrence param if set
    ocurrence = None
    for o in opts:
        if o[0] == '--ocurrence':
            ocurrence = o[1]
            break
    # Get the file contents into a dummy tree
    treeListCtrl = DummyTreeList()
    error, output = CompressionManager.list(args[0], treeListCtrl)
    if error:
        return (error, _(u'ERROR: Archive %s cannot be opened:')%args[0]+' ' + output)
    # If no contents give, extract everything
    if len(args) < 2:
        treeListCtrl.SetSelections([treeListCtrl.GetRootItem()])
    # Else select the requested contents
    else:
        selectedNodes = []
        for arg in args[1:]:
            # Call the tree search function
            exists, nodeId = Utilities.CheckFileExistsOnTree(arg, treeListCtrl, ocurrence)
            # If the content does not exist, end with error
            if not nodeId:
                meserror(_(u'ERROR: %(content)s does not exist in %(archive)s.') % 
                    {'content':arg,'archive':args[0]})
                sys.exit(1)
            # Else select the node with the content
            else:
                selectedNodes.append(nodeId)
        treeListCtrl.SetSelections(selectedNodes)
    # Extract the contents from the file
    return CompressionManager.extract(args[0], treeListCtrl, os.getcwd())            
    
def list(opts, args):
    "Show the contents of the specified file"
    import CompressionManager
    # Error if not one file is given
    if len(args) != 1:
        meserror(_(u'ERROR: You need to specify the file to list.')+' '+
        _(u'Run "tarumba -h" for help.'))
        sys.exit(2)
    # Show the contents of the file
    return CompressionManager.listText(args[0])

def test(opts, args):
    "Test the integrity of the specified file"
    import CompressionManager
    # Error if not one file is given
    if len(args) != 1:
        meserror(_(u'ERROR: You need to specify the file to test.')+' '+
            _(u'Run "tarumba -h" for help.'))
        sys.exit(2)
    # Test the integrity of the file
    return CompressionManager.test(args[0])

def fix(opts, args):
    "Fix the specified file"
    import CompressionManager
    # Error if not two files are given
    if len(args) != 2:
        meserror(_(u'ERROR: You need to specify the original file and ' \
            ' also a name for the repaired file.')+' '+
            _(u'Run "tarumba -h" for help.'))
        sys.exit(2)
    # Original and repaired file can't be the same
    if (os.path.normpath(args[0]) == os.path.normpath(args[1])):
        meserror(_(u'ERROR: Original and repaired file cannot be the same.'))
        sys.exit(2)
    # If the new file already exists, delete it
    if os.path.lexists(args[1]):
        try:
            os.remove(args[1])
        except OSError, e:
            return (1, _(u'Cannot overwrite %s' % args[1]))
    # Repair the damaged file
    return CompressionManager.fix(args[0], args[1])

def rename(opts, args):
    "Renames a content of the archive"
    import CompressionManager
    # Error if less than 2 files are given
    if len(args) != 3:
        meserror(_(u'ERROR: You need to specify the compressed file, the' \
            u' name of the content to rename and it\'s new name.')+' ' \
            '' +_(u'Run "tarumba -h" for help.'))
        sys.exit(2) 
    # Delete slashes at the end
    if args[2][-1] == '/':
        newName = args[2][:-1]
    # Avoid things like /../
    if args[2] == '/':
        args[2] = args[2][1:]
    if args[2] != os.path.normpath(args[2]) or args[2][0] == '/':
        meserror(_(u'ERROR: The new name %s is not allowed.') % args[2])
        sys.exit(1) 
    # Get the ocurrence param if set
    ocurrence = None
    for o in opts:
        if o[0] == '--ocurrence':
            ocurrence = o[1]
            break 
    # Get the file contents into a dummy tree
    treeListCtrl = DummyTreeList()
    error, output = CompressionManager.list(args[0], treeListCtrl)
    if error:
        return (error, _(u'ERROR: Archive %s cannot be opened:')%args[0]+' '+output)    
    # Select the requested contents
    selectedNodes = []     
    # Call the tree search function
    exists, nodeId = Utilities.CheckFileExistsOnTree(args[1], treeListCtrl, ocurrence)
    # If the content does not exist, end with error
    if not nodeId:
        meserror(_(u'ERROR: %(content)s does not exist in %(archive)s.') % 
            {'content':args[1],'archive':args[0]})
        sys.exit(1)
    # Else select the node with the content
    else:
        selectedNodes.append(nodeId)
    treeListCtrl.SetSelections(selectedNodes)
    # Rename the content of the file
    return CompressionManager.rename(
        args[0], treeListCtrl, args[2], Globals.compressionOptions) 

def main():
    "Main function"
    try:
        # Decode the input parameters 
        argvAux = []
        for x in sys.argv[1:]:
            argvAux.append(Utilities.Decode(x))
        # GNU behavior, of course ;)
        opts, args = getopt.gnu_getopt(argvAux, 
            'adfhlrtx', 
            ['add_to', 'comp_level=', 'ocurrence=', 'encode', 'help', 
             'use_dialogs', 'verbose', 'volume='])
    # Exit un case of error
    except getopt.GetoptError:
        meserror(_(u'ERROR: Invalid option.')+' '+_(u'Run "tarumba -h" for help.'))
        sys.exit(2)
    # Check that only an action is specified
    option = None
    mesError = (_(u'ERROR: Invalid combination of options.')+' '+_(u'Run "tarumba -h" for help.'))
    for o in ['-a', '-d', '-f', '-h', '--help', '-l', '-r', '-t', '-x']:
        if (o,'') in opts:
            if not option:
                option = o
            else:
                meserror(mensError)
                sys.exit(2)
    # Check for empty parameters
    for a in args:
        if not a:
            meserror(_(u'ERROR: Empty parameters are not allowed.'))
            sys.exit(2)
    # Translate the relative paths of the files
    args2 = []
    if (option != '-d') and (option != '-x') and (option != '-r'):
        for a in args:
            args2.append(os.path.abspath(a))
    # Delete ,extract and rename command uses "in archive" files
    else:
        if len(args) >= 1:
            args2 = [os.path.abspath(args[0])] + args[1:]
            
    # Process the aditional options
    
    # Verbose
    if ('--verbose','') in opts:
        Globals.VERBOSE = True
    import CompressionManager
    
    # The wxWidgets app is needed:
    #  - If no options (actions) are requested. This opens the MainFrame
    #  - When --use_dialogs is requested
    #  - For --add_to dialog
    global application
    application = None
    if (not option) or ((option == '-a') and (('--add_to','') in opts)) or (('--use_dialogs','') in opts):
        try:
            # Check if the DISPLAY variable is set. Or the app may crash without exceptions
            if 'DISPLAY' not in os.environ or len(os.environ['DISPLAY']) < 1:
                raise Exception()
            application = wx.App(redirect=False, clearSigInt=False)
            Globals.NOGUI = False
        # Disable the GUI if the X initialization fails
        except Exception, e:
            Utilities.Log(_(u'The X server is not available.'), Utilities.ERRO)
            Globals.NOGUI = True
    # Disable the GUI when not needed
    else:
        Globals.NOGUI = True
    
    # Compression level
    for o in opts:
        if o[0] == '--comp_level':
            if o[1] in ('min', 'def', 'max'):
                Globals.compressionOptions.level = o[1]
            else:
                meserror(_(u'ERROR: Invalid compression level.')+' '+
                    _(u'Run "tarumba -h" for help.'))
                sys.exit(2)
        # If no level given, set the default
        else:
            Globals.compressionOptions.level = 'def'
                
    # Create the temporary folder
    try:
        Temporary.createTmp()
    except Exception, e:
        meserror(_(u'ERROR: The temporary folder cannot be created. ' \
            u'Check the "tmpdir" variable in %s') % Globals.FILECONFIG[0])
        sys.exit(2)
        
    # Capture the SIGUSR1 signals. See Executor module for details
    signal.signal(signal.SIGUSR1, Executor.abortExecution)
    
    # Call the function that process every action
    if not option:
        error, output = launchGUI(opts,args2)
    elif option == '-a':
        error, output = add(opts, args2)
    elif option == '-d':
        error, output = delete(opts, args2)
    elif option == '-r':
        error, output = rename(opts, args2)
    elif option == '-f':
        error, output = fix(opts, args2)
    elif option in ('-h','--help'):
        error, output = help(opts, args2)
    elif option == '-l':
        error, output = list(opts, args2)
    elif option == '-t':
        error, output = test(opts, args2)
    elif option == '-x':
        error, output = extract(opts, args2) 

    # Delete the temporary folder before exit
    Temporary.deleteTmp()   
    
    # Show the output by standart or error output
    if error > 0:
        # When error is greater then 127 the return code is undesired
        # (usually 0). See the doc of the sys python module for more details.
        error = 1
        meserror(output)
    else:
        message(output)
        
    # Exist with the apropiate retur code
    sys.exit(error)

