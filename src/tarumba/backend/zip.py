# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's zip backend support"

from gettext import gettext as _

from tarumba.config import current as config
import tarumba.file_utils as t_file_utils
from tarumba.backend import backend as t_backend
from tarumba.gui import current as t_gui
import tarumba.utils as t_utils

class Zip(t_backend.Backend):
    "Zip archive backend"

    NAME = 'zip'

    # List of programs used to add
    COMPRESSORS = [config.get('zip_s_zip_bin')]
    # List of programs used to list and extract
    EXTRACTORS = [config.get('zip_s_unzip_bin')]

    # The backend can store duplicates
    CAN_DUPLICATE = False
    # The backend can encrypt it's contents
    CAN_ENCRYPT = True
    # The backend can store multiple files
    CAN_PACK = True
    # The backend can store special files
    CAN_SPECIAL = False

    # Particular patterns when adding files
    ADD_PATTERNS = ['Enter password: ', 'Verify password: ']
    # Particular patterns when extracting files
    EXTRACT_PATTERNS = [' password: ', 'password incorrect--reenter: ']

    def _expand_patterns(self, files):
        """
        Expand file name patterns trying to imitate the behaviour of tar.

        :param files: List of files
        :return: Expanded list of files
        """

        expanded_files = []
        for file in files:
            # Include directory contents
            if file.endswith('/'):
                expanded_files.append(file + '*')
            else:
                expanded_files.append(file)
        return expanded_files

    def list_commands(self, list_args):
        """
        Commands to list the archive contents.

        :param list_args: ListArgs object
        :return: List of commands
        """

        expanded_files = self._expand_patterns(list_args.get('files'))
        return [(config.get('zip_s_unzip_bin'), ['-Z', '-lT', '--h-t', '--',
            list_args.get('archive')] + expanded_files)]

    def add_commands(self, add_args, files):
        """
        Commands to add files to an archive.

        :param add_args: AddArgs object
        :param contents: Files root path
        :return: List of commands
        """

        params = '-r'
        if add_args.get('password'):
            params += 'e'
        if not add_args.get('follow_links'):
            params += 'y'
        if add_args.get('level'):
            params += add_args.get('level')
        return [(config.get('zip_s_zip_bin'), [params, add_args.get('archive'), '--', files])]

    def extract_commands(self, extract_args):
        """
        Commands to extract files from an archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        expanded_files = self._expand_patterns(extract_args.get('files'))
        return [(config.get('zip_s_unzip_bin'),
            ['-o', '--', extract_args.get('archive')] + expanded_files)]

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
        if len(elements) < 8:
            return
        output = extra.get('output')

        # List output
        if isinstance(output, list):
            columns = t_utils.get_list_columns(
                extra.get('columns'), config.get('zip_l_columns'), output)
            row = []
            for column in columns:
                # We are ignoring the zip version and other metadata
                # They may be added in the future by popular demand
                if column == t_backend.PERMS:
                    row.append(elements[0])
                elif column == t_backend.SIZE:
                    row.append(elements[3])
                elif column == t_backend.PACKED:
                    row.append(elements[5])
                elif column == t_backend.DATE:
                    yea = elements[7][0:4]
                    mon = elements[7][4:6]
                    day = elements[7][6:8]
                    hou = elements[7][9:11]
                    mit = elements[7][11:13]
                    row.append(f'{yea}-{mon}-{day} {hou}:{mit}')
                elif column == t_backend.NAME:
                    row.append(elements[7][16:])
            output.append(row)
        # Set output
        if isinstance(output, set):
            output.add(elements[7][16:])

    def parse_add(self, executor, line_number, line, extra):
        """
        Parse the output when adding files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line in self.ADD_PATTERNS:
            executor.send_line(extra.get('password'))
        elif line.startswith('  adding: ') or line.startswith('updating: '):
            end = line.find(' (deflated ')
            if end < 0:
                end = line.find(' (stored ')
            t_gui.adding_msg(line[10:end])
            t_gui.advance_progress()
        elif len(line) > 0:
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': line})

    def parse_extract(self, executor, line_number, line, extra):
        """
        Parse the output when extracting files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

        if line_number == 1:
            return

        password = False
        if line == 'password incorrect--reenter: ':
            message = _('wrong password, please try again')
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': message})
            extra.set('password', t_utils.get_password(None))
            password = True
        elif line.endswith(' password: '):
            # <-- len+3 --->        <-- 11 --->
            # [archive.zip] file.txt password:
            filename = line[len(extra.get('archive'))+3:-11]
            extra.set('password', t_utils.get_password(filename))
            password = True
        if password:
            executor.send_line(extra.get('password'))
            return

        file = extra.get('last_file')
        if file:
            moved = t_file_utils.move_extracted(file, extra)
            if moved:
                t_gui.extracting_msg(file)
            t_gui.advance_progress()

        if (line.startswith('   creating: ') or line.startswith('  inflating: ') or
            line.startswith(' extracting: ') or line.startswith('    linking: ')):
            extra.set('last_file', extra.get('contents').pop(0)[0])
        elif len(line) > 0:
            t_gui.warn(_('%(prog)s: warning: %(message)s\n') %
                {'prog': 'tarumba', 'message': line})
