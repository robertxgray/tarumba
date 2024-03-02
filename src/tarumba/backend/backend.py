# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's base archive backend"

from abc import ABC, abstractmethod

import tarumba.constants as t_constants

class Backend(ABC):
    "Abstract parent class for archiver backends"

    # Particular patterns when listing files
    LIST_PATTERNS = None
    # Particular patterns when adding files
    ADD_PATTERNS = None
    # Particular patterns when extracting files
    EXTRACT_PATTERNS = None

    def __init__(self, mime, operation):
        """
        Backend constructor.

        :param mime: Archive mime type
        """
        self.mime = mime
        self.operation = operation

    def can_duplicate(self):
        """
        Returns true if the archive can store duplicates.

        :return: True of False
        """

        if self.mime[0] == t_constants.MIME_TAR:
            return True
        return False

    def can_encrypt(self):
        """
        Returns true if the archive contents can be encrypted.

        :return: True of False
        """

        if self.mime[0] in (t_constants.MIME_7Z, t_constants.MIME_ZIP):
            return True
        return False

    def can_pack(self):
        """
        Returns true if the archive can store multiple files.

        :return: True of False
        """

        if self.mime[0] in (t_constants.MIME_BROTLI, t_constants.MIME_BZIP2,
                            t_constants.MIME_COMPRESS, t_constants.MIME_GZIP,
                            t_constants.MIME_LZMA, t_constants.MIME_XZ):
            return False
        return True

    def can_special(self):
        """
        Returns true if the archive can store special files.

        :return: True of False
        """

        if self.mime[0] == t_constants.MIME_TAR:
            return True
        return False

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
