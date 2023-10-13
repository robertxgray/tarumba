# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import parser, manager
import gettext
import logging
import sys

_ = gettext.gettext
log = logging.getLogger(__name__)

def main():
    """
    Main function.
    """

    args = parser.get_arguments()

    if args.command == 'list':
        manager.list(args)

if __name__ == '__main__':
    main()
