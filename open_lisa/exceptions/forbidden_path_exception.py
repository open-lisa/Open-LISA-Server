from .base_exception import OpenLISAException
import os


class ForbiddenPathException(OpenLISAException):
    """
    Raised when trying to manipulate an invalid path in file system
    """

    def __init__(self, permitted_paths, provided_path):
        message = "the given path {} is forbidden, the path must start with: {}. i.e: '{}" \
                  "/measures.csv'".format(provided_path, permitted_paths, permitted_paths[0])
        super().__init__(message)
