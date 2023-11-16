# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's command line parser"

import argparse
from gettext import gettext as _
import os
import sys

from tarumba.gui import current as t_gui

# Ref: https://github.com/python/cpython/blob/main/Lib/argparse.py
class ColouredArgumentParser(argparse.ArgumentParser):
    "Custom argument parser with coloured output"

    def _print_message(self, message, file=None):
        if message:
            file = file or sys.stderr
            try:
                if file == sys.stderr:
                    t_gui.error(message)
                else:
                    t_gui.info(message)
            except (AttributeError, OSError):
                pass

def get_arguments():
    """
    Get the command line arguments using argparse.

    :return: Input arguments
    """

    parser = ColouredArgumentParser(prog='tarumba',
                                    description=_('The universal archive manager'))
    parser.add_argument('command', choices=['l','list','a','add','e','extract'],
        help=_('command'))
    parser.add_argument('archive',
        help=_('archive file to process'))
    parser.add_argument('files', nargs='*',
        help=_('files to add or extract'))
    parser.add_argument('-c', '--columns',
        help=_('comma separated columns to include in the listing'))
    parser.add_argument('-f', '--follow-links', action='store_true',
        help=_('follow symbolic links. WARNING: MAY CREATE INIFINITE PATHS'))
    parser.add_argument('-n', '--no-color', action='store_true',
        help=_('disable colored output'))
    parser.add_argument('-v', '--verbose', action='store_true',
        help=_('verbosely list processed files'))
    args = parser.parse_args()

    # Get the absolute archive path
    args.archive = os.path.abspath(args.archive)

    return args
