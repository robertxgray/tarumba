# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's tar tests"

from tests import utils as test_utils

ARCHIVE='test.tar'
DIR='src'
FILE='README.md'
PATH='path'

def test_add_new():
    "Create an archive"

    test_utils.test_add(ARCHIVE, [DIR], [], True)

def test_add_existing():
    "Add files to the archive"

    test_utils.test_add(ARCHIVE, [FILE], [])

def test_add_duplicate():
    "Add duplicated files to the archive"

    test_utils.test_add(ARCHIVE, [FILE], [])

def test_add_path():
    "Add files to the archive with path"

    test_utils.test_add(ARCHIVE, [FILE], ['-p',PATH])

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

def test_extract_prompt(mocker):
    "Extract one file from the archive with prompt"

    mocker.patch('rich.prompt.Prompt.ask', return_value='n')
    test_utils.test_extract(ARCHIVE, [FILE], [])

def test_extract_occurrence():
    "Extract one file from the archive with occurrence"

    test_utils.test_extract(ARCHIVE, [FILE], ['-a','-o','1'])

def test_extract_all():
    "Extract all files from the archive"

    test_utils.test_extract(ARCHIVE, [], ['-a'])

def test_extract_none():
    "Extract all files from the archive without overwriting"

    test_utils.test_extract(ARCHIVE, [], ['-n'])

def test_cleanup():
    "Not a real test, just the cleanup"

    test_utils.cleanup(ARCHIVE)
    test_utils.cleanup(DIR)
    test_utils.cleanup(FILE)
    test_utils.cleanup(PATH)
