# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's archive manager"

from argparse import ArgumentError
from gettext import gettext as _
import mimetypes
import os

import magic

from tarumba import config as t_config
from tarumba import data_classes as t_data_classes
from tarumba import executor as t_executor
from tarumba import file_utils as t_file_utils
from tarumba import utils as t_utils
from tarumba.config import current as config
from tarumba.format import tar as t_tar
from tarumba.format import zip as t_zip
from tarumba.gui import current as t_gui

GZIP = 'application/gzip'
TAR = 'application/x-tar'
ZIP = 'application/zip'

def _detect_format(archive):
    """
    Detect the archive format.

    :param archive: Archive file name
    :return: Detected format
    :raises TypeError: If the format is unknown
    """

    name_mime = mimetypes.guess_type(archive, strict=False)

    if os.path.isfile(archive):
        file_mime = magic.from_file(archive, mime=True) # pylint: disable=no-member

        if name_mime[0] != TAR and name_mime[0] != file_mime:
            message = _("archive type and extension don't match")
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': message})

        if file_mime == GZIP:
            if name_mime[0] == TAR:
                pass #return targzip.TarGzip()
            else:
                pass #return gzip.Gzip()

        if file_mime == TAR:
            return t_tar.Tar()

        if file_mime == ZIP:
            return t_zip.Zip()

    else:
        if name_mime[0] == TAR and name_mime[1] == 'gzip':
            pass #return targzip.TarGzip()

        if name_mime[0] == TAR and name_mime[1] is None:
            return t_tar.Tar()

        if name_mime[0] == ZIP:
            return t_zip.Zip()

    message = _('unknown archive format')
    raise TypeError(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': message})

def _list_archive_2set(form, archive):
    """
    Returns the set of archive contents.

    :param form: Archive format
    :param archive: Archive path
    :return: Set of archive contents
    """

    commands = form.list_commands(archive)
    contents = t_executor.execute(commands)
    return form.parse_listing_2set(contents)

def list_archive(args):
    """
    List archive contents.

    :param args: Input arguments
    :raises FileNotFoundError: The archive is not readable
    """

    t_file_utils.check_read_file(args.archive)

    columns = None
    if args.columns:
        columns = t_config.parse_columns(args.columns)

    form = _detect_format(args.archive)
    t_gui.debug('format',  form)
    commands = form.list_commands(args.archive)
    contents = t_executor.execute(commands)
    return form.parse_listing(contents, columns)

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
            commands += add_args.get('form').add_commands(add_args, safe_file)
            commands.append((t_executor.CHDIR, [cwd]))
        # Move to the root when dealing with absolute paths
        elif file.startswith('/'):
            commands.append((t_executor.CHDIR, ['/']))
            commands += add_args.get('form').add_commands(add_args, safe_file)
            commands.append((t_executor.CHDIR, [cwd]))
        else:
            commands += add_args.get('form').add_commands(add_args, safe_file)
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

    add_args = t_data_classes.AddArgs()
    add_args.set('archive', args.archive)
    add_args.set('files', args.files)
    add_args.set('follow_links', config.get('follow_links'))
    add_args.set('form', _detect_format(args.archive))
    add_args.set('level', args.level)
    add_args.set('path', args.path.strip('/') if args.path else None)
    t_gui.debug('add_args', add_args)

    # Can we store multiple files?
    if not add_args.get('form').CAN_PACK:
        if os.path.isfile(add_args.get('archive')) or len(add_args.get('files')) > 1:
            raise ArgumentError(None, _("the archive can't store more than one file"))

    # Do we need to warn before overwrite?
    if not add_args.get('form').CAN_DUPLICATE and os.path.isfile(add_args.get('archive')):
        add_args.set('contents', _list_archive_2set(add_args.get('form'), add_args.get('archive')))

    try:
        # Process the files to add
        target_files, total = _add_archive_check(add_args)
        t_gui.debug('total', total)
        t_gui.update_progress_total(total)
        commands = _add_archive_commands(add_args, target_files)
        if commands:
            t_executor.execute(commands, add_args.get('form').parse_add, add_args)

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
    commands += extract_args.get('form').extract_commands(extract_args)
    commands.append((t_executor.CHDIR, [extract_args.get('cwd')]))
    return commands

def extract_archive(args):
    """
    Extract files from an archive.

    :param args: Input arguments
    """

    t_file_utils.check_read_file(args.archive)

    extract_args = t_data_classes.ExtractArgs()
    extract_args.set('archive', args.archive)
    extract_args.set('cwd', os.getcwd())
    extract_args.set('files', args.files)
    extract_args.set('form', _detect_format(args.archive))
    extract_args.set('path', args.path.strip('/') if args.path else None)
    t_gui.debug('extract_args', extract_args)

    try:
        extract_args.set('tmp_dir', t_file_utils.tmp_folder(os.getcwd()))
        t_gui.debug('mkdir', extract_args.get('tmp_dir'))
        # Process the files to extract
        commands = _extract_archive_commands(extract_args)
        if commands:
            t_executor.execute(commands, extract_args.get('form').parse_extract, extract_args)

    # Temporary folders must be deleted
    finally:
        if extract_args.get('tmp_dir'):
            t_gui.debug('rmdir', extract_args.get('tmp_dir'))
            t_file_utils.delete_folder(extract_args.get('tmp_dir'))
