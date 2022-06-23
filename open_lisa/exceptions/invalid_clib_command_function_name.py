from .base_exception import OpenLISAException


class InvalidCLibCommandFunctionNameError(OpenLISAException):
    """
    Raised when a CLibCommand is initialized with an unexisting function name in the lib provided
    """

    def __init__(self, function_name, lib_name):
        message = "Function name '{}' is invalid, could not be found in lib '{}'".format(
            function_name, lib_name)
        super().__init__(message)
