# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's archive classifier"

from gettext import gettext as _
import mimetypes
import os

import magic # pylint: disable=import-error

import tarumba.constants as t_constants
from tarumba.backend import x7z as t_x7z
from tarumba.backend import tar as t_tar
from tarumba.gui import current as t_gui

# Enrich the mimetypes maps
mimetypes.types_map['.7z'] = t_constants.MIME_7Z
mimetypes.encodings_map['.br'] = t_constants.MIME_BROTLI
mimetypes.encodings_map['.gz'] = t_constants.MIME_GZIP
mimetypes.encodings_map['.Z'] = t_constants.MIME_COMPRESS
mimetypes.encodings_map['.bz2'] = t_constants.MIME_BZIP2
mimetypes.encodings_map['.lz'] = t_constants.MIME_LZMA
mimetypes.encodings_map['.lzma'] = t_constants.MIME_LZMA
mimetypes.encodings_map['.xz'] = t_constants.MIME_XZ

def _sanitize_mime(mime):
    """
    Sanitize a mime type.

    :param mime: Tuple (type, encoding)
    :return: Tuple (type, encoding)
    """

    _type, _encoding = mime
    if _type == t_constants.MIME_TAR:
        return mime
    if _encoding is not None:
        return (_encoding, None)
    return (_type, None)

def detect_format(backend, archive, operation):
    """
    Detect the archive format and returns a backend to handle it.

    :param backend: Selected backend
    :param archive: Archive file name
    :param operation: Backend operation
    :return: Backend
    :raises TypeError: If the format is unknown
    """

    name_mime = _sanitize_mime(mimetypes.guess_type(archive, strict=False))
    t_gui.debug('name_mime', name_mime)
    mime = name_mime

    if os.path.isfile(archive):
        magic_mime = magic.Magic(mime=True)
        magic_mime_unc = magic.Magic(mime=True, uncompress=True)
        file_mime = _sanitize_mime((magic_mime_unc.from_file(archive),
                                    magic_mime.from_file(archive)))
        t_gui.debug('file_mime', file_mime)
        if name_mime[0] != file_mime[0]:
            message = _("detected archive type and extension don't match")
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': message})
        mime = file_mime

    if backend:
        if backend == t_constants.BACKEND_7ZIP:
            return t_x7z.X7z(mime, operation)
        if backend == t_constants.BACKEND_TAR:
            return t_tar.Tar(mime, operation)

    if mime[0] == t_constants.MIME_TAR:
        return t_tar.Tar(mime, operation)
    return t_x7z.X7z(mime, operation)

    # TODO
    #message = _('unknown archive format')
    #raise TypeError(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': message})
