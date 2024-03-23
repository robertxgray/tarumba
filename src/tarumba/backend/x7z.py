# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's 7z backend support"

import re
from pathlib import Path

from typing_extensions import override  # pylint: disable=import-error

import tarumba.constants as t_constants
import tarumba.file_utils as t_file_utils
import tarumba.utils as t_utils
from tarumba import executor as t_executor
from tarumba.backend import backend as t_backend
from tarumba.config import current as config
from tarumba.gui import current as t_gui


class X7z(t_backend.Backend):
    "7z archiver backend"

    # Particular patterns when listing files
    LIST_PATTERNS = frozenset(['Enter password.*:'])
    # Particular patterns when adding files
    ADD_PATTERNS = frozenset(['Enter password.*:', 'Verify password.*:'])
    # Particular patterns when extracting files
    EXTRACT_PATTERNS = frozenset(['Enter password.*:'])

    # 7z uses this string to mark the start of the list of files
    LIST_START = '----------'

    @override
    def __init__(self, mime, operation):
        """
        Backend constructor.

        :param mime: Archive mime type
        :param operation: Backend operation
        """

        super().__init__(mime, operation)
        self._7zip_bin = t_utils.check_installed(config.get('backends_l_7zip_bin'))
        _7z_info = t_executor.Executor().execute_simple(self._7zip_bin)
        self._p7zip = self._check_p7zip(_7z_info)
        self._list_started = False
        self._current_file = {}

    def _check_p7zip(self, _7z_info):
        """
        Returns true if we are using a p7zip variant of the backend.

        :param _7z_info: Program output wihtout parameters
        :return: True if p7zip is detected
        """

        return _7z_info[2].startswith('p7zip')

    @override
    def can_duplicate(self):
        """
        Returns true if the archive can store duplicates.

        :return: True of False
        """

        return False # 7z can't manage duplicates, even in tarfiles

    @override
    def list_commands(self, list_args):
        """
        Commands to list the archive contents.

        :param list_args: ListArgs object
        :return: List of commands
        """

        return [(self._7zip_bin, ['l', '-slt', '--',
            list_args.get('archive'), *list_args.get('files')])]

    @override
    def add_commands(self, add_args, files):
        """
        Commands to add files to an archive.

        :param add_args: AddArgs object
        :param contents: Files root path
        :return: List of commands
        """

        params = ['a', '-bb1', '-ba', '-bd']
        if add_args.get('password'):
            params.append('-p')
            if self.mime[0] == t_constants.MIME_7Z:
                params.append('-mhe')
        if add_args.get('follow_links'):
            params.append('-snh')
            if self._p7zip:
                params.append('-l')
        else:
            params.append('-snl')
        if add_args.get('level'):
            params.append(f"-mx={add_args.get('level')}")
        return [(self._7zip_bin, [*params, '--', add_args.get('archive'), files])]

    @override
    def extract_commands(self, extract_args):
        """
        Commands to extract files from an archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        return [(self._7zip_bin, ['x', '-y', '-bb1', '-ba', '-bd', '--',
            extract_args.get('archive'), *extract_args.get('files')])]

    def _parse_list_line(self, line):
        """
        Parses one line of the listing.

        :param line: Line
        """

        if line.startswith('Path = '):
            self._current_file[t_constants.COLUMN_NAME] = line[7:]
        elif line.startswith('Size = '):
            self._current_file[t_constants.COLUMN_SIZE] = line[7:]
        elif line.startswith('Packed Size = '):
            self._current_file[t_constants.COLUMN_PACKED] = line[14:]
        elif line.startswith('Modified = '):
            self._current_file[t_constants.COLUMN_DATE] = line[11:27]
        elif line.startswith('Attributes = '):
            self._current_file[t_constants.COLUMN_PERMS] = line[-10:]
        elif line.startswith('Encrypted = '):
            self._current_file[t_constants.COLUMN_ENC] = line[12:]
        elif line.startswith('CRC = '):
            self._current_file[t_constants.COLUMN_CRC] = line[6:]
        elif line.startswith('Method = '):
            self._current_file[t_constants.COLUMN_METHOD] = line[9:]

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
        for pattern in self.LIST_PATTERNS:
            regex = re.compile(pattern)
            if regex.fullmatch(line):
                extra.put('password', t_utils.get_password(archive=extra.get('archive')))
                executor.send_line(extra.get('password'))
                return

        if not self._list_started:
            if line == self.LIST_START:
                self._list_started = True
        else:
            output = extra.get('output')

            # List output
            if isinstance(output, list):
                if line == '': # End of file
                    columns = t_utils.get_list_columns(
                        extra.get('columns'), config.get('main_l_list_columns'), output)

                    # Some formats can't store the file name
                    if t_constants.COLUMN_NAME not in self._current_file:
                        self._current_file[t_constants.COLUMN_NAME] = Path(
                            extra.get('archive')).stem

                    row = [self._current_file.get(column) for column in columns]
                    output.append(row)
                    self._current_file = {}

                else:
                    self._parse_list_line(line)

            # Set output
            elif isinstance(output, set) and line.startswith('Path = '):
                output.add(line[7:])

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
                executor.send_line(extra.get('password'))
                return

        if line.startswith(('+ ', 'U ')):
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
                if not extra.get('password'):
                    extra.put('password', t_utils.get_password(archive=extra.get('archive')))
                executor.send_line(extra.get('password'))
                return

        if line.startswith('- '):
            t_file_utils.pop_and_move_extracted(extra)
