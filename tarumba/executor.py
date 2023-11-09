# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import utils

from gettext import gettext as _
import os
import pexpect

# Pseudo-command to change the working directory
CHDIR = 'CHDIR'

def execute(commands, parser=None):
    """
    Executes a list of commands via pexpect.

    :param commands: List of commands
    :parser: Optional line parser
    :return: Commands output
    """

    # Save the current working directory
    old_cwd = os.getcwd()

    for command in commands:

        # Process directory changes
        if command[0] == CHDIR:
            os.chdir(command[1][0])
            continue

        subprocess = pexpect.spawn(command[0], command[1], timeout=None, echo=False)

        # Read the subprocess output
        case = 1
        output = []
        line = 1
        while case > 0:
            case = subprocess.expect([pexpect.EOF, '\r\n', '\n'])
            if case > 0 or len(subprocess.before):
                sub_output = utils.decode(subprocess.before)
                output.append(sub_output)
                if parser:
                    parser(line, sub_output)
                line += 1

        subprocess.close()
        error = subprocess.status

        # Stop on error
        if error:
            message=_('failure in program %(program)s') % {'program': command[0]} + '\n'
            raise ChildProcessError(message + '\n'.join(output[-3:]))

    # Restore the current working directory
    os.chdir(old_cwd)
    return output
