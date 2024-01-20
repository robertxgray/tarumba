# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's test utils"

import os
import shutil
import sys

from tarumba.__main__ import main

TEST_PATH = 'test_files'

def test_add(archive, files, extra_args, force_new=False):
    """
    Test add command.

    :param archive: Archive path
    :param archive: Files to add
    :param extra_args: Extra arguments
    :param force_new: If true, existing archives will be removed
    """

    archive_path = os.path.join(TEST_PATH, archive)
    if force_new and os.path.isfile(archive_path):
        os.remove(archive_path)
    sys.argv = ['tarumba', 'a', '-v'] + extra_args
    sys.argv.append(archive_path)
    sys.argv += files
    main()

def test_list(archive, files, extra_args):
    """
    Test list command.

    :param archive: Archive path
    :param archive: Files to list
    :param extra_args: Extra arguments
    """

    sys.argv = ['tarumba', 'l'] + extra_args
    sys.argv.append(os.path.join(TEST_PATH, archive))
    sys.argv += files
    main()

def test_extract(archive, files, extra_args):
    """
    Test extract command.

    :param archive: Archive path
    :param archive: Files to extract
    :param extra_args: Extra arguments
    """

    cwd = os.getcwd()
    os.chdir(TEST_PATH)
    sys.argv = ['tarumba', 'e', '-v'] + extra_args
    sys.argv.append(archive)
    sys.argv += files
    main()
    os.chdir(cwd)

def cleanup(path):
    """
    Delete a file or folder in the tests dir.

    :param path: Path to delete
    """

    test_path = os.path.join(TEST_PATH, path)
    if os.path.isdir(test_path):
        shutil.rmtree(test_path, ignore_errors=True)
    else:
        os.remove(test_path)
