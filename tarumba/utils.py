# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config

from gettext import gettext as _
import os
import re
import sys

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

def check_read(filename):
    """
    Check if a file is readable.

    :param filename: File name to check
    :raises FileNotFoundError: The file is not readable
    """

    if os.path.isfile(filename):
        if not os.access(filename, os.R_OK):
            raise PermissionError(_("can't read %(filename)s") % {'filename': filename})
    else:
        if os.path.exists(filename):
            raise IsADirectoryError(_("%(filename)s is not a file") % {'filename': filename})
        else:
            raise FileNotFoundError(_("%(filename)s doesn't exist") % {'filename': filename})

def check_write(filename):
    """
    Check if a file is writable.

    :param filename: File name to check
    :raises FileNotFoundError: The file is not readable
    """

    if os.path.isfile(filename):
        if not os.access(filename, os.W_OK):
            raise PermissionError(_("can't write %(filename)s") % {'filename': filename})
    else:
        if os.path.exists(filename):
            raise IsADirectoryError(_("%(filename)s is not a file") % {'filename': filename})

def is_multivolume(archive):
    """
    Returns true if the file name matches the multivolume pattern.

    :param archive: Archive name
    :return: True if it's a multivolume
    """

    if re.match('.*\.[0-9]+$', archive):
        return True
    else:
        return False
    
def get_volumes(archive):
    """
    Checks if an archive is part of a multivolume and returns it's members.

    :param archive: Archive name
    :return: List of volumes, or None if not multivolume
    """

    if is_multivolume(archive):
        dot_position = archive.rfind('.') + 1
        len_suffix = len(archive[dot_position:])
        suffix_mask = '%0' + str(len_suffix) + 'i'
        prefix = archive[:dot_position]
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

# TODO: Delete?
def get_filesystem_tree(path):
    """
    Returns all the files and folders under a filesystem path.

    :param path: Filesystem path to walk
    :return: List of files and folders
    """

    tree = [path]
    if os.path.isdir(path) and not os.path.islink(path):
        for root, dirs, files in os.walk(path, topdown=True, followlinks=config.FOLLOW_LINKS):
            for name in files:
                tree.append(os.path.join(root, name))
            for name in dirs:
                tree.append(os.path.join(root, name))
    return tree


def count_filesystem_tree(path):
    """
    Returns the number of files and folders under a filesystem path.

    :param path: Filesystem path to walk
    :return: Number of files and folders
    """

    total = 1
    if os.path.isdir(path) and not os.path.islink(path):
        for root, dirs, files in os.walk(path, topdown=True, followlinks=config.FOLLOW_LINKS):
            for name in files:
                total += 1
            for name in dirs:
                total += 1
    return total
