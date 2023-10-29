# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba.gui import current as gui
from tarumba import config, executor, utils
from tarumba.format import tar

from argparse import ArgumentError
from gettext import gettext as _
import magic
import mimetypes
import os

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
        file_mime = magic.from_file(archive, mime=True)

        if name_mime[0] != TAR and name_mime[0] != file_mime:
            message = _("archive type and extension don't match")
            gui.warn(_('%(prog)s: warning: %(message)s\n') % {'prog': 'tarumba', 'message': message})
        
        if file_mime == GZIP:
            if name_mime[0] == TAR:
                pass #return targzip.TarGzip()
            else:
                pass #return gzip.Gzip()

        if file_mime == TAR:
            return tar.Tar()

    else:
        if name_mime[0] == TAR and name_mime[1] == 'gzip':
            pass #return targzip.TarGzip()

        if name_mime[0] == TAR and name_mime[1] is None:
            return tar.Tar()

    message = _('unknown archive format')
    raise TypeError(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': message})

def list_archive(args):
    """
    List archive contents.

    :param args: Input arguments
    :raises FileNotFoundError: The archive is not readable
    """

    utils.check_read(args.archive)

    columns = None
    if args.columns:
        columns = config.parse_columns(args.columns)

    format = _detect_format(args.archive)
    commands = format.list_commands(args.archive)
    contents = executor.execute(commands)
    return format.parse_listing(contents, columns)

def compress_archive(args):
    """
    Compress files into an archive.

    :param args: Input arguments
    """

    if len(args.files) < 1:
        raise ArgumentError(None, _("expected a list of files to compress"))

    utils.check_write(args.archive)

    format = _detect_format(args.archive)

    for file in args.files:
        tree = utils.get_filesystem_tree(file)
        commands = format.compress_commands(args.archive, file)
        executor.execute(commands)
