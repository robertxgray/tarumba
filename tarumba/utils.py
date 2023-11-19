# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's utilities"

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

def is_multivolume(archive):
    """
    Returns true if the file name matches the multivolume pattern.

    :param archive: Archive name
    :return: True if it's a multivolume
    """

    if re.match(r'.*\.[0-9]+$', archive):
        return True
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
    return None
