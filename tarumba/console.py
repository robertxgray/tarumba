# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config

from rich.console import Console

import sys

def info(message):
    """
    Prints a info message to the console.

    :param message: Message to print
    """

    if config.DISABLE_COLOR:
        sys.stdout.write(message.rstrip()+'\n')
    else:
        console = Console()
        console.out(message.rstrip())

def warn(message):
    """
    Prints a warning message to the console.

    :param message: Message to print
    """

    if config.DISABLE_COLOR:
        sys.stderr.write(message.rstrip()+'\n')
    else:
        console = Console(stderr=True, style='bold yellow')
        console.out(message.rstrip())

def error(message):
    """
    Prints an error message to the console.

    :param message: Message to print
    """

    if config.DISABLE_COLOR:
        sys.stderr.write(message.rstrip()+'\n')
    else:
        console = Console(stderr=True, style='bold red')
        console.out(message.rstrip())
