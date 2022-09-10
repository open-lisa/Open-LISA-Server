import random
import os
from open_lisa.domain.filesystem.filemanager import VALID_ROOT_FOLDERS, FileManager

SANDBOX_FOLDER = "data_test/sandbox"
CLIBS_FOLDER = "data_test/clibs"
DATABASE_FOLDER = "data_test/database"

CURR_TEST_FILE_BYTES = None
with open(__file__, "rb") as f:
    CURR_TEST_FILE_BYTES = f.read()


def test_list_directory_mockdir_to_be_tested_for_list_should_return_a_list_representing_the_directory():
    # NOTE: expected_directory should have the same order that is returned, otherwise the test would fail
    # the order is: first directories (alphabetically) and then files (alphabetically)
    empty_directory_name = "empty"
    expected_directory = [
        {
            "name": "1",
            "type": "directory",
            "children": [
                {
                    "name": "1_1",
                    "type": "directory",
                    "children": [
                        {
                            "name": "another_file.txt",
                            "type": "file"
                        },
                        {
                            "name": "file_1_1.py",
                            "type": "file"
                        }
                    ]
                },
                {
                    "name": "file_1.txt",
                    "type": "file"
                },
            ]
        },
        {
            "name": "2",
            "type": "directory",
            "children": [
                {
                    "name": "file_2.js",
                    "type": "file"
                },
            ]
        },
        {
            "name": empty_directory_name,
            "type": "directory",
            "children": []
        }
    ]

    fm = FileManager()

    curr_file_path = os.path.dirname(__file__)
    mock_directory = os.path.join(
        curr_file_path, "mockdir_to_be_tested_for_list")

    # create empty directory if needed
    empty_directory = os.path.join(
        curr_file_path, "mockdir_to_be_tested_for_list", empty_directory_name)
    if not os.path.isdir(empty_directory):
        os.makedirs(empty_directory)
    result = fm.list_directory_recursively(mock_directory)
    assert result == expected_directory


def test_write_get_and_delete_file():
    fm = FileManager(
        sandbox_folder_path=SANDBOX_FOLDER,
        clibs_folder_path=CLIBS_FOLDER,
        database_folder_path=DATABASE_FOLDER
    )

    root_folder = random.choice(VALID_ROOT_FOLDERS)
    remote_file_name = "remote_test_filemanager.py"
    remote_file_path = root_folder + "/" + remote_file_name
    absolute_path_for_remote_file = fm._folders_path[root_folder] + \
        "/" + remote_file_name
    fm.write_file(remote_file_path, "wb", CURR_TEST_FILE_BYTES)

    assert os.path.exists(absolute_path_for_remote_file)

    file_bytes = fm.get_file_data(remote_file_path, "rb")

    assert file_bytes == CURR_TEST_FILE_BYTES

    fm.delete_file(remote_file_path)

    assert not os.path.exists(absolute_path_for_remote_file)
