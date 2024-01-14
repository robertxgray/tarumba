# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's tar tests"

from tests import utils as test_utils

def test_add_new():
    "Create an archive"

    test_utils.test_add('test.tar', ['src/tarumba'], [], True)

def test_add_existing():
    "Add files to the archive"

    test_utils.test_add('test.tar', ['README.md'], [])

def test_add_duplicate():
    "Add duplicated files to the archive"

    test_utils.test_add('test.tar', ['README.md'], [])

def test_add_path():
    "Add files to the archive with path"

    test_utils.test_add('test.tar', ['README.md'], ['-p','path'])

def test_list_one():
    "List one content"

    test_utils.test_list('test.tar', ['README.md'], [])

def test_list_all():
    "List all contents"

    test_utils.test_list('test.tar', [], [])

def test_list_columns():
    "List all contents with custom columns"

    test_utils.test_list('test.tar', [], ['-c','NAME'])

def test_extract_one():
    "Extract one file from the archive"

    test_utils.test_extract('test.tar', ['README.md'], ['-a'])

def test_extract_occurrence():
    "Extract one file from the archive with occurrence"

    test_utils.test_extract('test.tar', ['README.md'], ['-a','-o','1'])

def test_extract_all():
    "Extract all files from the archive"

    test_utils.test_extract('test.tar', [], ['-a'])

def test_extract_none():
    "Extract all files from the archive without overwriting"

    test_utils.test_extract('test.tar', [], ['-n'])
