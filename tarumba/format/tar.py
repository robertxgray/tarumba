# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import configuration, utils
from tarumba.format import format
import os

class Tar(format.Format):

    def list_commands(self, archive):
        """
        Commands to list the archive contents.

        :param archive: Archive path
        :return: List of commands
        """

        basename = os.path.basename(archive)
        # Check for multivolume
        volumes = utils.get_volumes(archive)
        if volumes:
            pass
            # Numeric owner to avoid problems with odd user and group names
            #return [('Pipelines.py', ['!', configuration.CAT_BIN] + volumes + 
            #    ['///', configuration.TAR_BIN, '--numeric-owner', '-tv'],
            #    _(u'Reading contents of the file %s') % basename)]
        else:
            return [(configuration.TAR_BIN, ['--numeric-owner', '-tvf', archive])]

    def parse_listing(self, contents):
        """
        Parse the archive contents listing.

        :param contents: Archive contents listing
        :return: Listing parsed as rows
        """

        listing = [(self.PERMS, self.USER, self.GROUP, self.SIZE, self.DATE, self.TIME, self.NAME)]
        for content in contents:
            columns = content.split(None, 5)
            user_group = columns[1].split('/')
            listing.append((
                columns[0],
                user_group[0],
                user_group[1],
                columns[2],
                columns[3],
                columns[4],
                columns[5]
            ))
        return listing
