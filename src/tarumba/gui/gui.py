# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's base GUI"

from abc import ABC, abstractmethod


class Gui(ABC):
    "Abstract parent class for GUIs"

    # Answers
    YES = 'YES'
    NO = 'NO'
    ALL = 'ALL'
    NONE = 'NONE'

    @abstractmethod
    def debug(self, key, value):
        "Prints debugging information"

    @abstractmethod
    def info(self, message):
        "Prints a info message"

    @abstractmethod
    def warn(self, message):
        "Prints a warning message"

    @abstractmethod
    def error(self, message):
        "Prints an error message"

    @abstractmethod
    def prompt_password(self, message):
        "Prompts for a password"

    @abstractmethod
    def start_progress(self, message, file):
        "Starts a progress bar"

    @abstractmethod
    def stop_progress(self):
        "Stops a progress bar"

    @abstractmethod
    def update_progress_total(self, total):
        "Update the progress bar total"

    @abstractmethod
    def advance_progress(self):
        "Advance the progress bar"
