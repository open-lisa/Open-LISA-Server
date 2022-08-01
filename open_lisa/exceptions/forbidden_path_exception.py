from .base_exception import OpenLISAException
import os


class ForbiddenPathException(OpenLISAException):
    """
    Raised when trying to manipulate an invalid path in file system
    """

    def __init__(self):
        message = "the given path is forbidden, only the following paths are permitted: {}, {} and {}. i.e: '{}" \
                  "/measures.csv'".format(os.getenv("USER_FILES_FOLDER"), os.getenv("CLIBS_FOLDER"),
                                          os.getenv("DATABASE_FOLDER"), os.getenv("USER_FILES_FOLDER"))
        super().__init__(message)
