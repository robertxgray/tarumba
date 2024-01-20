# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's zip tests"

from tests import utils as test_utils

ARCHIVE='test.zip'
ARCHIVE_E='test_e.zip'
DIR='src'
FILE='README.md'
PATH='path'
PASSWORD='password'

def test_add_new():
    "Create an archive"

    test_utils.test_add(ARCHIVE, [DIR], [], force_new=True)

def test_add_new_encrypted(mocker):
    "Create an encrypted archive"

    mocker.patch('rich.prompt.Prompt.ask', return_value=PASSWORD)
    test_utils.test_add(ARCHIVE_E, [DIR], ['-e'], force_new=True)

def test_add_existing():
    "Add files to the archive"

    test_utils.test_add(ARCHIVE, [FILE], [])

def test_add_overwrite():
    "Add files to the archive and overwrite"

    test_utils.test_add(ARCHIVE, [FILE], ['-a'])

def test_add_none():
    "Add files to the archive without overwriting"

    test_utils.test_add(ARCHIVE, [FILE], ['-n'])

def test_add_path():
    "Add files to the archive with path"

    test_utils.test_add(ARCHIVE, [FILE], ['-p',PATH])

def test_add_level():
    "Add files to the archive with level"

    test_utils.test_add(ARCHIVE, [FILE], ['-a','-l','6'])

def test_list_one():
    "List one content"

    test_utils.test_list(ARCHIVE, [FILE], [])

def test_list_all():
    "List all contents"

    test_utils.test_list(ARCHIVE, [], [])

def test_list_columns():
    "List all contents with custom columns"

    test_utils.test_list(ARCHIVE, [], ['-c','NAME'])

def test_extract_one():
    "Extract one file from the archive"

    test_utils.test_extract(ARCHIVE, [FILE], ['-a'])

def test_extract_all():
    "Extract all files from the archive"

    test_utils.test_extract(ARCHIVE, [], ['-a'])

def test_extract_none():
    "Extract all files from the archive without overwriting"

    test_utils.test_extract(ARCHIVE, [], ['-n'])

def test_extract_encrypted(mocker):
    "Extract all files from an encrypted archive"

    mocker.patch('rich.prompt.Prompt.ask', return_value=PASSWORD)
    test_utils.test_extract(ARCHIVE_E, [], ['-a'])

def test_cleanup():
    "Not a real test, just the cleanup"

    test_utils.cleanup(ARCHIVE)
    test_utils.cleanup(ARCHIVE_E)
    test_utils.cleanup(DIR)
    test_utils.cleanup(FILE)
    test_utils.cleanup(PATH)
