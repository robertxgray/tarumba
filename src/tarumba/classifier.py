# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's archive classifier"

from gettext import gettext as _
import mimetypes
import os

import magic # pylint: disable=import-error

from tarumba.backend import _7z as t_7z
from tarumba.backend import tar as t_tar
from tarumba.gui import current as t_gui

_7Z = 'application/x-7z-compressed'
BROTLI = 'application/x-brotli'
BZIP2 = 'application/x-bzip2'
COMPRESS = 'application/x-compress'
GZIP = 'application/gzip'
LZMA = 'application/x-lzma'
TAR = 'application/x-tar'
ZIP = 'application/zip'
XZ = 'applicaiton/x-xz'

ERROR = 'application/x-decompression-error-gzip-'

# Enrich the mimetypes maps
mimetypes.types_map['.7z'] = _7Z
mimetypes.encodings_map['.br'] = BROTLI
mimetypes.encodings_map['.gz'] = GZIP
mimetypes.encodings_map['.Z'] = COMPRESS
mimetypes.encodings_map['.bz2'] = BZIP2
mimetypes.encodings_map['.lz'] = LZMA
mimetypes.encodings_map['.lzma'] = LZMA
mimetypes.encodings_map['.xz'] = XZ

def _sanitize_mime(mime):
    """
    Sanitize a mime type.

    :param mime: Tuple (type, encoding)
    :return: Tuple (type, encoding)
    """

    _type, _encoding = mime
    if _type == TAR:
        return mime
    if (_type is None or _type == ERROR) and _encoding is not None:
        return (mime[1], None)
    return (mime[0], None)

def detect_format(archive):
    """
    Detect the archive format and returns a backend to handle it.

    :param archive: Archive file name
    :return: Backend
    :raises TypeError: If the format is unknown
    """

    name_mime = _sanitize_mime(mimetypes.guess_type(archive, strict=False))
    mime = name_mime

    if os.path.isfile(archive):
        magic_mime = magic.Magic(mime=True)
        magic_mime_unc = magic.Magic(mime=True, uncompress=True)
        file_mime = _sanitize_mime((magic_mime_unc.from_file(archive),
                                    magic_mime.from_file(archive)))
        if name_mime[0] != file_mime[0]:
            message = _("detected archive type and extension don't match")
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': message})
        mime = file_mime

    if mime[0] == TAR:
        return t_tar.Tar(mime)
    return t_7z._7z(mime)

    # TODO
    #message = _('unknown archive format')
    #raise TypeError(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': message})
