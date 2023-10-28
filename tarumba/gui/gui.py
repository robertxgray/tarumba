# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from abc import ABC, abstractmethod

class Gui(ABC):

    @abstractmethod
    def info(self, message):
        "Prints a info message to the console."
        pass

    @abstractmethod
    def warn(self, message):
        "Prints a warning message to the console."
        pass

    @abstractmethod
    def error(self, message):
        "Prints an error message to the console."
        pass

    @abstractmethod
    def print_listing(self, listing):
        "Prints an archive contents listing to the console."
        pass
