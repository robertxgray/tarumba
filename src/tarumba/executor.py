# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's programs executor"

from collections import deque
from gettext import gettext as _
import os

import pexpect

from tarumba import utils as t_utils
from tarumba.gui import current as t_gui

# Pseudo-command to change the working directory
CHDIR = 'CHDIR'

class Executor:
    "Class implementing the programs executor"

    subprocess = None

    def execute_simple(self, command):
        """
        Executes a command, waits for it to finish and resturns all the output.

        :param command: Command
        :return: List of lines in command output
        """

        output = t_utils.decode(pexpect.run(command))
        t_gui.debug('output', output)
        return output.split('\r\n')

    def execute(self, commands, patterns, parser, extra):
        """
        Executes a list of commands via pexpect.

        :param commands: List of commands
        :param patterns: Particular patterns
        :param parser: Line parser
        :param extra: Extra data
        """

        # Save the current working directory
        old_cwd = os.getcwd()

        for command in commands:
            t_gui.debug('command', command)

            # Process directory changes
            if command[0] == CHDIR:
                os.chdir(command[1][0])
                continue

            if not patterns:
                patterns = []

            self.subprocess = pexpect.spawn(command[0], command[1], timeout=None, echo=False)

            # Read the subprocess output
            case = 1
            sub_output = None
            buffer = deque(maxlen=5)
            line = 1
            while case > 0:
                case = self.subprocess.expect([pexpect.EOF, '\r\n', '\n'] + patterns)
                t_gui.debug('case', case)
                if case > 0 or len(self.subprocess.before):
                    sub_output = t_utils.decode(self.subprocess.before)
                    if case >= 3:
                        sub_output += t_utils.decode(self.subprocess.after)
                    t_gui.debug('sub_output', sub_output)
                    buffer.append(sub_output)
                    parser(self, line, sub_output, extra)
                    line += 1

            self.subprocess.close()
            error = self.subprocess.status
            self.subprocess = None

            # Stop on error
            if error:
                message=_('failure in program %(program)s') % {'program': command[0]} + '\n'
                if buffer:
                    message += '\n'.join(buffer)
                raise ChildProcessError(message)

        # Restore the current working directory
        os.chdir(old_cwd)

    def send_line(self, line):
        """
        Function used to send data to the subprocess.

        :param line: String data to send
        """

        t_gui.debug('send_line', line)
        assert self.subprocess is not None, _('an archiver process is not running')
        self.subprocess.sendline(line)
