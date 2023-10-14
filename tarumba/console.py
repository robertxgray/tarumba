# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config

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

    console = Console(color_system=config.COLOR)
    console.out(message.rstrip())

def warn(message):
    """
    Prints a warning message to the console.

    :param message: Message to print
    """

    console = Console(color_system=config.COLOR, stderr=True, style='bold yellow')
    console.out(message.rstrip())

def error(message):
    """
    Prints an error message to the console.

    :param message: Message to print
    """

    console = Console(color_system=config.COLOR, stderr=True, style='bold red')
    console.out(message.rstrip())

def print_listing(archive, listing):
    """
    Prints an archive contents listing to the console.

    :param listing: Archive listing
    """

    table = Table(title=os.path.basename(archive))

    for column in listing[0]:
        table.add_column(_(column))

    for row in listing[1:]:
        table.add_row(*row)

    console = Console(color_system=config.COLOR)
    console.print(table)
