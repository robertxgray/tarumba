# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's tar archive support"

from gettext import gettext as _

from tarumba.config import current as config
from tarumba import executor as t_executor
from tarumba.format import format as t_format
from tarumba.gui import current as t_gui

class Tar(t_format.Format):

    "Tar archive support functions"

    def list_commands(self, archive):
        """
        Commands to list the archive contents.

        :param archive: Archive name
        :return: List of commands
        """

        return [(config.get('tar_bin'), ['--numeric-owner', '-tvf', archive])]

    def parse_listing(self, contents, columns):
        """
        Parse the archive contents listing.

        :param contents: Archive contents listing
        :param columns: Requestes columns or None for default
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
                    row.append(elements[5])
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

        safe_files = files
        if files.startswith('/'):
            commands.append((t_executor.CHDIR, ['/']))
            safe_files = files[1:]

        if config.get('follow_links'):
            params = '-rvhf'
        else:
            params = '-rvf'
        commands.append((config.get('tar_bin'), [params, archive, '--', safe_files]))

        return commands

    def parse_add(self, line_number, line):
        """
        Parse the output when adding files.

        :param line_number: Line number
        :param line: Line contents
        :return: True if the line has been successfully parsed
        """

        if 'tar: ' in line:
            t_gui.warn(line)
        else:
            if config.get('verbose'):
                t_gui.info(_('adding: [cyan]%(file)s[/cyan]') % {'file': line})
        t_gui.advance_progress()
        return True
