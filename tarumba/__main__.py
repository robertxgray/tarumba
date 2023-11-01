# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba.gui import current as gui
from tarumba import config, manager, parser
from gettext import gettext as _

import sys

def main():
    """
    Main function.
    """

    try:
        args = parser.get_arguments()

        # List
        if args.command == 'l' or args.command == 'list':
            message = _('reading %(archive)s') % {'archive': args.archive}
            with gui.start_progress(message):
                listing = manager.list_archive(args)
                gui.print_listing(listing)
                gui.stop_progress()

        # Compress
        if args.command == 'c' or args.command == 'compress':

            if args.follow_links:
                config.set_follow_links(args.follow_links)

            message = _('compressing into %(archive)s') % {'archive': args.archive}
            with gui.start_progress(message):
                manager.compress_archive(args)
                gui.stop_progress()

    # We get BrokenPipeError whenever the output is redirected, just ignore it
    except BrokenPipeError as e:
        pass
    except KeyboardInterrupt as e:
        sys.exit(130)
    except Exception as e:
        gui.error(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': str(e)})
        raise e # TODO: Remove this
        sys.exit(1)

if __name__ == '__main__':
    main()
