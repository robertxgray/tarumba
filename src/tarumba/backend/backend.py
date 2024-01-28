# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's base archive backend"

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

class Backend(ABC):
    "Abstract parent class for archive backends"

    # List of programs used to add
    COMPRESSORS = []
    # List of programs used to list and extract
    EXTRACTORS = []

    # The backend can store duplicates
    CAN_DUPLICATE = False
    # The backend can encrypt it's contents
    CAN_ENCRYPT = False
    # The backend can store multiple files
    CAN_PACK = False
    # The backend can store special files
    CAN_SPECIAL = False

    # Particular patterns when listing files
    LIST_PATTERNS = None
    # Particular patterns when adding files
    ADD_PATTERNS = None
    # Particular patterns when extracting files
    EXTRACT_PATTERNS = None

    def __init__(self, mime):
        """
        Backend constructor.

        :param mime: Archive mime type
        """
        self.mime = mime

    @abstractmethod
    def list_commands(self, list_args):
        "Commands to list the archive contents"

    @abstractmethod
    def add_commands(self, add_args, files):
        "Commands to add files to an archive"

    @abstractmethod
    def extract_commands(self, extract_args):
        "Commands to extract files from an archive"

    @abstractmethod
    def parse_list(self, executor, line_number, line, extra):
        "Parse the output when listing files"
        return False

    @abstractmethod
    def parse_add(self, executor, line_number, line, extra):
        "Parse the output when adding files"
        return False

    @abstractmethod
    def parse_extract(self, executor, line_number, line, extra):
        "Parse the output when extracting files"
        return False
