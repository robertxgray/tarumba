# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba.format import format

from gettext import gettext as _
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

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

# Compression options
FOLLOW_LINKS = False

def set_follow_links(follow_links):
    """
    Updates the value of FOLLOW_LINKS.

    :param follow_links: New boolean value
    """

    global FOLLOW_LINKS
    FOLLOW_LINKS = follow_links

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
