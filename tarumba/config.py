# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's global configuration"

from gettext import gettext as _
import os

import tarumba.data_classes as t_data_classes
from tarumba.format import format as t_format

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

class Config(t_data_classes.Base):
    "Global configuration class"

    dictionary = {
        'debug': False,
        # Colors
        'color_system': 'auto',
        'list_header_color': 'blue',
        'list_border_color': 'bright_black',
        'list_name_color': 'cyan',
        'list_default_color': 'default',
        # Compression options
        'follow_links': False,
        'verbose': False,
        # Paths
        'tmp': '/tmp',
        'tar_bin': 'tar',
        'zip_bin': 'zip',
        'unzip_bin': 'unzip',
        # Default columns
        'tar_columns': [t_format.PERMS, t_format.SIZE, t_format.DATE, t_format.NAME],
        'zip_columns': [t_format.PERMS, t_format.SIZE, t_format.DATE, t_format.NAME]
    }

current = Config()

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
        if formatted in t_format.COLUMNS_SET:
            output.append(formatted)
        else:
            raise ValueError(_('invalid column name: %(column)s') % {'column': column.strip()})
    return output
