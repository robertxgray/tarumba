# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Executor.py
# Purpose:      Performs the compression commands.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Executor.py $
# Copyright:    (c) 2006 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import Globals
import Utilities
import Temporary

import wx
import pexpect
import re
import sys
import os
import signal
import time

# Command to change the current directory
CHDIR = 'CHDIR'

# Current process being executed
subprocess = None

# Global variables
progress = None
varContinue = None
outputText = None

# If set to false, the user has aborted the subprocess
varContinue = True

# Path to the source files
TARUMBA_SOURCE = os.getenv('TARUMBA_SOURCE')
if not(TARUMBA_SOURCE):
            TARUMBA_SOURCE = os.path.dirname(sys.argv[0])

def abortExecution(signum, frame):
    "This funcion kills the current process on execution"
    global subprocess
    global varContinue
    varContinue = False
    if subprocess:
        subprocess.kill(signal.SIGTERM)
        
def showDialog():
    "This function shows the progress dialog or the output text"
    global progress
    global outputText
    if progress:
        progress.kill(signal.SIGUSR1)
    if outputText:
        outputText.kill(signal.SIGUSR1)
        
def hideDialog():
    "This function hides the progress dialog or the output text"
    global progress
    global outputText
    if progress:
        progress.kill(signal.SIGUSR2)
    if outputText:
        outputText.kill(signal.SIGUSR2)
        
def execute(commands, title='', parser=None, totalProgress=None,
    showOutput=False, unknownProgress=False, env=None):
    "Executes the given commands"
    # The input format is a list of tuples containing the following:
    # The name/route of the program to execute
    # The parameter list for the program
    # The message shown during the execution
    # If the name of the program is CHDIR a directory change is performed
    # X output can be disabled via the Globals.NOGUI variable
    
    global CHDIR
    global TARUMBA_SOURCE
    # Variables used to abort the subprocess and hide the dialog
    global subprocess
    global varContinue
    global progress
    global outputText
    # Init the return variables
    error = 0
    output = ''
    # Init variables used with except
    progress = None
    outputText = None
    # Show the commands to execute
    Utilities.Debug(`commands`)
    # Save the current directory
    currDir = os.getcwd()
    try:
        # Check if the parser is defined
        parserDef = False
        if parser and (parser() is not None):
            parserDef = True
        # If the X output is not disabled
        if not Globals.NOGUI:           
            if not showOutput:
                # Show a progress dialog
                if not totalProgress:
                    totalProgress = len(commands)
                # With unknown progress, the size is always 10
                if unknownProgress:
                    totalProgress = 10
                # Use a special call with the progress dialogs
                tempFileName = Temporary.tmpFile()
                tempFile = open(tempFileName, 'w')
                progress = pexpect.spawn(
                    '/usr/bin/env',
                    ['python',
                    TARUMBA_SOURCE+'/moreControls/CustomProgressDialog.py', 
                    str(os.getpid()),title,commands[0][2],
                    str(totalProgress),str(int(unknownProgress)),
                    tempFileName],
                    timeout=None)
                progress.setecho(False)
            else:
                # Show the TextCtrl. Use also the special call
                outputText = pexpect.spawn(
                    '/usr/bin/env',
                    ['python',
                    TARUMBA_SOURCE+'/moreControls/OutputTextDialog.py', 
                    str(os.getpid()),title],timeout=None)
                outputText.setecho(False)
        # Execute every command
        i = -1
        varContinue = True
        for command in commands:  
            # If the cancel button has been used, stop
            if not varContinue:
                break
            # If a parser is not defined and the X interface is not disabled
            if (not parserDef) and (not Globals.NOGUI) and (
                not showOutput) and (not unknownProgress):        
                # Update the progress dialog
                i += 1
                progress.sendline(Utilities.Encode(str(i)+' '+command[2]))
            # Execute the directory changes
            if command[0] == CHDIR:
                os.chdir(command[1][0])
                continue
            # Execute the commands using pexpect
            subprocess = pexpect.spawn(command[0], command[1], timeout=None, env=env)
            subprocess.setecho(False)
            case = 100
            output = []
            # Tries to get every line in the program's output
            while (case > 0):
                # If the cancel button has been used, stop
                if not varContinue:
                    break
                case = subprocess.expect(
                    [pexpect.EOF,
                    '\r\n', 
                    '\n'])
                if (case > 0) or len(subprocess.before):
                    subOutput = Utilities.Decode(subprocess.before)
                    output.append(subOutput)
                    # If the X output is not disabled
                    if not Globals.NOGUI:
                        # If showOutput is also sent to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.before)
                        elif parserDef and not unknownProgress:
                            increment, text = parser(subOutput)
                            i += increment
                            tempFile.write(Utilities.Encode(str(i)+' '+text+'\n'))
                            tempFile.flush()
                    # If not disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
            subprocess.close()
            error = subprocess.status
            # If error stop executing
            if error:
                # Tell if aborted by the user
                if not varContinue:
                    output = [_(u'Process aborted by the user.')]
                # Restore the current directory
                os.chdir(currDir)
                # If the interface is not disabled, finish it
                if not Globals.NOGUI:
                    if not showOutput:
                        progress.close()
                        Utilities.DeleteFile(tempFileName)
                    else:
                        outputText.kill(signal.SIGINT)
                        outputText.wait()
                return (error, output)
        # Restore the current directory
        os.chdir(currDir)
        # If the interface is not disabled, finish it
        if not Globals.NOGUI:
            if not showOutput:
                progress.close()
                Utilities.DeleteFile(tempFileName)
            else:
                outputText.kill(signal.SIGINT)
                outputText.wait()
        # Tell if aborted by the user
        if not varContinue:
            output = [_(u'Process stopped by the user')]
            error = 1
        return (error, output)
    except Exception, e:
        emessage = unicode(e)
        # Restore the current dir
        os.chdir(currDir)
        # If the interface is not disabled, finish it
        if not Globals.NOGUI:
            if not showOutput:
                if progress:
                    progress.close()
                    Utilities.DeleteFile(tempFileName)
            else:
                if outputText and outputText.isalive():
                    outputText.sendline(
                        Utilities.Encode(_(u'ERROR: ') + emessage))
                    outputText.kill(signal.SIGINT)
                    outputText.wait()
        # If not disabled but need output, use the standart
        elif showOutput:
            Utilities.Log(emessage, Utilities.ERRO)
        # Return the error message
        return (-1, [emessage])
        
def executeEncryptedZip(commands, title='', parser=None, totalProgress=None,
    showOutput=False, unknownProgress=False, env=None):
    "Executes the given commands and if a password is needed then "
    "asks to the user for it"
    # Progress dialogs can be disabled via Globals.NOGUI variable
    
    global CHDIR
    global TARUMBA_SOURCE
    # Variables used to abort the subprocess and hide the dialog
    global subprocess
    global varContinue
    global progress
    global outputText
    # Init the return variables
    error = 0
    output = ''
    # Init variables used with pexpect
    progress = None
    outputText = None
    enterPass = re.compile('.*password:')
    enterPass2 = re.compile('.*reenter:')
    password=Globals.compressionOptions.password
    # Show the commands to execute
    Utilities.Debug(`commands`)
    # Save the current directory
    currDir = os.getcwd()
    try:
        # Check if the parser is defined
        parserDef = False
        if parser and (parser() is not None):
            parserDef = True
        # If the X interface is not disabled
        if not Globals.NOGUI:
            if not showOutput:
                # Show a progress dialog
                if not totalProgress:
                    totalProgress = len(commands)
                # With unknown progress, the size is always 10
                if unknownProgress:
                    totalProgress = 10
                # Use a special call with the progress dialogs
                tempFileName = Temporary.tmpFile()
                tempFile = open(tempFileName, 'w')
                progress = pexpect.spawn(
                    '/usr/bin/env',
                    ['python',
                    TARUMBA_SOURCE+'/moreControls/CustomProgressDialog.py', 
                    str(os.getpid()),title,commands[0][2],
                    str(totalProgress),str(int(unknownProgress)),
                    tempFileName], 
                    timeout=None)
                progress.setecho(False)
            else:
                # Show the TextCtrl. Use also the special call
                outputText = pexpect.spawn(
                    '/usr/bin/env',
                    ['python',
                    TARUMBA_SOURCE+'/moreControls/OutputTextDialog.py', 
                    str(os.getpid()),title],timeout=None)
                outputText.setecho(False)     
        # Ejecute every command
        i = -1
        j = -1
        varContinue = True
        numCommands = len(commands)-1
        # Tests if a password has been used
        passwordUsed = 0
        while i < numCommands:
            # If the cancel button has been used, stop
            if not varContinue:
                break
            i += 1
            command = commands[i]
            # If a parser is not defined and the X interface is not disabled
            if (not parserDef) and (not Globals.NOGUI) and (
                not showOutput) and (not unknownProgress):        
                # Update the progress dialog
                j += 1
                progress.sendline(Utilities.Encode(str(j)+' '+command[2]))
            # Performs the directory changes
            if command[0] == CHDIR:
                os.chdir(command[1][0])
                continue
            # Execute the commands using pexpect
            subprocess = pexpect.spawn(command[0], command[1], timeout=None, env=env)
            subprocess.setecho(False)
            case = 100
            output = []
            # Tries to get every line of the program's output
            flagPassword = False
            while (case > 0):
                case = subprocess.expect(
                    [pexpect.EOF,  
                    '\r\n',
                    '\n',
                    enterPass, 
                    enterPass2])
                    
                # Show the output of the process
                if ((case > 0) and (case < 3)) or len(subprocess.before) > 0:
                    subOutput = Utilities.Decode(subprocess.before)
                    output.append(subOutput)
                    # If the X interface is not disabled
                    if not Globals.NOGUI:
                        # If sendOutput send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.before)
                        elif parserDef and not unknownProgress:
                            increment, text = parser(subOutput)
                            j += increment
                            tempFile.write(Utilities.Encode(str(j)+' '+text+'\n'))
                            tempFile.flush()
                    # If not disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                # If asked for password, add also the subprocess.after
                if ((case > 2) and (len(subprocess.after) > 0)):
                    subOutput = Utilities.Decode(subprocess.after)
                    output.append(subOutput)
                    # If the X interface is not disabled
                    if not Globals.NOGUI:
                        # If showOutput send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.after)
                    # If disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                        
                # If we are asked for the password, introduce it
                if case > 2:
                    # If we don't have it, ask to the user
                    if not password: 
                        # PATCH: Wait to show the password dialog
                        # The app does not behave well when opening two
                        # dialogs at the sime time
                        time.sleep(3)
                        password = Utilities.AskForPassword(_(u'Enter the ' \
                            u'password for %s') % command[1][-1])
                        if not password:
                            password = ''
                        # Avoid 4 pass request when no initial pass set 
                        if passwordUsed == 0:
                            passwordUsed = 1
                        # Update the global password variable
                        Globals.compressionOptions.password = password
                    # Use the password and mark it's use
                    if not flagPassword:
                        passwordUsed += 1
                        flagPassword = True
                    subprocess.sendline(Utilities.Encode(password))
                    
            # End the subprocess
            subprocess.close()
            error = subprocess.status
            # If a password has been used with no success, try it again
            if error:
                if passwordUsed > 0 and passwordUsed < 4:
                    error = 0
                    password = None
                    i -= 1
            # On success, go to next file and reset the variable
            else:
                passwordUsed = 0
            # In case of error, stop executing
            if error:
                # Tell if aborted by the user
                if not varContinue:
                    output = [_(u'Process stopped by the user')]
                # If the X interface is not disabled, finish it
                if not Globals.NOGUI:
                    if not showOutput:
                        progress.close()
                    else:
                        outputText.kill(signal.SIGINT)
                        outputText.wait()
                # Restore the current directory
                os.chdir(currDir)
                return (error, output)
        # Restore the current directory
        os.chdir(currDir)
        # If the X interface is not disable, finish it
        if not Globals.NOGUI:
            if not showOutput:
                progress.close()
            else:
                outputText.kill(signal.SIGINT)
                outputText.wait()
        # Tell if aborted by the user
        if not varContinue:
            output = [_(u'Process stopped by the user')]
            error = 1
        return (error, output)
    except Exception, e:
        emessage = unicode(e)
        # Restore the current directory
        os.chdir(currDir)
        # If the X interface is not disabled, finish it
        if not Globals.NOGUI:
            if not showOutput:
                if progress:
                    progress.close()
            else:
                if outputText and outputText.isalive():
                    outputText.sendline(
                        Utilities.Encode(_(u'ERROR: ') + emessage))
                    outputText.kill(signal.SIGINT)
                    outputText.wait()
        # If not disabled but need output, use the standart
        elif showOutput:
            Utilities.Log(emessage, Utilities.ERRO)
        # Return the error message
        return (-1, [emessage])
    
def executeEncryptedZipTest(commands, title='', showOutput=True, 
    unknownProgress=False, env=None):
    "Executes the given commands and if a password is needed then "
    "asks to the user for it"
    # Progress dialogs can be disabled via Globals.NOGUI variable
    
    global CHDIR
    global TARUMBA_SOURCE
    # Variables used to abort the subprocess and hide the dialog
    global subprocess
    global varContinue
    global outputText
    # Init the return variables
    error = 0
    output = ''
    # Init variables used with pexpect
    outputText = None
    enterPass = re.compile('.*password:')
    enterPass2 = re.compile('.*reenter:')
    # Show the commands to execute
    Utilities.Debug(`commands`)
    # Save the current directory
    currDir = os.getcwd()
    try:
        # If the X interface is not disabled
        if not Globals.NOGUI:
            # Show the TextCtrl. Use also the special call
            outputText = pexpect.spawn(
                '/usr/bin/env',
                ['python',
                TARUMBA_SOURCE+'/moreControls/OutputTextDialog.py', 
                str(os.getpid()),title],timeout=None)
            outputText.setecho(False)     
        # Ejecute every command
        i = -1
        varContinue = True
        numCommands = len(commands)-1
        while i < numCommands:
            # If the cancel button has been used, stop
            if not varContinue:
                break
            i += 1
            command = commands[i]
            # Execute the commands using pexpect
            subprocess = pexpect.spawn(command[0], command[1], timeout=None, env=env)
            subprocess.setecho(False)
            case = 100
            output = []
            # Tries to get every line of the program's output
            flagPassword = False
            while (case > 0):
                case = subprocess.expect(
                    [pexpect.EOF,  
                    '\r\n',
                    '\n',
                    enterPass, 
                    enterPass2])
                    
                # Show the output of the process
                if ((case > 0) and (case < 3)) or len(subprocess.before) > 0:
                    subOutput = Utilities.Decode(subprocess.before)
                    output.append(subOutput)
                    # If the X interface is not disabled
                    if not Globals.NOGUI:
                        # If sendOutput send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.before)
                    # If not disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                # If asked for password, add also the subprocess.after
                if ((case > 2) and (len(subprocess.after) > 0)):
                    subOutput = Utilities.Decode(subprocess.after)
                    output.append(subOutput)
                    # If the X interface is not disabled
                    if not Globals.NOGUI:
                        # If showOutput send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.after)
                    # If disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                        
                # If we are asked for the password, introduce it
                if case > 2:
                        # PATCH: Wait to show the password dialog
                        # The app does not behave well when opening two
                        # dialogs at the sime time
                        time.sleep(3)
                        # Get the file name from the subprocess' output
                        if case == 3:
                            filenameAux = subprocess.after[
                                :subprocess.after.rfind(' ')]
                            filename = filenameAux[
                                filenameAux.rfind(' ')+1:]
                            password = Utilities.AskForPassword(_(u'Enter the ' \
                                u'password for %s') % filename)
                        # If password incorrect, show a fixed message
                        else:
                            password = Utilities.AskForPassword(_(u'Password ' \
                                u'incorrect. Try again'))
                        if not password:
                            password = ''                   
                        subprocess.sendline(Utilities.Encode(password))
                    
            # End the subprocess
            subprocess.close()
            error = subprocess.status
            # In case of error, stop executing
            if error:
                # Tell if aborted by the user
                if not varContinue:
                    output = [_(u'Process stopped by the user')]
                # If the X interface is not disabled, finish it
                if not Globals.NOGUI:
                    outputText.kill(signal.SIGINT)
                    outputText.wait()
                # Restore the current directory
                os.chdir(currDir)
                return (error, output)
        # Restore the current directory
        os.chdir(currDir)
        # If the X interface is not disable, finish it
        if not Globals.NOGUI:
            outputText.kill(signal.SIGINT)
            outputText.wait()
        # Tell if aborted by the user
        if not varContinue:
            output = [_(u'Process stopped by the user')]
            error = 1
        return (error, output)
    except Exception, e:
        emessage = unicode(e)
        # Restore the current directory
        os.chdir(currDir)
        # If the X interface is not disabled, finish it
        if not Globals.NOGUI:
            if not showOutput:
                if progress:
                    progress.close()
            else:
                if outputText and outputText.isalive():
                    outputText.sendline(Utilities.Encode(_(u'ERROR: ') + emessage))
                    outputText.kill(signal.SIGINT)
                    outputText.wait()
        # If not disabled but need output, use the standart
        elif showOutput:
            Utilities.Log(emessage, Utilities.ERRO)
        # Return the error message
        return (-1, [emessage])

def executeEncryptedRar(commands, title='', parser=None, totalProgress=None,
    showOutput=False, unknownProgress=False, env=None):
    "Executes the given commands and if a password is needed then "
    "asks to the user for it"
    # Progress dialogs can be disabled via the Globals.NOGUI variable
    
    global CHDIR
    global TARUMBA_SOURCE
    # Variables used to abort the subprocess and hide the dialog
    global subprocess
    global varContinue
    global progress
    global outputText
    # Init the return variables
    error = 0
    output = ''
    # Init the variables used with pexpect
    progress = None
    outputText = None
    enterPass = re.compile('Enter password \(will not be echoed\).*:')
    enterPass2 = re.compile(
        '.* - use current password \? \[Y\]es, \[N\]o, \[A\]ll ')
    password=Globals.compressionOptions.password
    # Show the commands to execute
    Utilities.Debug(`commands`)
    # Save the current directory
    currDir = os.getcwd()
    try:
        # Check if the parser is defined
        parserDef = False
        if parser and (parser() is not None):
            parserDef = True
        # If the X interface is not disabled
        if not Globals.NOGUI:
            if not showOutput:
                # Show a progress dialog
                if not totalProgress:
                    totalProgress = len(commands)
                # With unknown progress, the size is always 10
                if unknownProgress:
                    totalProgress = 10
                # Use a special call with the progress dialogs
                tempFileName = Temporary.tmpFile()
                tempFile = open(tempFileName, 'w')
                progress = pexpect.spawn(
                    '/usr/bin/env',
                    ['python',
                    TARUMBA_SOURCE+'/moreControls/CustomProgressDialog.py', 
                    str(os.getpid()),title,commands[0][2],
                    str(totalProgress),str(int(unknownProgress)),
                    tempFileName], 
                    timeout=None)
                progress.setecho(False)
            else:
                # Show the TextCtrl. Use also the special call
                outputText = pexpect.spawn(
                    '/usr/bin/env',
                    ['python',
                    TARUMBA_SOURCE+'/moreControls/OutputTextDialog.py', 
                    str(os.getpid()),title],timeout=None)
                outputText.setecho(False)
        # Ejecute every command
        i = -1
        j = -1
        varContinue = True
        numCommands = len(commands)-1
        # Tests if a password has been used
        passwordUsed = 0
        while i < numCommands:
            # If cancel button has been pressed, stop
            if not varContinue:
                break
            i += 1
            command = commands[i]
            # If a parser is not defined and the X interface is enabled
            if (not parserDef) and (not Globals.NOGUI) and (
                not showOutput) and (not unknownProgress):           
                # Update the progress bar
                j += 1
                progress.sendline(Utilities.Encode(str(j)+' '+command[2]))
            # Execute the directory changes
            if command[0] == CHDIR:
                os.chdir(command[1][0])
                continue
            # Execute the program using pexpect
            subprocess = pexpect.spawn(command[0], command[1], timeout=None, env=env)
            subprocess.setecho(False)
            case = 100
            output = []
            # Try to get every line of the output
            flagPassword = False
            while (case > 0):
                case = subprocess.expect(
                    [pexpect.EOF,  
                    '\r\n',
                    '\n',
                    enterPass2,
                    enterPass, 
                    'Reenter password:'])
                    
                # Show the output of the process
                if ((case > 0) and (case < 3)) or len(subprocess.before) > 0:
                    subOutput = Utilities.Decode(subprocess.before)
                    output.append(subOutput)
                    # If the X interface is enabled
                    if not Globals.NOGUI:
                        # If showOutput, send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.before)
                        elif parserDef and not unknownProgress:
                            increment, text = parser(subOutput)
                            j += increment
                            tempFile.write(Utilities.Encode(str(j)+' '+text+'\n'))
                            tempFile.flush()
                    # If disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                # If input is requested, then add subprocess.after
                if ((case > 2) and (len(subprocess.after) > 0)):
                    subOutput = Utilities.Decode(subprocess.after)
                    output.append(subOutput)
                    # If the X interface is enabled
                    if not Globals.NOGUI:
                        # If showOutput send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.after)
                    # If disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                        
                # When asking for continue using password, say "no"
                # We will never be here (I think)
                if case == 3:
                   subprocess.sendline(Utilities.Encode('N')) 
                # If we are asked for the password, enter it
                if case > 3:
                    # If we don't have it, ask to the user
                    if not password:
                        # PATCH: Wait to show the password dialog
                        # The app does not behave well when opening two
                        # dialogs at the sime time
                        time.sleep(3)
                        password = Utilities.AskForPassword(_(u'Enter the ' \
                            u'password for %s') % command[1][-1])
                        if not password:
                            password = ''
                        # Avoid 4 pass request when no initial pass set 
                        if passwordUsed == 0:
                            passwordUsed = 1
                        # Update the global password variable          
                        Globals.compressionOptions.password = password
                    # Use the password and mark it's use
                    if not flagPassword:
                        passwordUsed += 1
                        flagPassword = True
                    subprocess.sendline(Utilities.Encode(password))
            
            # End the subprocess
            subprocess.close()
            error = subprocess.status
            # If a password has been used with no success, try it again
            if error:
                if passwordUsed > 0 and passwordUsed < 4:
                    error = 0
                    password = None
                    i -= 1
            # On success, go to next file and reset the variable
            else:
                passwordUsed = 0
            # In case of error don't continue
            if error:
                # Tell if aborted by the user
                if not varContinue:
                    output = [_(u'Process stopped by the user')]
                # If the X interface is enabled finish it
                if not Globals.NOGUI:
                    if not showOutput:
                        progress.close()
                    else:
                        outputText.kill(signal.SIGINT)
                        outputText.wait()
                # Restore the current dir
                os.chdir(currDir)
                return (error, output)
        # Restore the current dir
        os.chdir(currDir)
        # If the X interface is enabled, finish it
        if not Globals.NOGUI:
            if not showOutput:
                progress.close()
            else:
                outputText.kill(signal.SIGINT)
                outputText.wait()
        # Tell if aborted by the user
        if not varContinue:
            output = [_(u'Process stopped by the user')]
            error = 1
        return (error, output)
    except Exception, e:
        emessage = unicode(e)
        # Restore the current dir
        os.chdir(currDir)
        # If the X interface is enabled, finish it
        if not Globals.NOGUI:
            if not showOutput:
                if progress:
                    progress.close()
            else:
                if outputText and outputText.isalive():
                    outputText.sendline(
                        Utilities.Encode(_(u'ERROR: ') + emessage))
                    outputText.kill(signal.SIGINT)
                    outputText.wait()
        # If disabled but need output, use the standart
        elif showOutput:
            Utilities.Log(emessage, Utilities.ERRO)
        # Return the error message
        return (-1, [emessage])

def executeEncryptedRarTest(commands, title='', showOutput=True, 
    unknownProgress=False, env=None):
    "Executes the given commands and if a password is needed then "
    "asks to the user for it"
    # Progress dialogs can be disabled via the Globals.NOGUI variable
    
    global CHDIR
    global TARUMBA_SOURCE
    # Variables used to abort the subprocess and hide the dialog
    global subprocess
    global varContinue
    global outputText
    # Init the return variables
    error = 0
    output = ''
    # Init the variables used with pexpect
    outputText = None
    enterPass = re.compile('Enter password \(will not be echoed\).*:')
    enterPass2 = re.compile(
        '.* - use current password \? \[Y\]es, \[N\]o, \[A\]ll ')
    # Show the commands to execute
    Utilities.Debug(`commands`)
    # Save the current directory
    currDir = os.getcwd()
    try:
        # If the X interface is not disabled
        if not Globals.NOGUI:
            # Show the TextCtrl. Use also the special call
            outputText = pexpect.spawn(
                '/usr/bin/env',
                ['python',
                TARUMBA_SOURCE+'/moreControls/OutputTextDialog.py', 
                str(os.getpid()),title],timeout=None)
            outputText.setecho(False)
        # Ejecute every command
        i = -1
        varContinue = True
        numCommands = len(commands)-1
        while i < numCommands:
            # If cancel button has been pressed, stop
            if not varContinue:
                break
            i += 1
            command = commands[i]
            # Execute the program using pexpect
            subprocess = pexpect.spawn(command[0], command[1], timeout=None, env=env)
            subprocess.setecho(False)
            case = 100
            output = []
            alwaysSamePassword = None
            # Try to get every line of the output
            while (case > 0):
                case = subprocess.expect(
                    [pexpect.EOF,  
                    '\r\n',
                    '\n',
                    enterPass2,
                    enterPass, 
                    'Reenter password:']) 
                      
                # Show the output of the process
                if ((case > 0) and (case < 3)) or len(subprocess.before):
                    subOutput = Utilities.Decode(subprocess.before)
                    output.append(subOutput)
                    # If the X interface is enabled
                    if not Globals.NOGUI:
                        # If showOutput, send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.before)
                    # If disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                # If input is requested, then add subprocess.after
                if ((case > 2) and (len(subprocess.after) > 0)):
                    subOutput = Utilities.Decode(subprocess.after)
                    output.append(subOutput)
                    # If the X interface is enabled
                    if not Globals.NOGUI:
                        # If showOutput send it to the textCtrl
                        if showOutput:
                            outputText.sendline(subprocess.after)
                    # If disabled but need output, use the standart
                    elif showOutput:
                        Utilities.StandartOutput(subOutput)
                        
                # Ask to the user about continue using the same password
                if case == 3:
                    if not alwaysSamePassword:
                        hideDialog()
                        answerAux = Utilities.YesNoDialog(_(u'Use the same password for all the files?'))
                        if (answerAux == wx.ID_YES): 
                            alwaysSamePassword = 'Y'
                        else:
                            alwaysSamePassword = 'N' 
                        showDialog()
                    subprocess.sendline(Utilities.Encode(alwaysSamePassword))
                # If we are asked for the password, enter it
                if case > 3:
                    # PATCH: Wait to show the password dialog
                    # The app does not behave well when opening two
                    # dialogs at the sime time
                    time.sleep(3)
                    # Get the file name from the subprocess' output
                    filename = subprocess.after[
                        subprocess.after.rfind(' ')+1:-1]
                    password = Utilities.AskForPassword(_(u'Enter the ' \
                        u'password for %s') % filename)
                    if not password:
                        password = ''
                    # Use the password 
                    subprocess.sendline(Utilities.Encode(password))
                    
            # End the subprocess
            subprocess.close()
            error = subprocess.status
            # In case of error don't continue
            if error:
                # Tell if aborted by the user
                if not varContinue:
                    output = [_(u'Process stopped by the user')]
                # If the X interface is enabled finish it
                if not Globals.NOGUI:
                    outputText.kill(signal.SIGINT)
                    outputText.wait()
                # Restore the current dir
                os.chdir(currDir)
                return (error, output)
        # Restore the current dir
        os.chdir(currDir)
        # If the X interface is enabled, finish it
        if not Globals.NOGUI:
            outputText.kill(signal.SIGINT)
            outputText.wait()
        # Tell if aborted by the user
        if not varContinue:
            output = [_(u'Process stopped by the user')]
            error = 1
        return (error, output)
    except Exception, e:
        emessage = unicode(e)
        # Restore the current dir
        os.chdir(currDir)
        # If the X interface is enabled, finish it
        if not Globals.NOGUI:
            if outputText and outputText.isalive():
                outputText.sendline(
                    Utilities.Encode(_(u'ERROR: ') + emessage))
                outputText.kill(signal.SIGINT)
                outputText.wait()
        # If disabled but need output, use the standart
        elif showOutput:
            Utilities.Log(emessage, Utilities.ERRO)
        # Return the error message
        return (-1, [emessage])

def executeOpenssl(commands, title, password, env=None):
    "Use openssl to encrypt o decrypt a file"
    # The progress dialog can be diabled via Globals.NOGUI
    
    # Init the return variables
    error = 0
    output = ''
    # Show the commands to execute
    Utilities.Debug(`commands`)
    global TARUMBA_SOURCE
    # Variables used to abort the subprocess
    global subprocess
    global varContinue
    # Init variables used with pexpect
    progress = None
    enterPass = re.compile('.*password:')
    # Use an array with a single command to be like the others
    command = commands[0]
    try:
        # If the X interface is enabled
        if not Globals.NOGUI:
            # Use a special call with the progress dialogs
            tempFileName = Temporary.tmpFile()
            tempFile = open(tempFileName, 'w')
            progress = pexpect.spawn(
                '/usr/bin/env',
                ['python',
                TARUMBA_SOURCE+'/moreControls/CustomProgressDialog.py', 
                str(os.getpid()),title,commands[0][2],
                str(10),str(int(True)),
                tempFileName], 
                timeout=None)
            progress.setecho(False)      
        # Execute the command with pexpect
        subprocess = pexpect.spawn(command[0], command[1], timeout=None, env=env)
        subprocess.setecho(False)
        case = 100
        output = []
        # Try to get every line of the output
        while (case > 0):
            case = subprocess.expect(
                [pexpect.EOF,  
                '\r\n',
                '\n',
                enterPass])
            if ((case > 0) and (case < 3)) or len(subprocess.before) > 0:
                output.append(Utilities.Decode(subprocess.before))
            # If asked by password, add also the subprocess.after
            if ((case > 2) and (len(subprocess.after) > 0)):
                output.append(Utilities.Decode(subprocess.after))
            # If asked by the password, enter it
            if case > 2:
                subprocess.sendline(Utilities.Encode(password))
        subprocess.close()
        error = subprocess.status
        # In case of error stop executing
        if error:
            # Tell if aborted by the user
            if not varContinue:
                output = [_(u'Process stopped by the user')]
            # If the X interface is enabled finish it
            if not Globals.NOGUI:
                progress.close()
            return (error, output)
        # If the X interface is enabled finish it
        if not Globals.NOGUI:
            progress.close()
        # Tell if aborted by the user
        if not varContinue:
            output = [_(u'Process stopped by the user')]
            error = 1
        return (error, output)
    except Exception, e:
        # If the X interface is enabled finish it
        if not Globals.NOGUI:
            if progress:
                progress.close()
        # Return the error message
        return (-1, [unicode(e)])
        
