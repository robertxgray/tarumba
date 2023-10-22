# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import console, manager, parser
from gettext import gettext as _
import sys

def main():
    """
    Main function.
    """

    try:
        args = parser.get_arguments()

        if args.command == 'list':
            listing = manager.list(args)
            console.print_listing(listing)

    # We get BrokenPipeError whenever the output is redirected, just ignore it
    except BrokenPipeError as e:
        pass
    except Exception as e:
        console.error(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': str(e)})

if __name__ == '__main__':
    main()
