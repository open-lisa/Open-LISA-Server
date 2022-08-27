from .base_exception import OpenLISAException
import os


class ForbiddenPathDeletionException(OpenLISAException):
    """
    Raised when trying to delete an forbidden directory in server file system
    """

    def __init__(self, protected_directories, given_directory):
        message = "cannot delete the given path {}, it belongs to forbidden deletion path list: {}."\
            .format(protected_directories, given_directory)
        super().__init__(message)
