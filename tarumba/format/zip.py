# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's zip archive support"

from gettext import gettext as _

from tarumba.config import current as config
import tarumba.file_utils as t_file_utils
from tarumba.format import format as t_format
from tarumba.gui import current as t_gui

class Zip(t_format.Format):
    "Zip archive support functions"

    NAME = 'zip'

    # The format can store duplicates
    CAN_DUPLICATE = False
    # The format can store multiple files
    CAN_PACK = True
    # The format can store special files
    CAN_SPECIAL = False

    def list_commands(self, archive, files):
        """
        Commands to list the archive contents.

        :param archive: Archive name
        :param files: List of files
        :return: List of commands
        """

        safe_files = []
        for file in files:
            safe_files.append(file+'*')
        return [(config.get('unzip_bin'), ['-Z', '-lT', '--h-t', '--', archive] + safe_files)]

    def parse_listing(self, contents, columns):
        """
        Parse the archive contents listing.

        :param contents: Archive contents listing
        :param columns: Requested columns or None for default
        :return: Listing parsed as rows
        """

        if not columns:
            columns = config.get('zip_columns')
        listing = [columns]
        for content in contents:
            row = []
            elements = content.split(None, 7)
            for column in columns:
                # We are ignoring the zip version and other metadata
                # They may be added in the future by popular demand
                if column == t_format.PERMS:
                    row.append(elements[0])
                elif column == t_format.SIZE:
                    row.append(elements[3])
                elif column == t_format.PACKED:
                    row.append(elements[5])
                elif column == t_format.DATE:
                    yea = elements[7][0:4]
                    mon = elements[7][4:6]
                    day = elements[7][6:8]
                    hou = elements[7][9:11]
                    mit = elements[7][11:13]
                    row.append(f'{yea}-{mon}-{day} {hou}:{mit}')
                elif column == t_format.NAME:
                    row.append(elements[7][16:])
            listing.append(row)
        return listing

    def parse_listing_2set(self, contents):
        """
        Parse the archive contents into a set.

        :param contents: Archive contents listing
        :return: Set of filenames
        """

        listing = set()
        for content in contents:
            elements = content.split(None, 7)
            listing.add(elements[7][16:])
        return listing

    def add_commands(self, add_args, files):
        """
        Commands to add files to an archive.

        :param add_args: AddArgs object
        :param contents: Files root path
        :return: List of commands
        """

        params = '-r'
        if not add_args.get('follow_links'):
            params += 'y'
        if add_args.get('level'):
            params += add_args.get('level')
        return [(config.get('zip_bin'), [params, add_args.get('archive'), '--', files])]

    def parse_add(self, line_number, line, extra):
        """
        Parse the output when adding files.

        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        :return: True if the line has been successfully parsed
        """

        if line.startswith('  adding:') or line.startswith('updating:'):
            if config.get('verbose'):
                end = line.find(' (stored ')
                t_gui.info(_('adding: [cyan]%(file)s[/cyan]') % {'file': line[10:end]})
            t_gui.advance_progress()
            return True
        if len(line) > 0:
            t_gui.warn(line)
            return False
        return True

    def extract_commands(self, extract_args):
        """
        Commands to extract files from an archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        return [(config.get('unzip_bin'),
            ['-o', '--', extract_args.get('archive')] + extract_args.get('files'))]

    def parse_extract(self, line_number, line, extra):
        """
        Parse the output when extracting files.

        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        :return: True if the line has been successfully parsed
        """

        file = extra.get('last_file')
        if file:
            moved = t_file_utils.move_extracted(file, extra)
            if moved and config.get('verbose'):
                t_gui.info(_('extracting: [cyan]%(file)s[/cyan]') % {'file': file})
            t_gui.advance_progress()

        if line.startswith('   creating:'):
            extra.set('last_file', line[13:])
        elif line.startswith('  inflating:') or line.startswith(' extracting:'):
            extra.set('last_file', line[13:-2]) # Zip adds 2 spaces at the end
        elif line.startswith('    linking:'):
            extra.set('last_file', line[13:line.find('  -> ')])
        else:
            extra.set('last_file', None)
            return False
        return True
