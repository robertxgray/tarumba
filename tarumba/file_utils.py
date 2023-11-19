# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's utilities"

from gettext import gettext as _
import os

from tarumba.config import current as config

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

def check_filesystem_tree(path, form):
    """
    Returns all the files and folders under a filesystem path.

    :param path: Filesystem path to walk
    :param form: Archive format
    :return: List of files and folders
    """

    if not os.path.exists(path):
        raise FileNotFoundError(_("%(filename)s doesn't exist") % {'filename': path})
    if not form.CAN_SPECIAL and not os.path.isfile(path) and not os.path.isdir(path):
        raise FileNotFoundError(
            _("%(format)s archive format can't store the special file %(filename)s") %
            {'format': form.NAME, 'filename': path})
    if not os.access(path, os.R_OK):
        raise PermissionError(_("can't read %(filename)s") % {'filename': path})

    total = 1
    if os.path.isdir(path) and not os.path.islink(path):
        for root, dirs, files in os.walk(path, topdown=True,
            followlinks=config.get('follow_links')):
            for name in files:
                filepath = os.path.join(root, name)
                if not form.CAN_SPECIAL and not os.path.isfile(filepath):
                    raise FileNotFoundError(
                        _("%(format)s archive format can't store the special file %(filename)s") %
                        {'format': form.NAME, 'filename': path})
                if not os.access(filepath, os.R_OK):
                    raise PermissionError(_("can't read %(filename)s") % {'filename': filepath})
                total += 1
            for name in dirs:
                total += 1
    return total
