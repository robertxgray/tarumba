# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import argparse
import gettext

_ = gettext.gettext

def get_arguments():
    """
    Get the command line arguments using argparse.

    :return: Input arguments
    """

    parser = argparse.ArgumentParser(prog='tarumba',
                                     description=_('The universal archive manager'))
    parser.add_argument('command', choices=['list','create','add'], help=_('Command'))
    parser.add_argument('archive', help=_('Archive file to process'))
    return parser.parse_args()
