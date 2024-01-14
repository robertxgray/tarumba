# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's zip tests"

from tests import utils as test_utils

def test_add_new():
    "Create an archive"

    test_utils.test_add('test.zip', ['src/tarumba'], [], force_new=True)

def test_add_existing():
    "Add files to the archive"

    test_utils.test_add('test.zip', ['README.md'], [])

def test_add_overwrite():
    "Add files to the archive and overwrite"

    test_utils.test_add('test.zip', ['README.md'], ['-a'])

def test_add_none():
    "Add files to the archive without overwriting"

    test_utils.test_add('test.zip', ['README.md'], ['-n'])

def test_add_path():
    "Add files to the archive with path"

    test_utils.test_add('test.zip', ['README.md'], ['-p','path'])

def test_add_level():
    "Add files to the archive with level"

    test_utils.test_add('test.zip', ['README.md'], ['-a','-l','6'])

def test_list_one():
    "List one content"

    test_utils.test_list('test.zip', ['README.md'], [])

def test_list_all():
    "List all contents"

    test_utils.test_list('test.zip', [], [])

def test_list_columns():
    "List all contents with custom columns"

    test_utils.test_list('test.zip', [], ['-c','NAME'])

def test_extract_one():
    "Extract one file from the archive"

    test_utils.test_extract('test.zip', ['README.md'], ['-a'])

def test_extract_all():
    "Extract all files from the archive"

    test_utils.test_extract('test.zip', [], ['-a'])

def test_extract_none():
    "Extract all files from the archive without overwriting"

    test_utils.test_extract('test.zip', [], ['-n'])
