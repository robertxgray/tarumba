# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's console interface"

from gettext import gettext as _

from rich import box as r_box
from rich import console as r_console
from rich import progress as r_progress
from rich import table as r_table

from tarumba.config import current as config
from tarumba.format import format as t_format
from tarumba.gui import gui as t_gui


class Console(t_gui.Gui):

    "Class implementing the GUI functions on console mode"

    def __init__(self):
        self.out_c = r_console.Console(
            color_system=config.get('color_system'), highlight=False)
        self.err_c = r_console.Console(
            color_system=config.get('color_system'), highlight=False, stderr=True)
        self.progress = None
        self.task = None

    # COMMON FUNCTIONS

    def info(self, message):
        """
        Prints a info message to the console.

        :param message: Message to print
        """

        self.out_c.print(message.rstrip())

    def warn(self, message):
        """
        Prints a warning message to the console.

        :param message: Message to print
        """

        self.out_c.print(message.rstrip(), style='bold yellow')

    def error(self, message):
        """
        Prints an error message to the console.

        :param message: Message to print
        """

        self.err_c.print(message.rstrip(), style='bold red')

    def start_progress(self, message):
        """
        Starts a progress bar.

        :param message: Message to include in the task
        :return: Progress bar
        """

        assert self.progress is None, _('a progress bar is already running')
        self.progress = r_progress.Progress(
            r_progress.TextColumn("[progress.description]{task.description}"),
            r_progress.BarColumn(),
            r_progress.TaskProgressColumn(),
            console=self.out_c)
        self.task = self.progress.add_task(message, total=None, transient=True)
        return self.progress

    def stop_progress(self):
        """
        Stops a progress bar.
        """

        assert self.progress is not None, _('a progress bar is not running')
        self.progress.remove_task(self.task)
        self.task = None
        self.progress = None

    def update_progress_total(self, total):
        """
        Update the progress bar total.

        :param total: Number of files
        """

        assert self.progress is not None, _('a progress bar is not running')
        self.progress.update(self.task, total=total)

    def advance_progress(self):
        """
        Advance the progress bar.

        :param file: File being processed
        """

        assert self.progress is not None, _('a progress bar is not running')
        self.progress.advance(self.task)

    # CONSOLE SPECIFIC FUNCTIONS

    def disable_color(self):
        """
        Disables the colored output.
        """

        self.out_c = r_console.Console(color_system=None, highlight=False)
        self.err_c = r_console.Console(color_system=None, highlight=False, stderr=True)

    def print_listing(self, listing):
        """
        Prints an archive contents listing to the console.

        :param listing: Archive listing
        """

        table = r_table.Table(box=r_box.SIMPLE, header_style=config.get('list_header_color'),
            border_style=config.get('list_border_color'))

        for column in listing[0]:
            if column == t_format.NAME:
                table.add_column(_(column), style=config.get('list_name_color'))
            elif column == t_format.SIZE:
                table.add_column(_(column), style=config.get('list_default_color'),
                justify='right')
            else:
                table.add_column(_(column), style=config.get('list_default_color'))

        for row in listing[1:]:
            table.add_row(*row)

        self.out_c.print(table)
