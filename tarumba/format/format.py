# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's base archive format"

from abc import ABC, abstractmethod

# Columns in archive contents
DATE = 'DATE'
NAME = 'NAME'
OWNER = 'OWNER'
PACKED = 'PACKED'
PERMS = 'PERMISSIONS'
SIZE = 'SIZE'

# Set to check if a column exists
COLUMNS_SET = {
    DATE,
    NAME,
    OWNER,
    PACKED,
    PERMS,
    SIZE
}

class Format(ABC):
    "Abstract parent class for archive formats"

    NAME = None

    # The format can store duplicates
    CAN_DUPLICATE = False
    # The format can store multiple files
    CAN_PACK = False
    # The format can store special files
    CAN_SPECIAL = False

    @abstractmethod
    def list_commands(self, archive):
        "Commands to list the archive contents"

    @abstractmethod
    def parse_listing(self, contents, columns):
        "Parse the archive contents listing"

    @abstractmethod
    def parse_listing_2set(self, contents):
        "Parse the archive contents into a set"

    @abstractmethod
    def add_commands(self, archive, files):
        "Commands to add files to an archive"

    @abstractmethod
    def parse_add(self, line_number, line):
        "Parse the output when adding files"
