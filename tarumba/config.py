# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba.format import format

from gettext import gettext as _

# Colors
COLOR_SYSTEM = 'auto'
LIST_HEADER_COLOR = 'blue'
LIST_BORDER_COLOR = 'bright_black'
LIST_NAME_COLOR = 'cyan'
LIST_DEFAULT_COLOR = 'default'

# Binary paths
CAT_BIN = 'cat'
TAR_BIN = 'tar'

# Default lists
TAR_COLUMNS = [format.NAME, format.SIZE, format.DATE, format.PERMS, format.OWNER]

def parse_columns(col_string):
    """
    Parse a list of columns.

    :param col_string: Text describing a list of columns
    :return: List of columns
    :raises ValueError: A column name is invalid
    """

    output = []
    columns = col_string.split(',')
    for column in columns:
        formatted = column.strip().upper()
        if formatted in format.COLUMNS_SET:
            output.append(formatted)
        else:
            raise ValueError(_('invalid column name: %(column)s') % {'column': column.strip()})
    return output
