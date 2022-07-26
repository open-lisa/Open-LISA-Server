import os
from open_lisa.domain.filesystem.filemanager import FileManager


def test_list_directory_mockdir_to_be_tested_for_list_should_return_a_list_representing_the_directory():
    # NOTE: expected_directory should have the same order that is returned, otherwise the test would fail
    # the order is: first directories (alphabetically) and then files (alphabetically)
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
                    "name": "2_3",
                    "type": "directory",
                    "children": []
                },
                {
                    "name": "file_2.js",
                    "type": "file"
                },
            ]
        },
        {
            "name": "3",
            "type": "directory",
            "children": []
        },
    ]

    fm = FileManager()

    curr_file_path = os.path.dirname(__file__)
    mock_directory = os.path.join(
        curr_file_path, "mockdir_to_be_tested_for_list")
    result = fm.list_directory_recursively(mock_directory)
    assert result == expected_directory
