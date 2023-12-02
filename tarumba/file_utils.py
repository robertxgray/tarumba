# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's utilities"

from gettext import gettext as _
import os
import shutil

from tarumba import utils as t_utils
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

    follow_links = config.get('follow_links')
    if not os.path.lexists(path):
        raise FileNotFoundError(_("%(filename)s doesn't exist") % {'filename': path})
    if (not form.CAN_SPECIAL and not os.path.isfile(path) and not os.path.isdir(path) and
        not os.path.islink(path)):
        raise IsADirectoryError(
            _("%(format)s archive format can't store the special file %(filename)s") %
            {'format': form.NAME, 'filename': path})
    if not os.access(path, os.R_OK, follow_symlinks=follow_links):
        raise PermissionError(_("can't read %(filename)s") % {'filename': path})

    copy = True
    if contents is not None and path.lstrip('/') in contents:
        if overwrite not in (t_gui.ALL, t_gui.NONE):
            overwrite = t_gui.prompt_ynan(
                _('%(filename)s already exists in %(archive)s. Do you want to overwrite?') %
                {'filename': path, 'archive': os.path.basename(archive)})
        copy = overwrite in (t_gui.YES, t_gui.ALL)
    return (overwrite, copy)

def _check_add_file_copy(path, tmp_dir, copy):
    """
    Copies a file if a temporary path is given.

    :param path: File path
    :param tmp_dir: Tuple with temporary path and same FS flag
    :param copy: If false, skip this file
    :return: Number of files processed: 0 or 1
    """

    if tmp_dir and copy:
        follow_links = config.get('follow_links')
        dest_path = os.path.join(tmp_dir[0], path.lstrip('/'))

        if follow_links:
            os.symlink(path, dest_path)
        elif tmp_dir[1]:
            os.link(path, dest_path)
        else:
            shutil.copy2(path, dest_path, follow_symlinks=False)

    return 1 if copy else 0

def _check_add_folder_copy(path, tmp_dir):
    """
    Copies a folder if a temporary path is given.

    :param path: Folder path
    :param tmp_dir: Tuple with temporary path and same FS flag
    :return: Number of folders, always 1
    """

    if tmp_dir:
        dest_path = os.path.join(tmp_dir[0], path.lstrip('/'))
        os.makedirs(dest_path, exist_ok=True)
    return 1

def check_add_filesystem_tree(form, archive, path, contents, tmp_dir):
    """
    Returns all the files and folders under a filesystem path.

    :param form: Archive format
    :param archive: Archive path
    :param path: Filesystem path to walk
    :param contents: Archive contents
    :param tmp_dir: Tuple with temporary path and same FS flag
    :return: Number of files and folders
    """

    follow_links = config.get('follow_links')
    if os.path.isdir(path) and (follow_links or not os.path.islink(path)):
        total = 1
        overwrite = None
        for root, dirs, files in os.walk(path, topdown=True, followlinks=follow_links):
            for name in dirs:
                dirpath = os.path.join(root, name)
                total += _check_add_folder_copy(dirpath, tmp_dir)
            for name in files:
                filepath = os.path.join(root, name)
                overwrite, copy = _check_add_file(form, archive, filepath, contents, overwrite)
                total += _check_add_file_copy(filepath, tmp_dir, copy)
    else:
        overwrite, copy = _check_add_file(form, archive, path, contents, None)
        total = _check_add_file_copy(path, tmp_dir, copy)
    return total

def get_filesystem(path):
    """
    Returns the file system of a given path.

    :param path: Path
    :return: Filesystem
    """

    file = os.open(path,os.O_RDONLY)
    file_system = os.fstat(file)[2]
    os.close(file)
    return file_system

def delete_folder(path):
    """
    Deletes a folder and it's contents.

    :param path: Folder path
    """

    shutil.rmtree(path)

def tmp_folder(path):
    """
    Creates and returns a temporary folder in the requested root path.

    :param path: Root path
    :return: Temporary folder path
    """

    while True:
        name = os.path.join(path, '.tar' + t_utils.random_name())
        if not os.path.lexists(name):
            os.mkdir(name)
            return name

def tmp_folder_same_fs(path):
    """
    Creates a temporary folder in the same file system (when possible) as the requested path.
    Returns a tuple with the path and a flag indicating if using the same FS was viable.
    When follow_links is enabled, we can always pretend to be in the same FS.

    :param path: Reference path
    :return: Tuple with temporary path and flag
    """

    base_path = os.path.dirname(os.path.abspath(path))
    path_fs = get_filesystem(base_path)

    default_tmp = config.get('tmp')
    default_tmp_fs = get_filesystem(default_tmp)
    # Prefer the default tmp
    if config.get('follow_links') or path_fs == default_tmp_fs:
        return (tmp_folder(default_tmp), True)
    # Use a hidden folder in the same path as an alternative
    if os.access(base_path, os.W_OK):
        return (tmp_folder(base_path), True)
    # The path is not writable, using the default tmp in another FS as last resort
    return (tmp_folder(default_tmp), False)
