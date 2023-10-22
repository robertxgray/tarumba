# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config
from tarumba.format import format

from rich import box
from rich.console import Console
from rich.table import Table

from gettext import gettext as _
import os
import sys

def info(message):
    """
    Prints a info message to the console.

    :param message: Message to print
    """

    console = Console(color_system=config.COLOR_SYSTEM)
    console.out(message.rstrip())

def warn(message):
    """
    Prints a warning message to the console.

    :param message: Message to print
    """

    console = Console(color_system=config.COLOR_SYSTEM, stderr=True, style='bold yellow')
    console.out(message.rstrip())

def error(message):
    """
    Prints an error message to the console.

    :param message: Message to print
    """

    console = Console(color_system=config.COLOR_SYSTEM, stderr=True, style='bold red')
    console.out(message.rstrip())

def print_listing(listing):
    """
    Prints an archive contents listing to the console.

    :param listing: Archive listing
    """

    table = Table(box=box.SIMPLE, header_style=config.LIST_HEADER_COLOR, border_style=config.LIST_BORDER_COLOR)

    for column in listing[0]:
        if column == format.NAME:
            table.add_column(_(column), style=config.LIST_NAME_COLOR)
        elif column == format.SIZE:
            table.add_column(_(column), style=config.LIST_DEFAULT_COLOR, justify='right')
        else:
            table.add_column(_(column), style=config.LIST_DEFAULT_COLOR)

    for row in listing[1:]:
        table.add_row(*row)

    console = Console(color_system=config.COLOR_SYSTEM)
    console.print(table)