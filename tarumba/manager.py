# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import console, executor
from tarumba.format import tar

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
            console.warn(_('%(prog)s: warning: %(message)s\n') % {'prog': 'tarumba', 'message': message})
        
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

def list(args):
    """
    List archive contents.

    :param args: Input arguments
    :raises FileNotFoundError: The file 
    """

    if not os.path.isfile(args.archive) or not os.access(args.archive, os.R_OK):
        raise FileNotFoundError(_("can't read %(filename)s") % {'filename': args.archive})

    format = _detect_format(args.archive)
    if format is not None:
        commands = format.list_commands(args.archive)
        contents = executor.execute(commands)
        return format.parse_listing(contents)
