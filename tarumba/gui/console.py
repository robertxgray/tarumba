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

    def info(self, message):
        """
        Prints a info message to the console.

        :param message: Message to print
        """

        console = r_console.Console(color_system=config.COLOR_SYSTEM)
        console.out(message.rstrip())

    def warn(self, message):
        """
        Prints a warning message to the console.

        :param message: Message to print
        """

        console = r_console.Console(color_system=config.COLOR_SYSTEM, stderr=True, style='bold yellow')
        console.out(message.rstrip())

    def error(self, message):
        """
        Prints an error message to the console.

        :param message: Message to print
        """

        console = r_console.Console(color_system=config.COLOR_SYSTEM, stderr=True, style='bold red')
        console.out(message.rstrip())

    def new_progress(self):
        """
        Creates a new progress bar.

        :return: Progress bar
        """
        console = r_console.Console(color_system=config.COLOR_SYSTEM)
        return r_progress.Progress(console=console)

    def print_listing(self, listing, console):
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

        console.print(table)
