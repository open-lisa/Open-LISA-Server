from .base_exception import OpenLISAException


class InvalidCommandParameterValueError(OpenLISAException):
    """
    Raised when a command parameter value provided does not match with the expected type
    """

    def __init__(self, value_provided, expected_type):
        message = "parameter value {} is not valid for a command parameter of type {}".format(
            value_provided, expected_type)
        super().__init__(message)
