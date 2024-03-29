# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's tar backend support"

from gettext import gettext as _

from typing_extensions import override  # pylint: disable=import-error

import tarumba.constants as t_constants
import tarumba.file_utils as t_file_utils
from tarumba import utils as t_utils
from tarumba.backend import backend as t_backend
from tarumba.config import current as config
from tarumba.gui import current as t_gui

LIST_ELEMENTS = 5

class Tar(t_backend.Backend):
    "Tar archiver backend"

    @override
    def __init__(self, mime, operation):
        """
        Backend constructor.

        :param mime: Archive mime type
        :param operation: Backend operation
        """

        super().__init__(mime, operation)
        self._tar_bin = t_utils.check_installed(config.get('backends_l_tar_bin'))

    @override
    def list_commands(self, list_args):
        """
        Commands to list the archive contents.

        :param list_args: ListArgs object
        :return: List of commands
        """

        params = []
        params.append('--numeric-owner')
        if list_args.get('occurrence'):
            params.append('--occurrence='+list_args.get('occurrence'))
        return [(self._tar_bin,
            [*params, '-tvf', list_args.get('archive'), '--', *list_args.get('files')])]

    @override
    def add_commands(self, add_args, files):
        """
        Commands to add files to an archive.

        :param add_args: AddArgs object
        :param files: List of files
        :return: List of commands
        """

        params = []
        if add_args.get('follow_links'):
            params.append('-h')
        if not add_args.get('owner'):
            params.append('--owner=0')
            params.append('--group=0')
        return [(self._tar_bin,
            [*params, '-rvSf', add_args.get('archive'), '--', files])]

    @override
    def extract_commands(self, extract_args):
        """
        Commands to extract files from an archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        params = []
        if extract_args.get('occurrence'):
            params.append('--occurrence='+extract_args.get('occurrence'))
        return [(self._tar_bin,
            [*params, '-xvf', extract_args.get('archive'), '--', *extract_args.get('files')])]

    @override
    def test_commands(self, test_args):
        """
        Commands to test the archive contents.

        :param test_args: TestArgs object
        :return: List of commands
        """

        return [(self._tar_bin,
            ['-tf', test_args.get('archive'), '--', *test_args.get('files')])]

    @override
    def parse_list(self, executor, line_number, line, extra):
        """
        Parse the output when listing files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        elements = line.split(None, 4)
        if len(elements) < LIST_ELEMENTS:
            return
        output = extra.get('output')

        # List output
        if isinstance(output, list):
            columns = t_utils.get_list_columns(
                extra.get('columns'), config.get('main_l_list_columns'), output)
            row = []
            for column in columns:
                if column == t_constants.COLUMN_PERMS:
                    row.append(elements[0])
                elif column == t_constants.COLUMN_OWNER:
                    row.append(elements[1])
                elif column == t_constants.COLUMN_SIZE:
                    row.append(elements[2])
                elif column == t_constants.COLUMN_DATE:
                    row.append(f'{elements[3]} {elements[4][:5]}')
                elif column == t_constants.COLUMN_NAME:
                    name = elements[4][6:]
                    link_pos = name.find(' -> ')
                    if link_pos >= 0:
                        row.append(name[:link_pos])
                    else:
                        row.append(name)
            output.append(row)
        # Set output
        elif isinstance(output, set):
            output.add(elements[4][6:])

    @override
    def parse_add(self, executor, line_number, line, extra):
        """
        Parse the output when adding files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line.startswith(f'{self._tar_bin}: '):
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': line})
        elif len(line) > 0:
            t_gui.adding_msg(line)
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

        if line.startswith(f'{self._tar_bin}: '):
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': line})
        elif len(line) > 0:
            t_file_utils.pop_and_move_extracted(extra)

    @override
    def parse_test(self, executor, line_number, line, extra):
        """
        Parse the output when testing files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line.startswith(f'{self._tar_bin}: '):
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': line})
        elif len(line) > 0:
            t_gui.testing_msg(line)
            t_gui.advance_progress()
