# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import console

import argparse
from gettext import gettext as _
import sys

# Ref: https://github.com/python/cpython/blob/main/Lib/argparse.py
class ColouredArgumentParser(argparse.ArgumentParser):
    "Custom argument parser with coloured output."

    def _print_message(self, message, file=None):
        if message:
            file = file or sys.stderr
            try:
                if file == sys.stderr:
                    console.error(message)
                else:
                    file.write(message)
            except (AttributeError, OSError):
                pass

def get_arguments():
    """
    Get the command line arguments using argparse.

    :return: Input arguments
    """

    parser = ColouredArgumentParser(prog='tarumba',
                                    description=_('The universal archive manager'))
    parser.add_argument('command', choices=['list','create','add'], help=_('command'))
    parser.add_argument('archive', help=_('archive file to process'))
    return parser.parse_args()
