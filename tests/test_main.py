# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's main function tests"

import sys

import pytest

from tarumba.__main__ import main


class TestMain:
    "Main function tests"

    def test_noargs(self):
        "Run the program without arguments"

        sys.argv = []
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 2

    def test_help(self):
        "Print the help"

        sys.argv = [
            'tarumba',
            '-h'
        ]
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0

    def test_help_nocolor(self):
        "Print the help without color"

        sys.argv = [
            'tarumba',
            '-h',
            '-m'
        ]
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0

    def test_help_debug(self):
        "Print the help with debugging"

        sys.argv = [
            'tarumba',
            '-h',
            '-d'
        ]
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
