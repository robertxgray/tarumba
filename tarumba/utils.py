# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import configuration

from rich.console import Console

import os
import re
import sys

def log(message):
    """
    Prints a log message to the console.

    :param message: Message to print
    """

    if configuration.DISABLE_COLOR:
        sys.stdout.write(message.rstrip()+'\n')
    else:
        console = Console()
        console.out(message.rstrip())

def error(message):
    """
    Prints an error message to the console.

    :param message: Message to print
    """

    if configuration.DISABLE_COLOR:
        sys.stderr.write(message.rstrip()+'\n')
    else:
        console = Console(stderr=True, style='bold red')
        console.out(message.rstrip())

def encode(text):
    """
    Encode text to the default encoding.
    Used with text to be sent to pexpect or config files.

    :param text: Input text
    :return: Encoded text
    """

    return text.encode(sys.getfilesystemencoding(), 'replace')

def decode(text):
    """
    Decode text from the default encoding.
    Used with text received from the terminal.

    :param text: Input text
    :return: Decoded text
    """

    return text.decode(sys.getfilesystemencoding(), 'replace')

def is_multivolume(filename):
    """
    Returns true if the file name matches the multivolume pattern.

    :param filename: File name
    :return: True if it's a multivolume
    """

    if re.match('.*\.[0-9]+$', filename):
        return True
    else:
        return False
    
def get_volumes(filename):
    """
    Checks if a file is part of a multivolume and returns it's members.

    :param filename: File name
    :return: List of volumes, or None if not multivolume
    """

    if is_multivolume(filename):
        dot_position = filename.rfind('.') + 1
        len_suffix = len(filename[dot_position:])
        suffix_mask = '%0' + str(len_suffix) + 'i'
        prefix = filename[:dot_position]
        # Cycle through the existing files
        idx = 0
        volumes = []
        next_vol = prefix + (suffix_mask % idx)
        while os.path.isfile(next_vol):
            volumes.append(next_vol)
            idx += 1
            next_vol = prefix + (suffix_mask % idx)
        return volumes
    # If not multivolume, return None
    else:
        return None
