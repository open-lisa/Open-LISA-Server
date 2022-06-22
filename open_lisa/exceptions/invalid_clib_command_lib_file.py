from .base_exception import OpenLISAException


class InvalidCLibCommandLibFileError(OpenLISAException):
    """
    Raised when a CLibCommand is initialized with a C lib that could not be opened
    """

    def __init__(self, lib_name):
        message = "C lib '{}' could not be initialized".format(lib_name)
        super().__init__(message)
