# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's test utils"

import dataclasses
import os
import pathlib
import shutil
import sys

from tarumba.__main__ import main

TEST_PATH = "test_files"
PREFFIX = "¡!|<>'\"^#$%&@€(){}[]=¿?*-+Ñ_"  # Testing problematic chars


@dataclasses.dataclass
class TestParams:
    "Test params class"

    backend: str
    binary: str
    archive: str


def _add_preffix_to_files(files):
    """
    Adds the preffix to a list of files.
    :param files: List of files
    :return: Lis of files with preffix
    """

    out = []
    for file in files:
        if file[0] == "/":
            out.append(file)
        else:
            out.append(PREFFIX + file)
    return out


def test_add(archive, files, extra_args):
    """
    Test add command.

    :param archive: Archive path
    :param files: Files to add
    :param extra_args: Extra arguments
    """

    cwd = os.getcwd()
    os.chdir(TEST_PATH)
    try:
        sys.argv = ["tarumba", "a", "-v", *extra_args]
        sys.argv.append(PREFFIX + archive)
        sys.argv += _add_preffix_to_files(files)
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

    sys.argv = ["tarumba", "l", *extra_args]
    sys.argv.append(os.path.join(TEST_PATH, PREFFIX + archive))
    sys.argv += _add_preffix_to_files(files)
    main()


def test_test(archive, files, extra_args):
    """
    Test test command.

    :param archive: Archive path
    :param archive: Files to test
    :param extra_args: Extra arguments
    """

    sys.argv = ["tarumba", "t", *extra_args]
    sys.argv.append(os.path.join(TEST_PATH, PREFFIX + archive))
    sys.argv += _add_preffix_to_files(files)
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
        sys.argv = ["tarumba", "e", "-v", *extra_args]
        sys.argv.append(PREFFIX + archive)
        sys.argv += _add_preffix_to_files(files)
        main()
    finally:
        os.chdir(cwd)


def test_rename(archive, files, extra_args):
    """
    Test rename command.

    :param archive: Archive path
    :param archive: Files to rename
    :param extra_args: Extra arguments
    """

    sys.argv = ["tarumba", "r", *extra_args]
    sys.argv.append(os.path.join(TEST_PATH, PREFFIX + archive))
    sys.argv += _add_preffix_to_files(files)
    main()


def test_delete(archive, files, extra_args):
    """
    Test delete command.

    :param archive: Archive path
    :param archive: Files to delete
    :param extra_args: Extra arguments
    """

    sys.argv = ["tarumba", "d", *extra_args]
    sys.argv.append(os.path.join(TEST_PATH, PREFFIX + archive))
    sys.argv += _add_preffix_to_files(files)
    main()


def _get_test_path(path, dest=None, *, archive_folder=None, use_preffix=True):
    """
    Returns paths in the tests dir.

    :param path: Original path
    :param dest: Optional destination name
    :param archive_folder: Optional archive folder
    :param use_preffix: Apply multichar preffix
    """

    if archive_folder is not None:
        archive_base = pathlib.Path(archive_folder).stem
        test_dir = os.path.join(TEST_PATH, PREFFIX + archive_base)
    else:
        test_dir = TEST_PATH
    if dest:
        if use_preffix:
            return os.path.join(test_dir, PREFFIX + dest)
        return os.path.join(test_dir, dest)
    if use_preffix:
        base_name = os.path.basename(path)
        dir_name = os.path.dirname(path)
        return os.path.join(test_dir, os.path.join(dir_name, PREFFIX + base_name))
    return os.path.join(test_dir, path)


def copy(path, dest=None, *, use_preffix=True):
    """
    Copies a file or folder to the tests dir.

    :param path: Original path
    :param dest: Optional destination name
    :param use_preffix: Apply multichar preffix
    """

    test_path = _get_test_path(path, dest, use_preffix=use_preffix)
    if os.path.isdir(path):
        shutil.copytree(path, test_path, symlinks=True)
    else:
        shutil.copy2(path, test_path, follow_symlinks=False)


def link(path, dest=None, *, use_preffix=True):
    """
    Creates a symbolic link in the tests dir.

    :param path: Original path
    :param dest: Optional destination name
    :param use_preffix: Apply multichar preffix
    """

    test_path = _get_test_path(path, dest, use_preffix=use_preffix)
    if use_preffix:
        os.symlink(PREFFIX + path, test_path)
    else:
        os.symlink(path, test_path)


def cleanup(path, *, archive_folder=None, use_preffix=True):
    """
    Delete a file or folder in the tests dir.

    :param path: Path to delete
    :param archive_folder: Optional archive folder
    :param use_preffix: Apply multichar preffix
    """

    test_path = _get_test_path(path, archive_folder=archive_folder, use_preffix=use_preffix)
    if os.path.isdir(test_path):
        shutil.rmtree(test_path, ignore_errors=True)
    elif os.path.lexists(test_path):
        os.remove(test_path)


def assert_file_exists(path, *, archive_folder=None, use_preffix=True):
    """
    Asserts that a file exists in the tests dir.

    :param file: File path
    :param archive_folder: Optional archive folder
    :param use_preffix: Apply multichar preffix
    """

    test_path = _get_test_path(path, archive_folder=archive_folder, use_preffix=use_preffix)
    assert os.path.isfile(test_path)
    assert not os.path.islink(test_path)


def assert_dir_exists(path, *, archive_folder=None, use_preffix=True):
    """
    Asserts that a directory exists in the tests dir.

    :param dir: Directory path
    :param archive_folder: Optional archive folder
    :param use_preffix: Apply multichar preffix
    """

    test_path = _get_test_path(path, archive_folder=archive_folder, use_preffix=use_preffix)
    assert os.path.isdir(test_path)
    assert not os.path.islink(test_path)


def assert_link_exists(path, *, archive_folder=None, use_preffix=True):
    """
    Asserts that a link exists in the tests dir.

    :param file: Link path
    :param archive_folder: Optional archive folder
    :param use_preffix: Apply multichar preffix
    """

    test_path = _get_test_path(path, archive_folder=archive_folder, use_preffix=use_preffix)
    assert os.path.islink(test_path)
