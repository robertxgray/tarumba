# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba.gui import current as gui
from tarumba import manager, parser
from gettext import gettext as _

import sys

def main():
    """
    Main function.
    """

    try:
        args = parser.get_arguments()

        if args.command == 'list':
            with gui.new_progress() as progress:
                msg = _('reading %(archive)s') % {'archive': args.archive}
                task = progress.add_task(msg, total=None, transient=True)  
                listing = manager.list(args)
                gui.print_listing(listing, progress.console)
                progress.update(task, visible=False)

    # We get BrokenPipeError whenever the output is redirected, just ignore it
    except BrokenPipeError as e:
        pass
    except KeyboardInterrupt as e:
        sys.exit(130)
    except Exception as e:
        gui.error(_('%(prog)s: error: %(message)s\n') % {'prog': 'tarumba', 'message': str(e)})
        sys.exit(1)

if __name__ == '__main__':
    main()
