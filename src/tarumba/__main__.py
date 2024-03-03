# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's main function"

from gettext import gettext as _
import os
import sys

from tarumba import manager as t_manager
from tarumba import cmd_parser as t_cmd_parser
from tarumba.config import current as config
from tarumba.gui import current as t_gui

def main():
    """
    Main function.
    """

    try:
        args = t_cmd_parser.get_arguments()

        # Options
        if args.debug:
            config.set('main_b_debug', args.debug)
            t_gui.debug('args', args)
        if args.follow_links:
            config.set('main_b_follow_links', args.follow_links)
        if args.verbose:
            config.set('main_b_verbose', args.verbose)
        if args.no_color:
            t_gui.disable_color()

        basename = os.path.basename(args.archive)

        # List
        if args.command in ('l', 'list'):
            message = _('reading')
            with t_gui.start_progress(message, basename):
                listing = t_manager.list_archive(args)
                t_gui.print_listing(listing)
                t_gui.stop_progress()

        # Compress
        if args.command in ('a', 'add'):
            message = _('adding files to')
            with t_gui.start_progress(message, basename):
                t_manager.add_archive(args)
                t_gui.stop_progress()

        # Extract
        if args.command in ('e', 'extract'):
            message = _('extracting files from')
            with t_gui.start_progress(message, basename):
                t_manager.extract_archive(args)
                t_gui.stop_progress()

    # We get BrokenPipeError whenever the output is redirected, just ignore it
    except BrokenPipeError:
        t_gui.stop_progress()
    except KeyboardInterrupt:
        t_gui.stop_progress()
        sys.exit(130)
    except Exception as ex: # pylint: disable=broad-except
        t_gui.stop_progress()
        t_gui.error(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': str(ex)})
        t_gui.print_exception()
        sys.exit(1)

if __name__ == '__main__':
    main()
