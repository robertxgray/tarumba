# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config
from tarumba.format import format
from tarumba.gui import gui

from rich import box, console, table

from gettext import gettext as _
import os
import sys

class Console(gui.Gui):

    def info(self, message):
        """
        Prints a info message to the console.

        :param message: Message to print
        """

        con = console.Console(color_system=config.COLOR_SYSTEM)
        con.out(message.rstrip())

    def warn(self, message):
        """
        Prints a warning message to the console.

        :param message: Message to print
        """

        con = console.Console(color_system=config.COLOR_SYSTEM, stderr=True, style='bold yellow')
        con.out(message.rstrip())

    def error(self, message):
        """
        Prints an error message to the console.

        :param message: Message to print
        """

        con = console.Console(color_system=config.COLOR_SYSTEM, stderr=True, style='bold red')
        con.out(message.rstrip())

    def print_listing(self, listing):
        """
        Prints an archive contents listing to the console.

        :param listing: Archive listing
        """

        tab = table.Table(box=box.SIMPLE, header_style=config.LIST_HEADER_COLOR, border_style=config.LIST_BORDER_COLOR)

        for column in listing[0]:
            if column == format.NAME:
                tab.add_column(_(column), style=config.LIST_NAME_COLOR)
            elif column == format.SIZE:
                tab.add_column(_(column), style=config.LIST_DEFAULT_COLOR, justify='right')
            else:
                tab.add_column(_(column), style=config.LIST_DEFAULT_COLOR)

        for row in listing[1:]:
            tab.add_row(*row)

        con = console.Console(color_system=config.COLOR_SYSTEM)
        con.print(tab)
