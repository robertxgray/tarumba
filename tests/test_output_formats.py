# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's main function tests"

import tarumba.constants as t_constants
from tests import utils as test_utils

TEST = "output_formats"
TEST_PARAMS = test_utils.TestParams(t_constants.BACKEND_TAR, test_utils.GTAR, "test_gtar.tar")


class TestMain:
    "Main function tests"

    def test_init_files(self):
        "Create the test files"

        test_utils.test_init_files(TEST, TEST_PARAMS)

    def test_add_new(self):
        "Create the archive"

        test_utils.test_add(TEST, TEST_PARAMS, [test_utils.DIR, test_utils.FILE_ABS], ["-b", TEST_PARAMS.backend])
        test_utils.assert_file_exists(TEST, TEST_PARAMS.archive)

    def test_list_table(self):
        "List files in table format"

        test_utils.test_list(TEST, TEST_PARAMS, [], ["-b", TEST_PARAMS.backend, "-o", "table"])

    def test_list_raw(self):
        "List files in raw format"

        test_utils.test_list(TEST, TEST_PARAMS, [], ["-b", TEST_PARAMS.backend, "-o", "raw"])

    def test_list_csv(self):
        "List files in csv format"

        test_utils.test_list(TEST, TEST_PARAMS, [], ["-b", TEST_PARAMS.backend, "-o", "csv"])

    def test_list_json(self):
        "List files in json format"

        test_utils.test_list(TEST, TEST_PARAMS, [], ["-b", TEST_PARAMS.backend, "-o", "json"])

    def test_cleanup(self):
        "Test files cleanup"

        test_utils.test_cleanup(TEST, TEST_PARAMS)
