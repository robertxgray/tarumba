# Copyright: (c) 2025, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's Rar backend support"

import os
from gettext import gettext as _

from typing_extensions import override

import tarumba.constants as t_constants
import tarumba.errors as t_errors
import tarumba.file_utils as t_file_utils
import tarumba.utils as t_utils
from tarumba import executor as t_executor
from tarumba.backend import backend as t_backend
from tarumba.config import current as config
from tarumba.gui import current as t_gui

LIST_ELEMENTS = 7


class Rar(t_backend.Backend):
    "Rar archiver backend"

    # Particular patterns when listing files
    LIST_PATTERNS = frozenset([" password: ", "password incorrect--reenter: "])
    # Particular patterns when adding files
    ADD_PATTERNS = frozenset(["Enter password: ", "Verify password: "])
    # Particular patterns when extracting files
    EXTRACT_PATTERNS = frozenset([" password: ", "password incorrect--reenter: "])
    # Particular patterns when testing files
    TEST_PATTERNS = frozenset([" password: ", "password incorrect--reenter: "])

    @override
    def __init__(self, mime, operation):
        """
        Backend constructor.

        :param mime: Archive mime type
        :param operation: Backend operation
        """

        super().__init__(mime, operation)
        self._rar_bin = None
        self._can_compress = False
        self._current_file = {}

        # Rar is required to modify archives
        try:
            self._rar_bin = t_utils.check_installed(config.get("backends_l_rar_bin"))
            self._can_compress = True
        except t_errors.BackendUnavailableError:
            if operation in (t_constants.OPERATION_ADD, t_constants.OPERATION_DELETE, t_constants.OPERATION_RENAME):
                raise

        # Unrar can be used to list and extract if rar is unavailable
        if not self._rar_bin:
            try:
                self._rar_bin = t_utils.check_installed(config.get("backends_l_unrar_bin"))
                self._check_unrar_free()
            except t_errors.BackendUnavailableError:
                if not self._rar_bin:
                    raise

    def _check_unrar_free(self):
        """
        Checks if we are using the free version of unrar. This version is unsupported because modern rar tools cannot
        be used to create a compatible (RAR 2.0) archive. Please contact us if you need this feature and know how it
        could be tested.
        """

        unrar_output = t_executor.Executor().execute_simple(self._rar_bin)
        if unrar_output[0].endswith("Archive not specified"):
            raise t_errors.BackendUnavailableError(
                _(
                    "we are sorry but the free version of unrar is not supported, because it is not compatible with "
                    "modern archives. We recommend using the unar backend instead."
                )
            )

    @override
    def list_commands(self, list_args):
        """
        Commands to list files in the archive.

        :param list_args: ListArgs object
        :return: List of commands
        """

        return [(self._rar_bin, ["vt", "-c-", "--", list_args.get("archive"), *self._unslash(list_args.get("files"))])]

    @override
    def add_commands(self, add_args, files):
        """
        Commands to add files to the archive.

        :param add_args: AddArgs object
        :param files: List of files
        :return: List of commands
        """

        params = ["a", "-idcdp", "-y"]
        if add_args.get("password"):
            params.append("-hp")
        if not add_args.get("follow_links"):
            params.append("-ol")
        if add_args.get("level"):
            params.append(f"-m{add_args.get('level')}")
        return [(self._rar_bin, [*params, add_args.get("archive"), "--", *self._slash(files)])]

    @override
    def extract_commands(self, extract_args):
        """
        Commands to extract files from the archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        return [
            (
                self._rar_bin,
                ["x", "-idcdp", "-y", "-o+", extract_args.get("archive"), *self._unslash(extract_args.get("files"))],
            )
        ]

    @override
    def delete_commands(self, delete_args):
        """
        Commands to delete files from the archive.

        :param delete_args: DeleteArgs object
        :return: List of commands
        """

        return [
            (self._rar_bin, ["d", "-idcdp", delete_args.get("archive"), "--", *self._unslash(delete_args.get("files"))])
        ]

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
                self._rar_bin,
                ["t", "-idcdp", "--", test_args.get("archive"), *self._unslash(test_args.get("files"))],
            )
        ]

    def _parse_list_line(self, line):
        """
        Parses one line of the listing.

        :param line: Line
        """

        if line.startswith("        Name: "):
            self._current_file[t_constants.COLUMN_NAME] = line[14:]
        elif line.startswith("        Size: "):
            self._current_file[t_constants.COLUMN_SIZE] = line[14:]
        elif line.startswith(" Packed size: "):
            self._current_file[t_constants.COLUMN_PACKED] = line[14:]
        elif line.startswith("       mtime: "):
            self._current_file[t_constants.COLUMN_DATE] = line[14:30]
        elif line.startswith("  Attributes: "):
            self._current_file[t_constants.COLUMN_PERMS] = line[14:]
        elif line.startswith("   CRC32 MAC: "):
            self._current_file[t_constants.COLUMN_CRC] = line[14:]
        elif line.startswith("       Flags: "):
            if "encrypted" in line[14]:
                self._current_file[t_constants.COLUMN_ENC] = _("yes")
        # Rar's output doesn't include a trailing slash in directories
        elif line.startswith("        Type: ") and line[14:] == "Directory":
            self._current_file[t_constants.COLUMN_NAME] += "/"
            self._current_file[t_constants.COLUMN_SIZE] = "0"
            self._current_file[t_constants.COLUMN_PACKED] = "0"

    @override
    def parse_list(self, executor, line_number, line, extra):
        """
        Parse the output when listing files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        # Password prompt
        # for pattern in self.LIST_PATTERNS:
        #    regex = re.compile(pattern)
        #    if regex.fullmatch(line):
        #        extra.put("password", t_utils.get_password(archive=extra.get("archive")))
        #        executor.send_line(extra.get("password"))
        #        return

        output = extra.get("output")

        # List output
        if isinstance(output, list):
            if line == "" and self._current_file:  # End of file
                row = [self._current_file.get(column) for column in extra.get("columns")]
                output.append(row)
                self._current_file = {}

            else:
                self._parse_list_line(line)

        # Set output
        elif isinstance(output, set):
            if line == "" and self._current_file:  # End of file
                output.add(self._current_file[t_constants.COLUMN_NAME])
                self._current_file = {}
            elif line.startswith("        Name: "):
                self._current_file[t_constants.COLUMN_NAME] = line[14:]
            elif line.startswith("        Type: ") and line[14:] == "Directory":
                self._current_file[t_constants.COLUMN_NAME] += "/"

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
            if line.endswith(pattern):
                executor.send_line(extra.get("password"))
                return

        if line.startswith(("Adding    ", "Updating  ")):
            t_gui.adding_msg(line[10:-3].rstrip())
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
            if line.endswith(pattern):
                if not extra.get("password"):
                    extra.put("password", t_utils.get_password(archive=extra.get("archive")))
                executor.send_line(extra.get("password"))
                return

        if line.startswith(("Creating    ", "Extracting  ")):
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
            if line.endswith(pattern):
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
            if line.endswith(pattern):
                extra.put("password", t_utils.get_password(archive=extra.get("archive")))
                executor.send_line(extra.get("password"))
                return

        if line.startswith("Testing     "):
            # In my tests OK is sometimes followed by a space, but not always
            t_gui.testing_msg(line[12:].rstrip()[:-2].rstrip())
            t_gui.advance_progress()

    def _slash(self, files):
        """
        Adds a trailing slash to directories in the list of files.

        :param files: List of files
        """
        output = []
        for file in files:
            if not file.endswith("/") and os.path.isdir(file):
                output.append(file + "/")
            else:
                output.append(file)
        return output

    def _unslash(self, files):
        """
        Removes the trailing slash from a list of files.

        :param files: List of files
        """

        return [file.rstrip("/") for file in files]
