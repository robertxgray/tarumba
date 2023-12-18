# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's tar archive support"

from gettext import gettext as _
import shlex

from tarumba.config import current as config
import tarumba.file_utils as t_file_utils
from tarumba.format import format as t_format
from tarumba.gui import current as t_gui

class Tar(t_format.Format):
    "Tar archive support functions"

    NAME = 'tar'

    # The format can store duplicates
    CAN_DUPLICATE = True
    # The format can store multiple files
    CAN_PACK = True
    # The format can store special files
    CAN_SPECIAL = True

    def list_commands(self, archive):
        """
        Commands to list the archive contents.

        :param archive: Archive name
        :return: List of commands
        """

        return [(config.get('tar_bin'), ['--numeric-owner', '--quoting-style=shell-always', '-tvf', archive])]

    def parse_listing(self, contents, columns):
        """
        Parse the archive contents listing.

        :param contents: Archive contents listing
        :param columns: Requested columns or None for default
        :return: Listing parsed as rows
        """

        if not columns:
            columns = config.get('tar_columns')
        listing = [columns]
        for content in contents:
            row = []
            elements = content.split(None, 5)
            for column in columns:
                if column == t_format.PERMS:
                    row.append(elements[0])
                elif column == t_format.OWNER:
                    row.append(elements[1])
                elif column == t_format.SIZE:
                    row.append(elements[2])
                elif column == t_format.DATE:
                    row.append(f'{elements[3]} {elements[4]}')
                elif column == t_format.NAME:
                    row.append(shlex.split(elements[5])[0])
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
            elements = content.split(None, 5)
            listing.add(shlex.split(elements[5])[0])
        return listing

    def add_commands(self, add_args, files):
        """
        Commands to add files to an archive.

        :param add_args: AddArgs object
        :param files: List of files
        :return: List of commands
        """

        commands = []

        if add_args.get('follow_links'):
            params = '-rvhf'
        else:
            params = '-rvf'
        commands.append((config.get('tar_bin'), [params, add_args.get('archive'), '--', files]))

        return commands

    def parse_add(self, line_number, line, extra):
        """
        Parse the output when adding files.

        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        :return: True if the line has been successfully parsed
        """

        if 'tar: ' in line:
            t_gui.warn(line)
        else:
            if config.get('verbose'):
                t_gui.info(_('adding: [cyan]%(file)s[/cyan]') % {'file': line})
        t_gui.advance_progress()
        return True

    def extract_commands(self, extract_args):
        """
        Commands to extract files from an archive.

        :param extract_args: ExtractArgs object
        :return: List of commands
        """

        commands = []

        commands.append((config.get('tar_bin'),
            ['-xvf', extract_args.get('archive'), '--'] + extract_args.get('files')))

        return commands

    def parse_extract(self, line_number, line, extra):
        """
        Parse the output when extracting files.

        :param line_number: Line number
        :param line: Line contents
        :param extra: Extra data
        :return: True if the line has been successfully parsed
        """

        moved = t_file_utils.move_extracted(line, extra)
        if moved and config.get('verbose'):
            t_gui.info(_('extracting: [cyan]%(file)s[/cyan]') % {'file': line})
        t_gui.advance_progress()
        return True
