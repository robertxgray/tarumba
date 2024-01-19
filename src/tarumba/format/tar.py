# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's tar archive support"

from gettext import gettext as _

from tarumba.config import current as config
import tarumba.file_utils as t_file_utils
from tarumba.format import format as t_format
from tarumba.gui import current as t_gui
from tarumba import utils as t_utils

class Tar(t_format.Format):
    "Tar archive support functions"

    NAME = 'tar'

    # List of programs used to add
    COMPRESSORS = [config.get('tar_s_tar_bin')]
    # List of programs used to list and extract
    EXTRACTORS = [config.get('tar_s_tar_bin')]

    # The format can store duplicates
    CAN_DUPLICATE = True
    # The format can encrypt it's contents
    CAN_ENCRYPT = False
    # The format can store multiple files
    CAN_PACK = True
    # The format can store special files
    CAN_SPECIAL = True

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
        return [(config.get('tar_s_tar_bin'),
            params + ['-tvf', list_args.get('archive'), '--'] + list_args.get('files'))]

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
        return [(config.get('tar_s_tar_bin'),
            params + ['-rvf', add_args.get('archive'), '--', files])]

    def extract_commands(self, extract_args):
        """
        Commands to extract files from an archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        params = []
        if extract_args.get('occurrence'):
            params.append('--occurrence='+extract_args.get('occurrence'))
        return [(config.get('tar_s_tar_bin'),
            params + ['-xvf', extract_args.get('archive'), '--'] + extract_args.get('files'))]

    def parse_list(self, executor, line_number, line, extra):
        """
        Parse the output when listing files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if not line:
            return
        elements = line.split(None, 4)
        if len(elements) < 5:
            return
        output = extra.get('output')

        # List output
        if isinstance(output, list):
            columns = t_utils.get_list_columns(
                extra.get('columns'), config.get('tar_l_columns'), output)
            row = []
            for column in columns:
                if column == t_format.PERMS:
                    row.append(elements[0])
                elif column == t_format.OWNER:
                    row.append(elements[1])
                elif column == t_format.SIZE:
                    row.append(elements[2])
                elif column == t_format.DATE:
                    row.append(f'{elements[3]} {elements[4][:5]}')
                elif column == t_format.NAME:
                    row.append(elements[4][6:])
            output.append(row)
        # Set output
        if isinstance(output, set):
            output.add(elements[4][6:])

    def parse_add(self, executor, line_number, line, extra):
        """
        Parse the output when adding files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line.startswith('tar: '):
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': line})
        elif len(line) > 0:
            t_gui.adding_msg(line)
            t_gui.advance_progress()

    def parse_extract(self, executor, line_number, line, extra):
        """
        Parse the output when extracting files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line.startswith('tar: '):
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': line})
        elif len(line) > 0:
            file = extra.get('contents').pop(0)[0]
            moved = t_file_utils.move_extracted(file, extra)
            if moved:
                t_gui.extracting_msg(file)
            t_gui.advance_progress()
