# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's test utils"

import os
import pathlib
import shutil
import sys

from tarumba.__main__ import main

TEST_PATH = 'test_files'

class TestParams:
    "Test params class"

    def __init__(self, backend, binary, archive):
        """
        Test params constructor.
        """

        self.backend = backend
        self.binary = binary
        self.archive = archive

def test_add(archive, files, extra_args):
    """
    Test add command.

    :param archive: Archive path
    :param archive: Files to add
    :param extra_args: Extra arguments
    """

    cwd = os.getcwd()
    os.chdir(TEST_PATH)
    try:
        sys.argv = ['tarumba', 'a', '-v', *extra_args]
        sys.argv.append(archive)
        sys.argv += files
        main()
    finally:
        os.chdir(cwd)

def test_list(archive, files, extra_args):
    """
    Test list command.

    :param archive: Archive path
    :param archive: Files to list
    :param extra_args: Extra arguments
    """

    sys.argv = ['tarumba', 'l', *extra_args]
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
    try:
        sys.argv = ['tarumba', 'e', '-v', *extra_args]
        sys.argv.append(archive)
        sys.argv += files
        main()
    finally:
        os.chdir(cwd)

def _get_test_path(path, dest=None, archive_folder=None):
    """
    Returns paths in the tests dir.

    :param path: Original path
    :param dest: Optional destination name
    :param archive_folder: Optional archive folder
    """

    if archive_folder is not None:
        archive_base = pathlib.Path(archive_folder).stem
        test_dir = os.path.join(TEST_PATH, archive_base)
    else:
        test_dir = TEST_PATH
    if dest:
        return os.path.join(test_dir, dest)
    return os.path.join(test_dir, path)

def copy(path, dest=None):
    """
    Copies a file or folder to the tests dir.

    :param path: Original path
    :param dest: Optional destination name
    """

    test_path = _get_test_path(path, dest)
    if os.path.isdir(path):
        shutil.copytree(path, test_path, symlinks=True)
    else:
        shutil.copy2(path, test_path, follow_symlinks=False)

def link(path, dest=None):
    """
    Creates a symbolic link in the tests dir.

    :param path: Original path
    :param dest: Optional destination name
    """

    test_path = _get_test_path(path, dest)
    os.symlink(path, test_path)

def cleanup(path, archive_folder=None):
    """
    Delete a file or folder in the tests dir.

    :param path: Path to delete
    :param archive_folder: Optional archive folder
    """

    test_path = _get_test_path(path, archive_folder=archive_folder)
    if os.path.isdir(test_path):
        shutil.rmtree(test_path, ignore_errors=True)
    elif os.path.lexists(test_path):
        os.remove(test_path)

def assert_file_exists(path, archive_folder=None):
    """
    Asserts that a file exists in the tests dir.

    :param file: File path
    :param archive_folder: Optional archive folder
    """

    test_path = _get_test_path(path, archive_folder=archive_folder)
    assert os.path.isfile(test_path)
    assert not os.path.islink(test_path)

def assert_dir_exists(path, archive_folder=None):
    """
    Asserts that a directory exists in the tests dir.

    :param dir: Directory path
    :param archive_folder: Optional archive folder
    """

    test_path = _get_test_path(path, archive_folder=archive_folder)
    assert os.path.isdir(test_path)
    assert not os.path.islink(test_path)

def assert_link_exists(path, archive_folder=None):
    """
    Asserts that a link exists in the tests dir.

    :param file: Link path
    :param archive_folder: Optional archive folder
    """

    test_path = _get_test_path(path, archive_folder=archive_folder)
    assert os.path.islink(test_path)
