# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import config, utils
from tarumba.format import format
import os

class Tar(format.Format):

    def list_commands(self, archive):
        """
        Commands to list the archive contents.

        :param args: Input arguments
        :return: List of commands
        """

        basename = os.path.basename(archive)
        # Check for multivolume
        volumes = utils.get_volumes(archive)
        if volumes:
            pass
            # Numeric owner to avoid problems with odd user and group names
            #return [('Pipelines.py', ['!', config.CAT_BIN] + volumes + 
            #    ['///', config.TAR_BIN, '--numeric-owner', '-tv'],
            #    _(u'Reading contents of the file %s') % basename)]
        else:
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