# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's zip archive support"

from gettext import gettext as _

from tarumba.config import current as config
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

    def list_commands(self, archive):
        """
        Commands to list the archive contents.

        :param archive: Archive name
        :return: List of commands
        """

        return [(config.get('unzip_bin'), ['-Z', '-l', '--h-t', archive])]

    def parse_listing(self, contents, columns):
        """
        Parse the archive contents listing.

        :param contents: Archive contents listing
        :param columns: Requestes columns or None for default
        :return: Listing parsed as rows
        """

        if not columns:
            columns = config.get('zip_columns')
        listing = [columns]
        for content in contents:
            row = []
            elements = content.split(None, 9)
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
                    row.append(f'{elements[7]} {elements[8]}')
                elif column == t_format.NAME:
                    row.append(elements[9])
            listing.append(row)
        return listing

    def add_commands(self, archive, files):
        """
        Commands to add files to an archive.

        :param archive: Archive name
        :param contents: Files root path
        :return: List of commands
        """

        commands = []

        if config.get('follow_links'):
            params = '-r'
        else:
            params = '-ry'
        commands.append((config.get('zip_bin'), [params, archive, '--', files]))

        return commands

    def parse_add(self, line_number, line):
        """
        Parse the output when adding files.

        :param line_number: Line number
        :param line: Line contents
        :return: True if the line has been successfully parsed
        """

        if line.startswith('  adding:') or line.startswith('updating:'):
            if config.get('verbose'):
                end = line.find(' (stored ')
                t_gui.info(_('adding: [cyan]%(file)s[/cyan]') % {'file': line[10:end]})
        else:
            t_gui.warn(line)
        t_gui.advance_progress()
        return True
