# Copyright: (c) 2024, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's constants"

# Supported backends
BACKEND_7ZIP = '7zip'
BACKEND_TAR = 'tar'

# Columns in archive contents
COLUMN_CRC = 'CRC'
COLUMN_DATE = 'DATE'
COLUMN_ENC = 'ENCRYPTED'
COLUMN_METHOD = 'METHOD'
COLUMN_NAME = 'NAME'
COLUMN_OWNER = 'OWNER'
COLUMN_PACKED = 'PACKED'
COLUMN_PERMS = 'PERMISSIONS'
COLUMN_SIZE = 'SIZE'

# Set to check if a column exists
COLUMNS_SET = {
    COLUMN_CRC,
    COLUMN_DATE,
    COLUMN_ENC,
    COLUMN_METHOD,
    COLUMN_NAME,
    COLUMN_OWNER,
    COLUMN_PACKED,
    COLUMN_PERMS,
    COLUMN_SIZE
}

# Mime types
MIME_7Z = 'application/x-7z-compressed'
MIME_BROTLI = 'application/x-brotli'
MIME_BZIP2 = 'application/x-bzip2'
MIME_COMPRESS = 'application/x-compress'
MIME_GZIP = 'application/gzip'
MIME_LZMA = 'application/x-lzma'
MIME_TAR = 'application/x-tar'
MIME_ZIP = 'application/zip'
MIME_XZ = 'applicaiton/x-xz'

# Backend operations
OPERATION_LIST = 'LIST'
OPERATION_ADD = 'ADD'
OPERATION_EXTRACT = 'EXTRACT'
OPERATION_RENAME = 'RENAME'
OPERATION_TEST = 'TEST'
