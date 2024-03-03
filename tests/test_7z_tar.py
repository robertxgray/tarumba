# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's 7z backend with tar archive tests"

import os

from tests import utils as test_utils

from tarumba.config import current as config

ARCHIVE='test.tar'
DIR='src'
FILE='README.md'
LINK1='link1'
LINK2='link2'
PATH='path'
X7Z_BIN='7zz'

def test_configure():
    "Not a real test, just configuration"

    config.set('backends_l_7z_bin', [X7Z_BIN])
    test_cleanup()
    test_utils.copy(DIR)
    test_utils.copy(FILE)
    test_utils.link(FILE, LINK1)
    test_utils.link(FILE, LINK2)

def test_add_new():
    "Create an archive"

    test_utils.test_add(ARCHIVE, [DIR], ['-b','7z'])
    test_utils.assert_file_exists(ARCHIVE)

def test_add_existing():
    "Add files to the archive"

    test_utils.test_add(ARCHIVE, [FILE], ['-b','7z'])
    test_utils.assert_file_exists(ARCHIVE)

def test_add_path():
    "Add files to the archive with path"

    test_utils.test_add(ARCHIVE, [FILE], ['-b','7z','-p',PATH])
    test_utils.assert_file_exists(ARCHIVE)

def test_add_links():
    "Add links to the archive"

    test_utils.test_add(ARCHIVE, [LINK1], ['-b','7z'])
    test_utils.assert_file_exists(ARCHIVE)

def test_add_links_follow():
    "Add links to the archive"

    test_utils.test_add(ARCHIVE, [LINK2], ['-b','7z','-f'])
    config.set('main_b_follow_links', False)
    test_utils.assert_file_exists(ARCHIVE)

def test_list_one():
    "List one content"

    test_utils.test_list(ARCHIVE, [FILE], ['-b','7z'])

def test_list_all():
    "List all contents"

    test_utils.test_list(ARCHIVE, [], ['-b','7z'])

def test_list_columns():
    "List all contents with custom columns"

    test_utils.test_list(ARCHIVE, [], ['-b','7z','-c','NAME'])

def test_extract_one():
    "Extract one file from the archive"

    test_utils.test_extract(ARCHIVE, [FILE], ['-b','7z','-a'])
    test_utils.assert_file_exists(FILE)

def test_extract_prompt(mocker):
    "Extract one file from the archive with prompt"

    mocker.patch('rich.prompt.Prompt.ask', return_value='n')
    test_utils.test_extract(ARCHIVE, [FILE], ['-b','7z'])
    test_utils.assert_file_exists(FILE)

def test_extract_all():
    "Extract all files from the archive"

    test_utils.cleanup(DIR)
    test_utils.cleanup(FILE)
    test_utils.cleanup(LINK1)
    test_utils.cleanup(LINK2)
    test_utils.test_extract(ARCHIVE, [], ['-b','7z','-a'])
    test_utils.assert_dir_exists(DIR)
    test_utils.assert_file_exists(FILE)
    test_utils.assert_file_exists(os.path.join(PATH, FILE))
    test_utils.assert_link_exists(LINK1)
    test_utils.assert_file_exists(LINK2)

def test_extract_none():
    "Extract all files from the archive without overwriting"

    test_utils.test_extract(ARCHIVE, [], ['-b','7z','-n'])
    test_utils.assert_dir_exists(DIR)
    test_utils.assert_file_exists(FILE)
    test_utils.assert_file_exists(os.path.join(PATH, FILE))
    test_utils.assert_link_exists(LINK1)
    test_utils.assert_file_exists(LINK2)

def test_cleanup():
    "Not a real test, just the cleanup"

    test_utils.cleanup(ARCHIVE)
    test_utils.cleanup(DIR)
    test_utils.cleanup(FILE)
    test_utils.cleanup(LINK1)
    test_utils.cleanup(LINK2)
    test_utils.cleanup(PATH)
