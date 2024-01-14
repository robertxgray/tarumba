# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's utilities"

from gettext import gettext as _
import os
import shutil

from tarumba import utils as t_utils
from tarumba.config import current as config
from tarumba.gui import current as t_gui

def check_read_file(filename):
    """
    Check if a file is readable.

    :param filename: File name to check
    :raises PermissionError: The file is not readable
    :raises IsADirectoryError: Non-file element in the path
    :raises FileNotFoundError: No element in the path
    """

    if os.path.isfile(filename):
        if not os.access(filename, os.R_OK):
            raise PermissionError(_("can't read %(filename)s") % {'filename': filename})
    else:
        if os.path.lexists(filename):
            raise IsADirectoryError(_("%(filename)s is not a file") % {'filename': filename})
        raise FileNotFoundError(_("%(filename)s doesn't exist") % {'filename': filename})

def check_write_file(filename):
    """
    Check if a file is writable.

    :param filename: File name to check
    :raises PermissionError: The file is not writable
    :raises IsADirectoryError: Element in path is not a file
    """

    if os.path.isfile(filename):
        if not os.access(filename, os.W_OK):
            raise PermissionError(_("can't write %(filename)s") % {'filename': filename})
    else:
        if os.path.lexists(filename):
            raise IsADirectoryError(_("%(filename)s is not a file") % {'filename': filename})
        if not os.access(os.path.dirname(filename), os.W_OK):
            raise PermissionError(_("can't write %(filename)s") % {'filename': filename})

def check_write_folder(filename):
    """
    Check if a folder is writable.

    :param filename: Folder name to check
    :raises PermissionError: The folder is not writable
    :raises NotADirectoryError: Element in path is not a folder
    """

    if os.path.isdir(filename):
        if not os.access(filename, os.W_OK):
            raise PermissionError(_("can't write %(filename)s") % {'filename': filename})
    else:
        raise NotADirectoryError(_("%(filename)s is not a folder") % {'filename': filename})

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

    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)

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

    default_tmp = config.get('main_s_tmp_path')
    default_tmp_fs = get_filesystem(default_tmp)
    # Prefer the default tmp
    if config.get('main_b_follow_links') or path_fs == default_tmp_fs:
        return (tmp_folder(default_tmp), True)
    # Use a hidden folder in the same path as an alternative
    if os.access(base_path, os.W_OK):
        return (tmp_folder(base_path), True)
    # The path is not writable, using the default tmp in another FS as last resort
    return (tmp_folder(default_tmp), False)

def _check_add_file(add_args, path):
    """
    Checks if a file can be archived.

    :param add_args: AddArgs object
    :param path: Filesystem path to walk
    :raises FileNotFoundError: The file doesn't exist
    :raises IsADirectoryError: Element in path is not a file
    :raises PermissionError: The file is not readable
    :return: True if the file can be archived
    """

    if not os.path.lexists(path):
        raise FileNotFoundError(_("%(filename)s doesn't exist") % {'filename': path})
    if (not add_args.get('format').CAN_SPECIAL and not os.path.isfile(path) and
        not os.path.isdir(path) and not os.path.islink(path)):
        raise IsADirectoryError(
            _("%(format)s archive format can't store the special file %(filename)s") %
            {'format': add_args.get('format').NAME, 'filename': path})
    if not os.access(path, os.R_OK, follow_symlinks=add_args.get('follow_links')):
        raise PermissionError(_("can't read %(filename)s") % {'filename': path})

    copy = True
    if add_args.get('contents') is not None:
        file_path = path.lstrip('/')
        # Add the extra path
        if add_args.get('path'):
            file_path = os.path.join(add_args.get('path'), file_path)
        if (file_path in add_args.get('contents') and
            add_args.get('overwrite') not in (t_gui.ALL, t_gui.NONE)):
            add_args.set('overwrite', t_gui.prompt_ynan(
                _('%(filename)s already exists in %(archive)s. Do you want to overwrite?'),
                file_path, os.path.basename(add_args.get('archive'))))
            copy = add_args.get('overwrite') in (t_gui.YES, t_gui.ALL)
    return copy

def _check_add_file_copy(add_args, path, tmp_dir, copy):
    """
    Copies a file if a temporary path is given.

    :param add_args: AddArgs object
    :param path: File path
    :param tmp_dir: Tuple with temporary path and same FS flag
    :param copy: If false, skip this file
    :return: Number of files processed: 0 or 1
    """

    if tmp_dir and copy:
        file_path = path.lstrip('/')
        # Add the extra path
        if add_args.get('path'):
            file_path = os.path.join(add_args.get('path'), file_path)
        dest_path = os.path.join(tmp_dir[0], file_path)

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        if add_args.get('follow_links'):
            os.symlink(path, dest_path)
        elif tmp_dir[1]:
            try:
                os.link(path, dest_path)
            except PermissionError:
                shutil.copy2(path, dest_path, follow_symlinks=False)
        else:
            shutil.copy2(path, dest_path, follow_symlinks=False)

    return 1 if copy else 0

def _check_add_folder_copy(add_args, path, tmp_dir):
    """
    Copies a folder if a temporary path is given.

    :param add_args: AddArgs object
    :param path: Folder path
    :param tmp_dir: Tuple with temporary path and same FS flag
    :return: Number of folders, always 1
    """

    if tmp_dir:
        dir_path = path.lstrip('/')
        # Add the extra path
        if add_args.get('path'):
            dir_path = os.path.join(add_args.get('path'), dir_path)
        dest_path = os.path.join(tmp_dir[0], dir_path)
        os.makedirs(dest_path, exist_ok=True)
        shutil.copystat(path, dest_path)
    return 1

def check_add_filesystem_tree(add_args, path, tmp_dir):
    """
    Returns all the files and folders under a filesystem path.

    :param add_args: AddArgs object
    :param path: Filesystem path to walk
    :param tmp_dir: Tuple with temporary path and same FS flag
    :return: Number of files and folders
    """

    if os.path.isdir(path) and (add_args.get('follow_links') or not os.path.islink(path)):
        total = _check_add_folder_copy(add_args, path, tmp_dir)
        for root, dirs, files in os.walk(path, topdown=True,
            followlinks=add_args.get('follow_links')):
            for name in dirs:
                dirpath = os.path.join(root, name)
                total += _check_add_folder_copy(add_args, dirpath, tmp_dir)
            for name in files:
                filepath = os.path.join(root, name)
                copy = _check_add_file(add_args, filepath)
                total += _check_add_file_copy(add_args, filepath, tmp_dir, copy)
    else:
        copy = _check_add_file(add_args, path)
        total = _check_add_file_copy(add_args, path, tmp_dir, copy)
    return total

def _move_extracted_link(file, dest_path):
    """
    Links extracted files to the destination path.

    :param file: Extracted file
    :param dest_path: Destination path
    """

    if os.path.isdir(file):
        os.mkdir(dest_path)
        shutil.copystat(file, dest_path)
    else:
        os.link(file, dest_path)

def move_extracted(file, extract_args):
    """
    Move the extracted files to the destination path.

    :param file: Extracted file
    :param extract_args: ExtractArgs object
    :return: True if the file has been moved
    """

    # Calculate the destination path
    mod_file = file
    extra_path = extract_args.get('path')
    if extra_path:
        extra_path += '/'
        if file.startswith(extra_path):
            mod_file = mod_file[len(extra_path):]
        else:
            message = (_("path modification %(path)s can't be applied to %(filename)s") %
                {'path': extra_path, 'filename': file})
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': message})

    dest_path = os.path.join(extract_args.get('cwd'), mod_file)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # Destination doesn't exist
    if not os.path.lexists(dest_path):
        _move_extracted_link(file, dest_path)
        return True
    # Destination is an existing folder
    if os.path.isdir(file) and os.path.isdir(dest_path):
        return True

    if extract_args.get('overwrite') not in (t_gui.ALL, t_gui.NONE):
        extract_args.set('overwrite', t_gui.prompt_ynan(
            _('%(filename)s already exists. Do you want to overwrite?'), dest_path))
    # Overwrite destination
    if extract_args.get('overwrite') in (t_gui.YES, t_gui.ALL):
        if os.path.isdir(dest_path):
            delete_folder(dest_path)
        else:
            os.remove(dest_path)
        _move_extracted_link(file, dest_path)
        return True
    return False
