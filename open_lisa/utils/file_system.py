import errno
import os
import sys

from open_lisa.exceptions.invalid_path_exception import InvalidPathException

USER_FILES_FOLDER = "sandbox"
# Sadly, Python fails to provide the following magic number for us
ERROR_INVALID_NAME = 123


def get_file_path(file_name):
    while file_name.startswith('/') or file_name.startswith('\\') or file_name.startswith('.'):
        file_name = file_name[1:]

    file_path = os.path.join(get_sandbox_dir(), file_name)

    if not is_path_exists_or_creatable(file_path):
        raise InvalidPathException(file_path)

    return file_path


def get_sandbox_dir():
    abs_path_this_file = os.path.dirname(os.path.abspath(__file__))
    sandbox_dir = os.path.join(abs_path_this_file, os.pardir, os.pardir, USER_FILES_FOLDER)

    return sandbox_dir


# Reference: https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta

def is_pathname_valid(pathname: str) -> bool:
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


def is_path_creatable(pathname: str) -> bool:
    """
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    """
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        return is_pathname_valid(pathname) and (
                os.path.exists(pathname) or is_path_creatable(pathname))
    except OSError:
        return False
