# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's utilities"

from gettext import gettext as _
import os
import random
import re
import sys

from tarumba.gui import current as t_gui

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

def safe_filelist(files):
    """
    Sanitizes a list of files.

    :param files: List of files
    :return: Sanitized list
    """

    safe_list = []
    for file in files:
        # Remove duplicate and trailing slashes
        safe_file = re.sub('/+', '/', file).rstrip('/')
        if safe_file not in safe_list:
            safe_list.append(safe_file)
    return safe_list

def random_name():
    """
    Returns a random-generated string.

    :return: Random name
    """

    characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
                    'o','p','q','r','s','t','u','v','w','x','y','z',
                    'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                    'O','P','Q','R','S','T','U','V','W','X','Y','Z',
                    '1','2','3','4','5','6','7','8','9','0','_']
    name = ''
    for _ in range(10):
        name += random.choice(characters)
    return name

def new_password(archive):
    """
    Prompts for a new password with double check.

    :param archive: Archive path
    :return: Password
    """

    base_name = os.path.basename(archive)
    password = None
    while password is None:
        password1 = t_gui.prompt_password(_('Enter a password for %(archive)s') %
            {'archive': base_name})
        password2 = t_gui.prompt_password(_('Reenter the password') %
            {'archive': base_name})
        if password1 == password2:
            password = password1
        else:
            message = _("the passwords don't match, please try again")
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': message})
    return password

def get_password(file):
    """
    Prompts for a existing password.

    :param file: File name
    :return: Password
    """

    if file:
        message = _('%(file)s is encrypted, enter the password') % {'file': file}
    else:
        message = _('enter the password')
    return t_gui.prompt_password(message)

def get_list_columns(input_cols, default_cols, output):
    """
    Returns the effective list of columns. If the output list is empty, headers will be added.

    :param input_cols: Input columns
    :param default_cols: Default columns
    :param output: Output list
    :return: List of columns
    """

    columns = input_cols
    if not columns:
        columns = default_cols
    if len(output) == 0:
        output.append(columns)
    return columns
