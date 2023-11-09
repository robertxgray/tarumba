# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config, executor, utils
from tarumba.format import format
from tarumba.gui import current as gui

import os

class Tar(format.Format):

    def list_commands(self, archive):
        """
        Commands to list the archive contents.

        :param archive: Archive name
        :return: List of commands
        """

        return [(config.TAR_BIN, ['--numeric-owner', '-tvf', archive])]

    def parse_listing(self, contents, columns):
        """
        Parse the archive contents listing.

        :param contents: Archive contents listing
        :param columns: Requestes columns or None for default
        :return: Listing parsed as rows
        """

        if not columns:
            columns = config.TAR_COLUMNS
        listing = [columns]
        for content in contents:
            row = []
            elements = content.split(None, 5)
            for column in columns:
                if column == format.PERMS:
                    row.append(elements[0])
                elif column == format.OWNER:
                    row.append(elements[1])
                elif column == format.SIZE:
                    row.append(elements[2])
                elif column == format.DATE:
                    row.append('%s %s' % (elements[3], elements[4]))
                elif column == format.NAME:
                    row.append(elements[5])
            listing.append(row)
        return listing

    def compress_commands(self, archive, files):
        """
        Commands to compress files into an archive.

        :param archive: Archive name
        :param contents: Files root path
        :return: List of commands
        """

        commands = []

        safe_files = files
        if files.startswith('/'):
            commands.append((executor.CHDIR, ['/']))
            safe_files = files[1:]

        if config.FOLLOW_LINKS:
            params = '-rvhf'
        else:
            params = '-rvf'
        commands.append((config.TAR_BIN, [params, archive, '--', safe_files]))

        return commands

    def parse_compress(self, line_number, line):
        """
        Parse the compression output.

        :param line_number: Line number
        :param line: Line contents
        """

        if 'tar: ' in line:
            gui.warn(line)
        else:
            if config.VERBOSE:
                gui.info(line)
        gui.advance_progress()
