# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's console interface"

from gettext import gettext as _
import shlex

from rich import box as r_box
from rich import console as r_console
from rich import progress as r_progress
from rich import prompt as r_prompt
from rich import table as r_table

from tarumba.config import current as config
from tarumba.format import format as t_format
from tarumba.gui import gui as t_gui


class Console(t_gui.Gui):
    "Class implementing the GUI functions on console mode"

    # Special chars
    UP = "\x1b[1A"
    CLEAR = "\x1b[2K"

    def __init__(self):
        self.out_c = r_console.Console(
            color_system=config.get('colors_s_system'), highlight=False)
        self.err_c = r_console.Console(
            color_system=config.get('colors_s_system'), highlight=False, stderr=True)
        self.progress = None
        self.task = None

    # COMMON FUNCTIONS

    def debug(self, key, value):
        """
        Prints a debugging information.

        :param message: Message to print
        """

        if config.get('main_b_debug'):
            self.out_c.out((f'{key.upper()}: {value}').rstrip(), style='bright_black')

    def info(self, message):
        """
        Prints a info message to the console.

        :param message: Message to print
        """

        self.out_c.out(message.rstrip())

    def warn(self, message):
        """
        Prints a warning message to the console.

        :param message: Message to print
        """

        self.out_c.out(message.rstrip(), style='bold yellow')

    def error(self, message):
        """
        Prints an error message to the console.

        :param message: Message to print
        """

        self.err_c.out(message.rstrip(), style='bold red')

    def prompt_password(self, message):
        """
        Prompts for a password.

        :param message: Message to print
        :return: Password
        """

        self._pause_progress()
        password = r_prompt.Prompt.ask(message, console=self.out_c, password=True)
        self._resume_progress()
        return password

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

    def prompt_ynan(self, message):
        """
        Prompts the user a yes/no/all/none question.

        :param message: Question message
        :return: 
        """

        self._pause_progress()
        choices = [_('yes'), _('no'), _('all'), _('none')]
        answer = r_prompt.Prompt.ask(message, console=self.out_c, choices=choices, default=_('no'))
        self._resume_progress()

        if answer == _('yes'):
            return self.YES
        if answer == _('no'):
            return self.NO
        if answer == _('all'):
            return self.ALL
        return self.NONE

    # CONSOLE SPECIFIC FUNCTIONS

    def _pause_progress(self):
        """
        Pauses the progress bar.
        """

        if self.progress is not None:
            self.progress.stop()
            self._clear_line()

    def _resume_progress(self):
        """
        Resumes the progress bar.
        """

        if self.progress is not None:
            self.progress.start()

    def _clear_line(self):
        """
        Clears the last line.
        """

        print(self.UP + self.CLEAR + self.UP)

    def disable_color(self):
        """
        Disables the colored output.
        """

        self.out_c = r_console.Console(color_system=None, highlight=False)
        self.err_c = r_console.Console(color_system=None, highlight=False, stderr=True)

    def print_exception(self):
        """
        Prints a traceback for the current exception.
        """

        if config.get('main_b_debug'):
            self.err_c.print_exception(show_locals=True)

    def print_listing(self, listing):
        """
        Prints an archive contents listing to the console.

        :param listing: Archive listing
        """

        table = r_table.Table(box=r_box.SIMPLE, header_style=config.get('colors_s_list_header'),
            border_style=config.get('colors_s_list_border'))

        col_name = None
        idx = 0
        for idx in range(len(listing[0])):
            column = listing[0][idx]
            if column == t_format.NAME:
                table.add_column(_(column), style=config.get('colors_s_list_name'))
                col_name = idx
            elif column == t_format.SIZE:
                table.add_column(_(column), style=config.get('colors_s_list_default'),
                justify='right')
            else:
                table.add_column(_(column), style=config.get('colors_s_list_default'))

        for row in listing[1:]:
            if col_name is not None:
                # Quote filenames when needed
                row[col_name] = shlex.quote(row[col_name])
            table.add_row(*row)

        self.out_c.print(table)
