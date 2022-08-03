from functools import reduce
import logging
import os
import sys
import errno
from pathlib import Path

from open_lisa.exceptions.forbidden_path_exception import ForbiddenPathException
from open_lisa.exceptions.invalid_path_exception import InvalidPathException

# Sadly, Python fails to provide the following magic number for us
ERROR_INVALID_NAME = 123

ROOT_FOLDER_SANDBOX = 'sandbox'
ROOT_FOLDER_CLIBS = 'clibs'
ROOT_FOLDER_DATABASE = 'database'
VALID_ROOT_FOLDERS = [ROOT_FOLDER_SANDBOX, ROOT_FOLDER_CLIBS, ROOT_FOLDER_DATABASE]


class FileManager:
    def __init__(self, sandbox_folder_path=os.getenv("USER_FILES_FOLDER"), clibs_folder_path=os.getenv("CLIBS_FOLDER"),
                 database_folder_path=os.getenv("DATABASE_FOLDER")) -> None:
        # NOTE: this class could have CRUDs logic for OpenLISA files (pos process, clibs, etc)
        project_root_path = os.getcwd()
        self._folders_path = {
            ROOT_FOLDER_SANDBOX: os.path.join(project_root_path, sandbox_folder_path),
            ROOT_FOLDER_CLIBS: os.path.join(project_root_path, clibs_folder_path),
            ROOT_FOLDER_DATABASE: os.path.join(project_root_path, database_folder_path)
        }

    def list_directory_recursively(self, directory):
        # Src of as_dict calculation https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
        as_dict = {}
        rootdir = directory.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, _, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = reduce(dict.get, folders[:-1], as_dict)
            parent[folders[-1]] = subdir

        # transform as_dict to list (best for frontend rendering)
        base_key = list(as_dict.keys())[0]
        directory_as_list = self.__transform_directory_represented_as_dict_to_list(
            as_dict[base_key])
        return directory_as_list

    def delete_file(self, file_path):
        file_path = self.__get_file_path(file_path)
        file_exists = os.path.exists(file_path)
        if file_exists:
            logging.info("[OpenLISA][FileManager][delete_file] Deleting file in {}".format(file_path))
            os.remove(file_path)

    def write_file(self, file_path, file_mode, data):
        file_path = self.__get_file_path(file_path)
        with open(file_path, file_mode) as file:
            file.write(data)

    def get_file_data(self, file_path, file_mode):
        file_path = self.__get_file_path(file_path)
        with open(file_path, file_mode) as file:
            return file.read()

    def __get_file_path(self, user_file_path):
        path_parts = Path(user_file_path).parts
        root_folder = path_parts[0]

        if root_folder not in VALID_ROOT_FOLDERS:
            raise ForbiddenPathException(VALID_ROOT_FOLDERS, user_file_path)

        user_file_path_without_root_folder = path_parts[1:]
        file_path = os.path.join(self._folders_path[root_folder], *user_file_path_without_root_folder)

        if not self.__is_path_exists_or_creatable(file_path):
            raise InvalidPathException(file_path)

        return file_path

    # Reference: https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta

    def __is_path_creatable(self, pathname: str) -> bool:
        """
        `True` if the current user has sufficient permissions to create the passed
        pathname; `False` otherwise.
        """
        dirname = os.path.dirname(pathname) or os.getcwd()
        return os.access(dirname, os.W_OK)

    def __is_pathname_valid(self, pathname: str) -> bool:
        """
        `True` if the passed pathname is a valid pathname for the current OS;
        `False` otherwise.
        """
        try:
            if not isinstance(pathname, str) or not pathname:
                return False

            _, pathname = os.path.splitdrive(pathname)

            root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                if sys.platform == 'win32' else os.path.sep
            assert os.path.isdir(root_dirname)  # ...Murphy and her ironclad Law

            root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

            for pathname_part in pathname.split(os.path.sep):
                try:
                    os.lstat(root_dirname + pathname_part)

                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == ERROR_INVALID_NAME:
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False
        except TypeError as exc:
            return False
        else:
            return True

    def __is_path_exists_or_creatable(self, pathname: str) -> bool:
        """
        `True` if the passed pathname is a valid pathname for the current OS _and_
        either currently exists or is hypothetically creatable; `False` otherwise.

        This function is guaranteed to _never_ raise exceptions.
        """
        try:
            return self.__is_pathname_valid(pathname) and (
                    os.path.exists(pathname) or self.__is_path_creatable(pathname))
        except OSError:
            return False

    def __transform_directory_represented_as_dict_to_list(self, directory_dict={}):
        result = []
        keys = list(directory_dict.keys())
        keys_that_are_directories = sorted(
            filter(lambda k: type(directory_dict[k]) == dict, keys))
        keys_that_are_files = sorted(
            filter(lambda k: directory_dict[k] == None, keys))
        keys = keys_that_are_directories + keys_that_are_files
        for k in keys:
            if type(directory_dict[k]) == dict:  # it is a directory
                children = self.__transform_directory_represented_as_dict_to_list(
                    directory_dict[k])
                result.append({
                    "name": k,
                    "type": "directory",
                    "children": children
                })
            elif directory_dict[k] == None:  # it is a file
                result.append({
                    "name": k,
                    "type": "file",
                })
        return result
