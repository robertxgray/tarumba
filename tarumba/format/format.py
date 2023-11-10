# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from abc import ABC, abstractmethod

# Columns in archive contents
NAME = 'NAME'
SIZE = 'SIZE'
DATE = 'DATE'
PERMS = 'PERMISSIONS'
OWNER = 'OWNER'

# Set to check if a column exists
COLUMNS_SET = {
    NAME,
    SIZE,
    DATE,
    PERMS,
    OWNER
}

class Format(ABC):
    "Abstract parent class for archive formats."

    @abstractmethod
    def list_commands(self, archive):
        "Commands to list the archive contents."
        pass

    @abstractmethod
    def parse_listing(self, contents, columns):
        "Parse the archive contents listing."
        pass

    @abstractmethod
    def add_commands(self, archive, files):
        "Commands to add files to an archive."
        pass

    @abstractmethod
    def parse_add(self, line_number, line):
        "Parse the output when adding files."
        pass
