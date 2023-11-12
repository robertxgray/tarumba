# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's archive manager"

from argparse import ArgumentError
from gettext import gettext as _
import mimetypes
import os
import re

import magic

from tarumba.gui import current as t_gui
from tarumba import config as t_config
from tarumba import executor as t_executor
from tarumba import utils as t_utils
from tarumba.format import tar as t_tar

GZIP = 'application/gzip'
TAR = 'application/x-tar'

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

    else:
        if name_mime[0] == TAR and name_mime[1] == 'gzip':
            pass #return targzip.TarGzip()

        if name_mime[0] == TAR and name_mime[1] is None:
            return t_tar.Tar()

    message = _('unknown archive format')
    raise TypeError(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': message})

def list_archive(args):
    """
    List archive contents.

    :param args: Input arguments
    :raises FileNotFoundError: The archive is not readable
    """

    t_utils.check_read(args.archive)

    columns = None
    if args.columns:
        columns = t_config.parse_columns(args.columns)

    form = _detect_format(args.archive)
    commands = form.list_commands(args.archive)
    contents = t_executor.execute(commands)
    return form.parse_listing(contents, columns)

def add_archive(args):
    """
    Add files to an archive.

    :param args: Input arguments
    """

    if len(args.files) < 1:
        raise ArgumentError(None, _("expected a list of files to add"))

    t_utils.check_write(args.archive)

    form = _detect_format(args.archive)

    # Remove duplicate slashes
    safe_files = []
    for file in args.files:
        safe_files.append(re.sub('/+', '/', file))

    total = 0
    for file in safe_files:
        total += t_utils.count_filesystem_tree(file)

    t_gui.update_progress_total(total)

    for file in safe_files:
        commands = form.add_commands(args.archive, file)
        t_executor.execute(commands, form.parse_add)
