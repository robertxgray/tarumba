# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's programs executor"

from gettext import gettext as _
import os
import pexpect

from tarumba import utils as t_utils

# Pseudo-command to change the working directory
CHDIR = 'CHDIR'

def execute(commands, parser=None):
    """
    Executes a list of commands via pexpect.

    :param commands: List of commands
    :parser: Optional line parser
    :return: Unparsed commands output
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
        sub_output = None
        output = []
        line = 1
        while case > 0:
            case = subprocess.expect([pexpect.EOF, '\r\n', '\n'])
            if case > 0 or len(subprocess.before):
                save_line = True
                sub_output = t_utils.decode(subprocess.before)
                if parser:
                    if parser(line, sub_output):
                        save_line = False
                if save_line:
                    output.append(sub_output)
                line += 1

        subprocess.close()
        error = subprocess.status

        # Stop on error
        if error:
            message=_('failure in program %(program)s') % {'program': command[0]} + '\n'
            if sub_output:
                message += sub_output
            raise ChildProcessError(message)

    # Restore the current working directory
    os.chdir(old_cwd)
    return output
