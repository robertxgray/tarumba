# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import executor
from tarumba.format import tar
import gettext

_ = gettext.gettext

def list(args):
    """
    List archive contents.

    :param args: Input arguments
    """

    format = tar.Tar()

    print(str(args))
    commands = format.list_commands(args.archive)
    print(str(commands))
    output = executor.execute(commands)
    print(str(output))
