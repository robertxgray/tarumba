# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's global configuration"

import configparser
from gettext import gettext as _
import os

import tarumba.data_classes as t_data_classes
from tarumba.format import format as t_format

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.expanduser('~/.local/share/tarumba')
CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.ini')

class Config(t_data_classes.Base):
    "Global configuration class"

    def __init__(self):
        """
        Initialize the dictionary.
        """

        super().__init__()
        self.dictionary = {
            'main_b_debug': False,
            'main_b_follow_links': False,
            'main_s_tmp_path': '/tmp',
            'main_b_verbose': False,
            # Colors
            'colors_s_system': 'auto',
            'colors_s_debug': 'bright_black',
            'colors_s_info': 'default',
            'colors_s_warn': 'bold yellow',
            'colors_s_error': 'bold red',
            'colors_s_list_header': 'blue',
            'colors_s_list_border': 'bright_black',
            'colors_s_list_name': 'cyan',
            'colors_s_list_default': 'default',
            'colors_s_progress_back': 'black',
            'colors_s_progress_complete': 'magenta',
            'colors_s_progress_finished': 'green',
            'colors_s_progress_pulse': 'magenta',
            'colors_s_progress_percentage': 'magenta',
            'colors_s_prompt': 'default',
            'colors_s_prompt_choices': 'bold magenta',
            'colors_s_prompt_default': 'bold cyan',
            'colors_s_prompt_invalid': 'red',
            'colors_s_prompt_invalid_choice': 'red',
            # Tar
            'tar_s_tar_bin': 'tar',
            'tar_l_columns': [t_format.PERMS, t_format.SIZE, t_format.DATE, t_format.NAME],
            # Zip
            'zip_s_zip_bin': 'zip',
            'zip_s_unzip_bin': 'unzip',
            'zip_l_columns': [t_format.PERMS, t_format.SIZE, t_format.DATE, t_format.NAME]
        }

def parse_columns(col_string):
    """
    Parse a list of columns.

    :param col_string: Text describing a list of columns
    :return: List of columns or None if no input
    :raises ValueError: A column name is invalid
    """

    if not col_string:
        return None

    output = []
    columns = col_string.split(',')
    for column in columns:
        formatted = column.strip().upper()
        if formatted in t_format.COLUMNS_SET:
            output.append(formatted)
        else:
            raise ValueError(_('invalid column name: %(column)s') % {'column': column.strip()})
    return output

def _config_2_init(config, parser):
    """
    Saves the configuration into a init file.

    :param config: Configuration
    :param parser: Init parser
    """

    for dict_key in config.dictionary:
        cfg_section, cfg_type, cfg_key = dict_key.split('_', 2)
        if cfg_section not in parser.sections():
            parser.add_section(cfg_section)
        if cfg_type == 'l':
            value = ' '.join(current.get(dict_key))
        else:
            value = str(current.get(dict_key))
        parser.set(cfg_section, cfg_key, value)

def _init_2_config(config, parser):
    """
    Loads the configuration form a init file.

    :param config: Configuration
    :param parser: Init parser
    """

    for dict_key in config.dictionary:
        cfg_section, cfg_type, cfg_key = dict_key.split('_', 2)
        if parser.get(cfg_section, cfg_key, fallback=None) is not None:
            if cfg_type == 'b':
                value = parser.getboolean(cfg_section, cfg_key)
            elif cfg_type == 'l':
                value = parser.get(cfg_section, cfg_key).split()
            else:
                value = parser.get(cfg_section, cfg_key)
            current.set(dict_key, value)

def _parse_config():
    """
    Parses the user configuration.
    If the file doesn't exist, it will be created with default values.
    """

    parser = configparser.ConfigParser()
    os.makedirs(CONFIG_PATH, exist_ok=True)
    if os.path.isfile(CONFIG_FILE):
        parser.read(CONFIG_FILE, encoding='utf-8')
        _init_2_config(current, parser)
    else:
        _config_2_init(current, parser)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as config_file:
            parser.write(config_file)

# Init the configuration
current = Config()
_parse_config()
