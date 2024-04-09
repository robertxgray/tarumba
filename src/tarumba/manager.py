# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's archive manager"

import os
from argparse import ArgumentError
from gettext import gettext as _

import tarumba.constants as t_constants
from tarumba import classifier as t_classifier
from tarumba import config as t_config
from tarumba import data_classes as t_data_classes
from tarumba import executor as t_executor
from tarumba import file_utils as t_file_utils
from tarumba import utils as t_utils
from tarumba.config import current as config
from tarumba.gui import current as t_gui

PAIR = 2

def _list_archive_2set(backend, archive):
    """
    Returns the set of archive contents.

    :param backend: Backend
    :param archive: Archive path
    :return: Set of archive contents
    """

    list_args = t_data_classes.ListArgs()
    list_args.put('archive', archive)
    list_args.put('files', [])
    list_args.put('backend', backend)
    list_args.put('output', set())
    t_gui.debug('list_args', list_args)

    commands = backend.list_commands(list_args)
    t_executor.Executor().execute(commands, list_args.get('backend').LIST_PATTERNS,
        list_args.get('backend').parse_list, list_args)
    return list_args.get('output')

def list_archive(args):
    """
    List archive contents.

    :param args: Input arguments
    """

    t_file_utils.check_read_file(args.archive)

    list_args = t_data_classes.ListArgs()
    list_args.put('archive', args.archive)
    list_args.put('columns', t_config.parse_columns(args.columns))
    list_args.put('files', args.files)
    list_args.put('backend', t_classifier.detect_format(args.backend, args.archive,
        t_constants.OPERATION_LIST))
    list_args.put('occurrence', args.occurrence)
    list_args.put('output', [])
    # Make sure the headers are added on empty archives
    t_utils.get_list_columns(list_args.get('columns'), config.get('main_l_list_columns'),
        list_args.get('output'))
    t_gui.debug('list_args', list_args)

    commands = list_args.get('backend').list_commands(list_args)
    t_executor.Executor().execute(commands, list_args.get('backend').LIST_PATTERNS,
        list_args.get('backend').parse_list, list_args)
    return list_args.get('output')

def _get_overwrite(args):
    """
    Determines the initial value for the overwrite variable.

    :param args: Input arguments
    :return: Overwrite value
    """

    if args.never_overwrite:
        return t_gui.NONE
    if args.always_overwrite:
        return t_gui.ALL
    return None

def _add_archive_get_password(backend, archive, encrypt):
    """
    Checks if encryption is required and prompts for a password when needed.

    :param encrypt: Encryption flag
    :param backend: Archive backend
    :raises ArgumentError: Encryption not available
    """

    password = None
    if encrypt:
        if backend.can_encrypt():
            password = t_utils.new_password(archive)
        else:
            raise ArgumentError(None, _("this archive format can't encrypt contents"))
    return password

def _add_archive_check_multiple(add_args):
    """
    Checks if the archive can store multiple and the operation is valid.

    :param add_args: AddArgs object
    :raises ArgumentError: Invalid operation
    """

    if not add_args.get('backend').can_pack():
        if (os.path.isfile(add_args.get('archive')) or
            len(add_args.get('files')) > 1 or
            os.path.isdir(add_args.get('files')[0])):
            raise ArgumentError(None, _("this archive format can't store more than one file"))
        if add_args.get('path'):
            raise ArgumentError(None, _("this archive format can't store file paths"))
        if not add_args.get('follow_links') and os.path.islink(add_args.get('files')[0]):
            raise ArgumentError(None, _("this archive format can't store links"))

def _add_archive_check(add_args):
    """
    Check the files to add and copy if needed. Updates the list of temporary folders. Existing
    files will be prompted to overrite if the format cannot store multiple files with the same
    path.

    :param add_args: AddArgs object
    :return: Tuple with target files and total
    """

    target_files = []
    total = 0
    # Copy is required for custom paths and exclusions
    copy = add_args.get('path') or add_args.get('contents') is not None
    safe_files = t_utils.safe_filelist(add_args.get('files'))
    for file in safe_files:
        t_gui.debug('file', file)
        tmp_dir = None
        if copy:
            tmp_dir = t_file_utils.tmp_folder_same_fs(file)
            t_gui.debug('mkdir', tmp_dir)
            add_args.get('tmp_dirs').append(tmp_dir[0])
        numfiles = t_file_utils.check_add_filesystem_tree(add_args, file, tmp_dir)
        if numfiles > 0:
            target_files.append(file)
            total += numfiles
    return (target_files, total)

def _add_archive_commands(add_args, files):
    """
    Generates the commands to add the files.

    :param add_args: AddArgs object
    :param files: List of files
    :return: List of commands
    """

    cwd = os.getcwd()
    commands = []
    index = 0
    for file in files:
        safe_file = file.lstrip('/')
        # Add the extra path
        if add_args.get('path'):
            safe_file = os.path.join(add_args.get('path'), safe_file)
        # Move to the temporary folders
        if add_args.get('tmp_dirs'):
            commands.append((t_executor.CHDIR, [add_args.get('tmp_dirs')[index]]))
            commands += add_args.get('backend').add_commands(add_args, safe_file)
            commands.append((t_executor.CHDIR, [cwd]))
        # Move to the root when dealing with absolute paths
        elif file.startswith('/'):
            commands.append((t_executor.CHDIR, ['/']))
            commands += add_args.get('backend').add_commands(add_args, safe_file)
            commands.append((t_executor.CHDIR, [cwd]))
        else:
            commands += add_args.get('backend').add_commands(add_args, safe_file)
        index += 1
    return commands

def add_archive(args):
    """
    Add files to an archive.

    :param args: Input arguments
    """

    if len(args.files) < 1:
        raise ArgumentError(None, _("expected a list of files to add"))

    t_file_utils.check_write_file(args.archive)

    backend = t_classifier.detect_format(args.backend, args.archive, t_constants.OPERATION_ADD)
    add_args = t_data_classes.AddArgs()
    add_args.put('archive', args.archive)
    add_args.put('files', args.files)
    add_args.put('follow_links', config.get('main_b_follow_links'))
    add_args.put('backend', backend)
    add_args.put('level', args.level)
    add_args.put('overwrite', _get_overwrite(args))
    add_args.put('owner', args.owner)
    add_args.put('password', _add_archive_get_password(backend, args.archive, args.encrypt))
    add_args.put('path', args.path.strip('/') if args.path else None)
    add_args.put('tmp_dirs', [])
    t_gui.debug('add_args', add_args)

    _add_archive_check_multiple(add_args)

    # Do we need to warn before overwrite?
    if not add_args.get('backend').can_duplicate() and os.path.isfile(add_args.get('archive')):
        add_args.put('contents',
            _list_archive_2set(add_args.get('backend'), add_args.get('archive')))

    try:
        # Process the files to add
        target_files, total = _add_archive_check(add_args)
        t_gui.debug('total', total)
        t_gui.update_progress_total(total)
        commands = _add_archive_commands(add_args, target_files)
        if commands:
            t_executor.Executor().execute(commands, add_args.get('backend').ADD_PATTERNS,
                add_args.get('backend').parse_add, add_args)

    # Temporary folders must be deleted
    finally:
        for tmp_dir in add_args.get('tmp_dirs'):
            t_gui.debug('rmdir', tmp_dir)
            t_file_utils.delete_folder(tmp_dir)

def _extract_archive_commands(extract_args):
    """
    Generates the commands to extract the files.

    :param add_args: ExtractArgs object
    :return: List of commands
    """

    commands = []
    commands.append((t_executor.CHDIR, [extract_args.get('tmp_dir')]))
    commands += extract_args.get('backend').extract_commands(extract_args)
    commands.append((t_executor.CHDIR, [extract_args.get('destination')]))
    return commands

def extract_archive(args):
    """
    Extract files from an archive.

    :param args: Input arguments
    """

    t_file_utils.check_read_file(args.archive)

    backend = t_classifier.detect_format(args.backend, args.archive, t_constants.OPERATION_EXTRACT)

    list_args = t_data_classes.ListArgs()
    list_args.put('archive', args.archive)
    list_args.put('columns', [t_constants.COLUMN_NAME])
    list_args.put('files', args.files)
    list_args.put('backend', backend)
    list_args.put('output', [])
    t_gui.debug('list_args', list_args)

    extract_args = t_data_classes.ExtractArgs()
    extract_args.put('archive', args.archive)
    extract_args.put('destination', os.getcwd())
    extract_args.put('create_folder', config.get('main_s_create_folder'))
    extract_args.put('files', args.files)
    extract_args.put('backend', backend)
    extract_args.put('occurrence', args.occurrence)
    extract_args.put('overwrite', _get_overwrite(args))
    extract_args.put('path', args.path.strip('/') if args.path else None)
    t_gui.debug('extract_args', extract_args)

    try:
        # Get the archive contents
        list_commands = extract_args.get('backend').list_commands(list_args)
        t_executor.Executor().execute(list_commands, list_args.get('backend').LIST_PATTERNS,
            list_args.get('backend').parse_list, list_args)
        extract_args.put('contents', t_utils.output_2_contents(list_args.get('output')))
        extract_args.put('password', list_args.get('password'))
        t_file_utils.check_extract_create_folder(extract_args)
        total = len(extract_args.get('contents'))
        t_gui.debug('total', total)
        t_gui.update_progress_total(total)
        # Use a temporary folder
        extract_args.put('tmp_dir', t_file_utils.tmp_folder(os.getcwd()))
        t_gui.debug('mkdir', extract_args.get('tmp_dir'))
        # Process the files to extract
        extract_commands = _extract_archive_commands(extract_args)
        if extract_commands:
            t_executor.Executor().execute(extract_commands,
                extract_args.get('backend').EXTRACT_PATTERNS,
                extract_args.get('backend').parse_extract, extract_args)

    # Temporary folders must be deleted
    finally:
        if extract_args.get('tmp_dir'):
            t_gui.debug('rmdir', extract_args.get('tmp_dir'))
            t_file_utils.delete_folder(extract_args.get('tmp_dir'))

def delete_archive(args):
    """
    Delete archive contents.

    :param args: Input arguments
    """

    if len(args.files) < 1:
        raise ArgumentError(None, _("expected a list of files to delete"))

    t_file_utils.check_write_file(args.archive)

    delete_args = t_data_classes.DeleteArgs()
    delete_args.put('archive', args.archive)
    delete_args.put('files', args.files)
    delete_args.put('backend', t_classifier.detect_format(args.backend, args.archive,
        t_constants.OPERATION_RENAME))
    delete_args.put('occurrence', args.occurrence)
    t_gui.debug('delete_args', delete_args)

    commands = delete_args.get('backend').delete_commands(delete_args)
    t_executor.Executor().execute(commands, delete_args.get('backend').DELETE_PATTERNS,
        delete_args.get('backend').parse_delete, delete_args)

def rename_archive(args):
    """
    Rename archive contents.

    :param args: Input arguments
    """

    if len(args.files) < PAIR or len(args.files) % PAIR != 0:
        raise ArgumentError(None,
            _("renaming requires pairs of file names, the current name and the new name"))

    t_file_utils.check_write_file(args.archive)

    rename_args = t_data_classes.RenameArgs()
    rename_args.put('archive', args.archive)
    rename_args.put('files', args.files)
    rename_args.put('backend', t_classifier.detect_format(args.backend, args.archive,
        t_constants.OPERATION_RENAME))
    rename_args.put('occurrence', args.occurrence)
    t_gui.debug('rename_args', rename_args)

    commands = rename_args.get('backend').rename_commands(rename_args)
    t_executor.Executor().execute(commands, rename_args.get('backend').RENAME_PATTERNS,
        rename_args.get('backend').parse_rename, rename_args)

def test_archive(args):
    """
    Test archive contents.

    :param args: Input arguments
    """

    t_file_utils.check_read_file(args.archive)

    test_args = t_data_classes.TestArgs()
    test_args.put('archive', args.archive)
    test_args.put('files', args.files)
    test_args.put('backend', t_classifier.detect_format(args.backend, args.archive,
        t_constants.OPERATION_TEST))
    test_args.put('occurrence', args.occurrence)
    t_gui.debug('test_args', test_args)

    commands = test_args.get('backend').test_commands(test_args)
    t_executor.Executor().execute(commands, test_args.get('backend').TEST_PATTERNS,
        test_args.get('backend').parse_test, test_args)
