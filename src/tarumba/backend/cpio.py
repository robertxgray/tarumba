# Copyright: (c) 2025, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's Cpio backend support"

import os
import re
import shlex
from datetime import datetime
from gettext import gettext as _

import tzlocal
from typing_extensions import override

import tarumba.constants as t_constants
import tarumba.file_utils as t_file_utils
import tarumba.utils as t_utils
from tarumba.backend import backend as t_backend
from tarumba.config import current as config
from tarumba.gui import current as t_gui

LIST_ELEMENTS = 8
LIST_DATE_FORMAT = "%b %d %Y %H:%M"


class Cpio(t_backend.Backend):
    "Cpio archiver backend"

    @override
    def __init__(self, mime, operation):
        """
        Backend constructor.

        :param mime: Archive mime type
        :param operation: Backend operation
        """

        super().__init__(mime, operation)
        self._cpio_bin = t_utils.check_installed(config.get("backends_l_cpio_bin"))
        self._error_prefix = f"{self._cpio_bin}: "
        if operation in [t_constants.OPERATION_ADD]:
            self._shell = t_utils.check_installed(config.get("main_l_shell"))
            self._find = t_utils.check_installed(config.get("main_l_find"))

    @override
    def list_commands(self, list_args):
        """
        Commands to list files in the archive.

        :param list_args: ListArgs object
        :return: List of commands
        """

        return [(self._cpio_bin, ["--force-local", "-tvF", list_args.get("archive")])]

    @override
    def add_commands(self, add_args, files):
        """
        Commands to add files to the archive.

        :param add_args: AddArgs object
        :param files: List of files
        :return: List of commands
        """

        archive_quot = shlex.quote(add_args.get("archive"))
        level = f" -{add_args.get('level')}" if add_args.get("level") else ""
        command = f"{shlex.quote(self._cpio_bin)} -cfN{level} {shlex.quote(files[0])} > {archive_quot}"
        return [(self._shell, ["-c", command])]

    @override
    def extract_commands(self, extract_args):
        """
        Commands to extract files from the archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        contents = extract_args.get("contents")
        if contents:
            archive_quot = shlex.quote(extract_args.get("archive"))
            content_quot = shlex.quote(contents[0])
            command = f"{shlex.quote(self._cpio_bin)} -dcfN {archive_quot} > {content_quot}"
            return [(self._shell, ["-c", command]), (self._shell, ["-c", "echo ''"])]
        return []

    @override
    def delete_commands(self, delete_args):
        """
        Commands to delete files from the archive.

        :param delete_args: DeleteArgs object
        :return: List of commands
        """

        return []

    @override
    def rename_commands(self, rename_args):
        """
        Commands to rename files in the archive.

        :param rename_args: RenameArgs object
        :return: List of commands
        """

        raise NotImplementedError(
            _("the %(back1)s backend cannot rename files, but you can use %(back2)s instead")
            % {"back1": "gzip", "back2": "7z"}
        )

    @override
    def test_commands(self, test_args):
        """
        Commands to test files in the archive.

        :param test_args: TestArgs object
        :return: List of commands
        """

        return [(self._cpio_bin, ["--force-local", "-tF", test_args.get("archive")])]

    def _parse_date(self, month, day, combo):
        """
        Parses the dates in cpio output. The backend provides the month, day and either the year of the time.

        :param month: Month
        :param day: Day
        :param combo: Year or time
        """

        if combo[2] == ":":
            today = datetime.now(tz=tzlocal.get_localzone())
            file_dt_str = f"{month} {day} {today.year} {combo}"
            file_dt = datetime.strptime(file_dt_str, LIST_DATE_FORMAT).astimezone(tzlocal.get_localzone())
            combo_year = today.year
            if file_dt > today:
                combo_year -= 1
            combo_time = combo
        else:
            combo_year = combo
            combo_time = "00:00"

        datetime_str = f"{month} {day} {combo_year} {combo_time}"
        return (
            datetime.strptime(datetime_str, LIST_DATE_FORMAT)
            .astimezone(tzlocal.get_localzone())
            .strftime(t_constants.DATE_FORMAT)
        )

    def _parse_list_row(self, elements, extra):
        """
        Builds an output row using the listing elements.

        :params file_name: File name
        :param elements: Listing elements
        :param extra: Extra data
        :return: Output row
        """

        row = []
        for column in extra.get("columns"):
            if column == t_constants.COLUMN_PERMS:
                row.append(elements[0])
            elif column == t_constants.COLUMN_OWNER:
                row.append(f"{elements[2]}/{elements[3]}")
            elif column == t_constants.COLUMN_SIZE:
                row.append(elements[4])
            elif column == t_constants.COLUMN_DATE:
                row.append(self._parse_date(elements[5], elements[6], elements[7][:5]))
            elif column == t_constants.COLUMN_NAME:
                row.append(elements[7][6:])
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

        if line.startswith(self._error_prefix):
            t_gui.warn(
                _("%(prog)s: warning: %(message)s\n") % {"prog": "tarumba", "message": line[len(self._error_prefix) :]}
            )

        elements = line.split(None, 7)
        if len(elements) < LIST_ELEMENTS:
            return
        output = extra.get("output")

        file_name = os.path.basename(elements[7][elements[7].find(" ") + 1 :])
        if extra.get("files") and file_name not in extra.get("files"):
            return

        # List output
        if isinstance(output, list):
            output.append(self._parse_list_row(elements, extra))
        # Set output
        elif isinstance(output, set):
            output.add(file_name)

    @override
    def parse_add(self, executor, line_number, line, extra):
        """
        Parse the output when adding files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line.startswith(self._error_prefix):
            t_gui.warn(
                _("%(prog)s: warning: %(message)s\n") % {"prog": "tarumba", "message": line[len(self._error_prefix) :]}
            )

    @override
    def parse_extract(self, executor, line_number, line, extra):
        """
        Parse the output when extracting files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line.startswith(self._error_prefix):
            t_gui.warn(
                _("%(prog)s: warning: %(message)s\n") % {"prog": "tarumba", "message": line[len(self._error_prefix) :]}
            )
        else:
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
            % {"back1": "gzip", "back2": "7z"}
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

        if line.startswith(self._error_prefix):
            t_gui.warn(
                _("%(prog)s: warning: %(message)s\n") % {"prog": "tarumba", "message": line[len(self._error_prefix) :]}
            )
        else:
            regex = re.compile(r"(.*):\s+OK$")
            regex_match = regex.fullmatch(line)
            if regex_match:
                t_gui.testing_msg(os.path.basename(regex_match.group(1)))
                t_gui.advance_progress()
