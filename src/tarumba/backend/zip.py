# Copyright: (c) 2024, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's Info-Zip backend support"

import re
from gettext import gettext as _

from typing_extensions import override

import tarumba.constants as t_constants
import tarumba.file_utils as t_file_utils
import tarumba.utils as t_utils
from tarumba import executor as t_executor
from tarumba.backend import backend as t_backend
from tarumba.config import current as config
from tarumba.gui import current as t_gui

LIST_ELEMENTS = 8


class Zip(t_backend.Backend):
    "Zip archiver backend"

    # Particular patterns when listing files
    LIST_PATTERNS = frozenset([".* password: ", "password incorrect--reenter: "])
    # Particular patterns when adding files
    ADD_PATTERNS = frozenset(["Enter password: ", "Verify password: "])
    # Particular patterns when extracting files
    EXTRACT_PATTERNS = frozenset([".* password: ", "password incorrect--reenter: "])
    # Particular patterns when testing files
    TEST_PATTERNS = frozenset([".* password: ", "password incorrect--reenter: "])

    @override
    def __init__(self, mime, operation):
        """
        Backend constructor.

        :param mime: Archive mime type
        :param operation: Backend operation
        """

        super().__init__(mime, operation)
        self._zip_bin = t_utils.check_installed(config.get("backends_l_zip_bin"))
        self._unzip_bin = t_utils.check_installed(config.get("backends_l_unzip_bin"))

    @override
    def list_commands(self, list_args):
        """
        Commands to list files in the archive.

        :param list_args: ListArgs object
        :return: List of commands
        """

        return [(self._unzip_bin, ["-Z", "-lT", "--h-t", "--", list_args.get("archive"), *list_args.get("files")])]

    @override
    def add_commands(self, add_args, files):
        """
        Commands to add files to the archive.

        :param add_args: AddArgs object
        :param files: List of files
        :return: List of commands
        """

        params = ["-r"]
        if add_args.get("password"):
            params.append("-e")
        if add_args.get("follow_links"):
            params.append("-y")
        if add_args.get("level"):
            params.append(f"-{add_args.get('level')}")
        return [(self._zip_bin, [*params, "--", add_args.get("archive"), *files])]

    @override
    def extract_commands(self, extract_args):
        """
        Commands to extract files from the archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        return [(self._unzip_bin,
            ["-o", "--", extract_args.get("archive"), *extract_args.get("files")])]

    @override
    def delete_commands(self, delete_args):
        """
        Commands to delete files from the archive.

        :param extract_args: DeleteArgs object
        :return: List of commands
        """

        return [(self._zip_bin,
            ["-d", "--", extract_args.get("archive"), *extract_args.get("files")])]

    @override
    def rename_commands(self, rename_args):
        """
        Commands to rename files in the archive.

        :param rename_args: RenameArgs object
        :return: List of commands
        """

        raise NotImplementedError(
            _("the %(back1)s backend cannot rename files, but you can use %(back2)s instead")
            % {"back1": "zip", "back2": "7z"}
        )

    @override
    def test_commands(self, test_args):
        """
        Commands to test files in the archive.

        :param test_args: TestArgs object
        :return: List of commands
        """

        return [
            (
                self._unzip_bin,
                ["-t", "--", test_args.get("archive"), *test_args.get("files")],
            )
        ]

    def _parse_list_row(self, elements, extra):
        """
        Builds an output row using the listing elements.

        :param elements: Listing elements
        :param extra: Extra data
        :return: Output row
        """

        row = []
        for column in extra.get("columns"):
            if column == t_constants.COLUMN_PERMS:
                row.append(elements[0])
            elif column == t_constants.COLUMN_SIZE:
                row.append(elements[3])
            elif column == t_constants.COLUMN_ENC:
                if elements[4][0] in ("T", "B"): # See zipinfo(1)
                    row.append(_("yes"))
                else:
                    row.append(None)
            elif column == t_constants.COLUMN_PACKED:
                row.append(elements[5])
            elif column == t_constants.COLUMN_METHOD:
                row.append(elements[6])
            elif column == t_constants.COLUMN_DATE:
                yea = elements[7][0:4]
                mon = elements[7][4:6]
                day = elements[7][6:8]
                hou = elements[7][9:11]
                mit = elements[7][11:13]
                row.append(f'{yea}-{mon}-{day} {hou}:{mit}')
            elif column == t_constants.COLUMN_NAME:
                row.append(elements[7][16:])
            else:
                row.append(None)
        return row

    @override
    def parse_list(self, executor, line_number, line, extra):
        """
        Parse the output when listing files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if not line or line.startswith('caution: '): # Ignore warnings
            return
        elements = line.split(None, 7)
        if len(elements) < LIST_ELEMENTS:
            return
        output = extra.get("output")

        # List output
        if isinstance(output, list):
            output.append(self._parse_list_row(elements, extra))
        # Set output
        elif isinstance(output, set):
            output.add(elements[7][16:])

    @override
    def parse_add(self, executor, line_number, line, extra):
        """
        Parse the output when adding files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        # Password prompt
        for pattern in self.ADD_PATTERNS:
            regex = re.compile(pattern)
            if regex.fullmatch(line):
                executor.send_line(extra.get("password"))
                return

        if line.startswith(("+ ", "U ")):
            t_gui.adding_msg(line[2:])
            t_gui.advance_progress()

    @override
    def parse_extract(self, executor, line_number, line, extra):
        """
        Parse the output when extracting files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        # Password prompt
        for pattern in self.EXTRACT_PATTERNS:
            regex = re.compile(pattern)
            if regex.fullmatch(line):
                if not extra.get("password"):
                    extra.put("password", t_utils.get_password(archive=extra.get("archive")))
                executor.send_line(extra.get("password"))
                return

        if line.startswith("- "):
            t_file_utils.pop_and_move_extracted(extra)

    @override
    def parse_delete(self, executor, line_number, line, extra):
        """
        Parse the output when deleting files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        # Password prompt
        for pattern in self.TEST_PATTERNS:
            regex = re.compile(pattern)
            if regex.fullmatch(line):
                extra.put("password", t_utils.get_password(archive=extra.get("archive")))
                executor.send_line(extra.get("password"))
                return

    @override
    def parse_rename(self, executor, line_number, line, extra):
        """
        Parse the output when renaming files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        raise NotImplementedError(
            _("the %(back1)s backend cannot rename files, but you can use %(back2)s instead")
            % {"back1": "zip", "back2": "7z"}
        )

    @override
    def parse_test(self, executor, line_number, line, extra):
        """
        Parse the output when testing files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        # Password prompt
        for pattern in self.TEST_PATTERNS:
            regex = re.compile(pattern)
            if regex.fullmatch(line):
                extra.put("password", t_utils.get_password(archive=extra.get("archive")))
                executor.send_line(extra.get("password"))
                return

        if line.startswith("    testing: "):
            t_gui.testing_msg(line[13:-5])
            t_gui.advance_progress()
