# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's 7z backend support"

from gettext import gettext as _

from tarumba.config import current as config
import tarumba.file_utils as t_file_utils
from tarumba.backend import backend as t_backend
from tarumba.gui import current as t_gui
import tarumba.utils as t_utils

class _7z(t_backend.Backend):
    "7z archiver backend"

    # List of programs used to add
    COMPRESSORS = [config.get('7z_s_7z_bin')]
    # List of programs used to list and extract
    EXTRACTORS = [config.get('7z_s_7z_bin')]

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

    # 7z uses this string to mark the start of the list of files
    LIST_START = '----------'


    def __init__(self, mime):
        """
        Backend constructor.

        :param mime: Archive mime type
        """

        super().__init__(mime)
        self._list_started = False
        self._current_file = {}

    def list_commands(self, list_args):
        """
        Commands to list the archive contents.

        :param list_args: ListArgs object
        :return: List of commands
        """

        return [(config.get('7z_s_7z_bin'), ['l', '-slt', '--',
            list_args.get('archive')] + list_args.get('files'))]

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

        return [(config.get('zip_s_unzip_bin'),
            ['-o', '--', extract_args.get('archive')] + list_args.get('files'))]

    def parse_list(self, executor, line_number, line, extra):
        """
        Parse the output when listing files.

        :param executor: Program executor
        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        """

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
                    row = []
                    for column in columns:
                        row.append(self._current_file.get(column))
                    output.append(row)
                    self._current_file = {}

                elif line.startswith('Path = '):
                    self._current_file[t_backend.NAME] = line[7:]
                elif line.startswith('Size = '):
                    self._current_file[t_backend.SIZE] = line[7:]
                elif line.startswith('Packed Size = '):
                    self._current_file[t_backend.PACKED] = line[14:]
                elif line.startswith('Modified = '):
                    self._current_file[t_backend.DATE] = line[11:-3]
                elif line.startswith('Attributes = '):
                    self._current_file[t_backend.PERMS] = line[-10:]
                elif line.startswith('Encrypted = '):
                    self._current_file[t_backend.ENC] = line[12:]
                elif line.startswith('CRC = '):
                    self._current_file[t_backend.CRC] = line[6:]
                elif line.startswith('Method = '):
                    self._current_file[t_backend.METHOD] = line[9:]

            # Set output
            if isinstance(output, set):
                if line.startswith('Path = '):
                    output.add(line[7:])

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
