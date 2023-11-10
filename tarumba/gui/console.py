# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config
from tarumba.format import format
from tarumba.gui import gui

from rich import box as r_box
from rich import console as r_console
from rich import progress as r_progress
from rich import table as r_table

from gettext import gettext as _
import os
import sys

class Console(gui.Gui):

    def __init__(self):
        self.out_c = r_console.Console(color_system=config.COLOR_SYSTEM, highlight=False)
        self.err_c = r_console.Console(color_system=config.COLOR_SYSTEM, highlight=False, stderr=True)
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

        table = r_table.Table(box=r_box.SIMPLE, header_style=config.LIST_HEADER_COLOR, border_style=config.LIST_BORDER_COLOR)

        for column in listing[0]:
            if column == format.NAME:
                table.add_column(_(column), style=config.LIST_NAME_COLOR)
            elif column == format.SIZE:
                table.add_column(_(column), style=config.LIST_DEFAULT_COLOR, justify='right')
            else:
                table.add_column(_(column), style=config.LIST_DEFAULT_COLOR)

        for row in listing[1:]:
            table.add_row(*row)

        self.out_c.print(table)
