# Copyright: (c) 2024, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's backend tests"

import os
from pathlib import Path

import pytest

import tarumba.classifier as t_classifier
import tarumba.constants as t_constants
from tarumba.config import current as config
from tests import utils as test_utils

test_params_list = [
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7zz', 'test_7zz.7z'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7zz', 'test_7zz.tar'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7zz', 'test_7zz.zip'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7zz', 'test_7zz.gz'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7zz', 'test_7zz.bz2'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7zz', 'test_7zz.xz'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7z', 'test_7z.7z'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7z', 'test_7z.tar'),
    test_utils.TestParams(t_constants.BACKEND_7ZIP, '7z', 'test_7z.zip'),
    test_utils.TestParams(t_constants.BACKEND_TAR, 'tar', 'test_tar.tar')
]

@pytest.fixture(scope="session", params=test_params_list)
def test_params(request):
    return request.param

class TestBackend:
    "Backend tests"

    DIR='src'
    FILE1='README.md'
    FILE2='COPYING'
    LINK1='link1'
    LINK2='link2'
    PASSWORD='password'
    PATH1='path1'
    PATH2='path2'

    def test_configure(self, test_params):
        "Not a real test, just configuration"

        config.put('backends_l_7zip_bin', [test_params.binary])
        config.put('backends_l_tar_bin', [test_params.binary])
        self.test_cleanup(test_params)
        test_utils.copy(self.DIR)
        test_utils.copy(self.FILE1)
        test_utils.copy(self.FILE2)
        test_utils.link(self.FILE1, self.LINK1)
        test_utils.link(self.FILE2, self.LINK2)

    def test_add_new(self, test_params):
        "Create an archive"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_ADD)
        if backend.can_pack():
            test_utils.test_add(test_params.archive, [self.DIR], ['-b',test_params.backend])
            test_utils.assert_file_exists(test_params.archive)
        else:
            with pytest.raises(SystemExit):
                test_utils.test_add(test_params.archive, [self.DIR], ['-b',test_params.backend])

    def test_add_new_encrypted(self, test_params, mocker):
        "Create an encrypted archive"

        backend = t_classifier.detect_format(
            test_params.backend, 'e_'+test_params.archive, t_constants.OPERATION_ADD)
        if backend.can_encrypt():
            mocker.patch('rich.prompt.Prompt.ask', return_value=self.PASSWORD)
            test_utils.test_add(
                'e_'+test_params.archive, [self.DIR], ['-b',test_params.backend,'-e'])
            test_utils.assert_file_exists(test_params.archive)
        else:
            with pytest.raises(SystemExit):
                test_utils.test_add(
                    'e_'+test_params.archive, [self.DIR], ['-b',test_params.backend,'-e'])

    def test_add_existing(self, test_params):
        "Add files to the archive"

        test_utils.test_add(test_params.archive, [self.FILE1], ['-b',test_params.backend])
        test_utils.assert_file_exists(test_params.archive)

    def test_add_duplicate(self, test_params):
        "Add duplicated files to the archive"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_ADD)
        if backend.can_duplicate():
            test_utils.test_add(test_params.archive, [self.FILE1], ['-b',test_params.backend])
            test_utils.assert_file_exists(test_params.archive)

    def test_add_level(self, test_params):
        "Add files to the archive with level"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_ADD)
        if not backend.can_pack():
            test_utils.cleanup(test_params.archive)

        test_utils.test_add(
            test_params.archive, [self.FILE2], ['-b',test_params.backend,'-l','3'])
        test_utils.assert_file_exists(test_params.archive)

    def test_add_path(self, test_params):
        "Add files to the archive with path"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_ADD)
        if backend.can_pack():
            test_utils.test_add(
                test_params.archive, [self.FILE1], ['-b',test_params.backend,'-p',self.PATH1])
            test_utils.assert_file_exists(test_params.archive)
        else:
            with pytest.raises(SystemExit):
                test_utils.test_add(
                    test_params.archive, [self.FILE1], ['-b',test_params.backend,'-p',self.PATH1])

    def test_add_path_follow(self, test_params):
        "Add files to the archive with path and follow links"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_ADD)
        if backend.can_pack():
            test_utils.test_add(
                test_params.archive, [self.FILE1], ['-b',test_params.backend,'-p',self.PATH2,'-k'])
            test_utils.assert_file_exists(test_params.archive)
        else:
            with pytest.raises(SystemExit):
                test_utils.test_add(test_params.archive, [self.FILE1],
                    ['-b',test_params.backend,'-p',self.PATH2,'-k'])

    def test_add_links(self, test_params):
        "Add links to the archive"

        # https://github.com/p7zip-project/p7zip/issues/39
        if test_params.binary == '7z':
            return

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_ADD)
        if backend.can_pack():
            test_utils.test_add(test_params.archive, [self.LINK1], ['-b',test_params.backend])
            test_utils.assert_file_exists(test_params.archive)
        else:
            with pytest.raises(SystemExit):
                test_utils.test_add(test_params.archive, [self.LINK1], ['-b',test_params.backend])

    def test_add_links_follow(self, test_params):
        "Add links to the archive with follow links"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_ADD)
        if not backend.can_pack():
            test_utils.cleanup(test_params.archive)

        test_utils.test_add(test_params.archive, [self.LINK2], ['-b',test_params.backend,'-k'])
        config.put('main_b_follow_links', False)
        test_utils.assert_file_exists(test_params.archive)

    def test_list_one(self, test_params):
        "List one content"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_LIST)
        if backend.can_pack() or backend.mime[0] == t_constants.MIME_GZIP:
            file_name = self.LINK2
        else:
            file_name = Path(test_params.archive).stem
        test_utils.test_list(test_params.archive, [file_name], ['-b',test_params.backend])

    def test_list_all(self, test_params):
        "List all contents"

        test_utils.test_list(test_params.archive, [], ['-b',test_params.backend])

    def test_list_columns(self, test_params):
        "List all contents with custom columns"

        test_utils.test_list(test_params.archive, [], ['-b',test_params.backend,'-c','NAME'])

    def test_list_encrypted(self, test_params, mocker):
        "Lists an encrypted archive"

        backend = t_classifier.detect_format(
            test_params.backend, 'e_'+test_params.archive, t_constants.OPERATION_LIST)
        if backend.can_encrypt():
            mocker.patch('rich.prompt.Prompt.ask', return_value=self.PASSWORD)
            test_utils.test_list('e_'+test_params.archive, [], ['-b',test_params.backend])

    def test_extract_one(self, test_params):
        "Extract one file from the archive"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_LIST)
        if backend.can_pack() or backend.mime[0] == t_constants.MIME_GZIP:
            file_name = self.LINK2
        else:
            file_name = Path(test_params.archive).stem
        test_utils.cleanup(file_name)
        test_utils.test_extract(test_params.archive, [file_name], ['-b',test_params.backend,'-a'])
        test_utils.assert_file_exists(file_name)

    def test_extract_prompt(self, test_params, mocker):
        "Extract one file from the archive with prompt"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_LIST)
        mocker.patch('rich.prompt.Prompt.ask', return_value='n')
        if backend.can_pack() or backend.mime[0] == t_constants.MIME_GZIP:
            file_name = self.LINK2
        else:
            file_name = Path(test_params.archive).stem
        test_utils.test_extract(test_params.archive, [file_name], ['-b',test_params.backend])
        test_utils.assert_file_exists(file_name)

    def test_extract_occurrence(self, test_params):
        "Extract one file from the archive with occurrence"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_EXTRACT)
        if backend.can_duplicate():
            test_utils.test_extract(
                test_params.archive, [self.FILE1], ['-b',test_params.backend,'-a','-o','1'])
            test_utils.assert_file_exists(self.FILE1)

    def test_extract_folder(self, test_params):
        "Extract one file from the archive with archive folder"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_LIST)
        if backend.can_pack() or backend.mime[0] == t_constants.MIME_GZIP:
            file_name = self.LINK2
        else:
            file_name = Path(test_params.archive).stem
        test_utils.cleanup(file_name)
        test_utils.test_extract(test_params.archive, [file_name], ['-b',test_params.backend,'-a','-f','yes'])
        test_utils.assert_file_exists(file_name, archive_folder=test_params.archive)

    def test_extract_all(self, test_params):
        "Extract all files from the archive"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_EXTRACT)

        base_name = Path(test_params.archive).stem
        test_utils.cleanup(base_name)
        test_utils.test_extract(test_params.archive, [], ['-b',test_params.backend,'-a'])
        if backend.can_pack():
            test_utils.assert_dir_exists(self.DIR, archive_folder=test_params.archive)
            test_utils.assert_file_exists(self.FILE1, archive_folder=test_params.archive)
            test_utils.assert_file_exists(os.path.join(self.PATH1, self.FILE1),
                archive_folder=test_params.archive)
            test_utils.assert_file_exists(os.path.join(self.PATH2, self.FILE1),
                archive_folder=test_params.archive)
            # https://github.com/p7zip-project/p7zip/issues/39
            if test_params.binary != '7z':
                test_utils.assert_link_exists(self.LINK1, archive_folder=test_params.archive)
            test_utils.assert_file_exists(self.LINK2, archive_folder=test_params.archive)
        elif backend.mime[0] == t_constants.MIME_GZIP:
            test_utils.assert_file_exists(self.LINK2)
        else:
            test_utils.assert_file_exists(base_name)

    def test_extract_all_no_folder(self, test_params):
        "Extract all files from the archive without archive folder"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_EXTRACT)

        base_name = Path(test_params.archive).stem
        test_utils.cleanup(self.DIR)
        test_utils.cleanup(self.FILE1)
        test_utils.cleanup(self.FILE2)
        test_utils.cleanup(self.LINK1)
        test_utils.cleanup(self.LINK2)
        test_utils.cleanup(self.PATH1)
        test_utils.cleanup(self.PATH2)
        test_utils.test_extract(test_params.archive, [], ['-b',test_params.backend,'-a','-f','no'])
        if backend.can_pack():
            test_utils.assert_dir_exists(self.DIR)
            test_utils.assert_file_exists(self.FILE1)
            test_utils.assert_file_exists(os.path.join(self.PATH1, self.FILE1))
            test_utils.assert_file_exists(os.path.join(self.PATH2, self.FILE1))
            # https://github.com/p7zip-project/p7zip/issues/39
            if test_params.binary != '7z':
                test_utils.assert_link_exists(self.LINK1)
            test_utils.assert_file_exists(self.LINK2)
        elif backend.mime[0] == t_constants.MIME_GZIP:
            test_utils.assert_file_exists(self.LINK2)
        else:
            test_utils.assert_file_exists(base_name)

    def test_extract_none(self, test_params):
        "Extract all files from the archive without overwriting"

        backend = t_classifier.detect_format(
            test_params.backend, test_params.archive, t_constants.OPERATION_EXTRACT)

        base_name = Path(test_params.archive).stem
        test_utils.test_extract(test_params.archive, [], ['-b',test_params.backend,'-n'])
        if backend.can_pack():
            test_utils.assert_dir_exists(self.DIR, archive_folder=test_params.archive)
            test_utils.assert_file_exists(self.FILE1, archive_folder=test_params.archive)
            test_utils.assert_file_exists(os.path.join(self.PATH1, self.FILE1),
                archive_folder=test_params.archive)
            test_utils.assert_file_exists(os.path.join(self.PATH2, self.FILE1),
                archive_folder=test_params.archive)
            # https://github.com/p7zip-project/p7zip/issues/39
            if test_params.binary != '7z':
                test_utils.assert_link_exists(self.LINK1, archive_folder=test_params.archive)
            test_utils.assert_file_exists(self.LINK2, archive_folder=test_params.archive)
        elif backend.mime[0] == t_constants.MIME_GZIP:
            test_utils.assert_file_exists(self.LINK2)
        else:
            test_utils.assert_file_exists(base_name)

    def test_extract_encrypted(self, test_params, mocker):
        "Lists an encrypted archive"

        test_utils.cleanup(self.DIR)
        backend = t_classifier.detect_format(
            test_params.backend, 'e_'+test_params.archive, t_constants.OPERATION_EXTRACT)
        if backend.can_encrypt():
            mocker.patch('rich.prompt.Prompt.ask', return_value=self.PASSWORD)
            test_utils.test_extract('e_'+test_params.archive, [], ['-b',test_params.backend,'-a'])
            test_utils.assert_dir_exists(self.DIR)

    def test_cleanup(self, test_params):
        "Not a real test, just the cleanup"

        base_name = Path(test_params.archive).stem
        test_utils.cleanup(base_name)
        test_utils.cleanup(test_params.archive)
        test_utils.cleanup('e_'+test_params.archive)
        test_utils.cleanup(self.DIR)
        test_utils.cleanup(self.FILE1)
        test_utils.cleanup(self.FILE2)
        test_utils.cleanup(self.LINK1)
        test_utils.cleanup(self.LINK2)
        test_utils.cleanup(self.PATH1)
        test_utils.cleanup(self.PATH2)
