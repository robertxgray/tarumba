# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's main tests"

import sys

import pytest

from tarumba.__main__ import main

def test_noargs():
    "Run the program without arguments"

    with pytest.raises(SystemExit):
        exit_code = main()
        assert exit_code == 2

def test_help():
    "Print the help"

    sys.argv = [
        'tarumba',
        '-h'
    ]
    with pytest.raises(SystemExit):
        exit_code = main()
        assert exit_code == 0

def test_help_nocolor():
    "Print the help without color"

    sys.argv = [
        'tarumba',
        '-h',
        '-m'
    ]
    with pytest.raises(SystemExit):
        exit_code = main()
        assert exit_code == 0

def test_help_debug():
    "Print the help with debugging"

    sys.argv = [
        'tarumba',
        '-h',
        '-d'
    ]
    with pytest.raises(SystemExit):
        exit_code = main()
        assert exit_code == 0
