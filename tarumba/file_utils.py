# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's utilities"

from gettext import gettext as _
import os

from tarumba.config import current as config
from tarumba.gui import current as t_gui

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
    :raises PermissionError: The file is not readable
    :raises IsADirectoryError: Element in path is not a file
    """

    if os.path.isfile(filename):
        if not os.access(filename, os.W_OK):
            raise PermissionError(_("can't write %(filename)s") % {'filename': filename})
    else:
        if os.path.exists(filename):
            raise IsADirectoryError(_("%(filename)s is not a file") % {'filename': filename})

def _check_add_file(form, archive, path, contents, overwrite):
    """
    Checks if a file can be archived.

    :param form: Archive format
    :param archive: Archive path
    :param path: Filesystem path to walk
    :param contents: Archive contents
    :param overwrite: Overwrite control
    :raises FileNotFoundError: The file doesn't exist
    :raises IsADirectoryError: Element in path is not a file
    :raises PermissionError: The file is not readable
    """
    if not os.path.exists(path):
        raise FileNotFoundError(_("%(filename)s doesn't exist") % {'filename': path})
    if not form.CAN_SPECIAL and not os.path.isfile(path) and not os.path.isdir(path):
        raise IsADirectoryError(
            _("%(format)s archive format can't store the special file %(filename)s") %
            {'format': form.NAME, 'filename': path})
    if not os.access(path, os.R_OK):
        raise PermissionError(_("can't read %(filename)s") % {'filename': path})
    if contents is not None and path in contents:
        overwrite = t_gui.prompt_ynan(
            _('%(filename)s already exists in %(archive)s. Do you want to overwrite?') %
            {'filename': path, 'archive': os.path.basename(archive)})
    return overwrite

def check_add_filesystem_tree(form, archive, path, contents):
    """
    Returns all the files and folders under a filesystem path.

    :param form: Archive format
    :param archive: Archive path
    :param path: Filesystem path to walk
    :param contents: Archive contents
    :return: Number of files and folders
    """

    overwrite = _check_add_file(form, archive, path, contents, None)
    print(overwrite)

    total = 1
    if os.path.isdir(path) and not os.path.islink(path):
        for root, dirs, files in os.walk(path, topdown=True,
            followlinks=config.get('follow_links')):
            for name in files:
                filepath = os.path.join(root, name)
                overwrite = _check_add_file(form, archive, filepath, contents, overwrite)
                total += 1
            for name in dirs:
                total += 1
    return total
