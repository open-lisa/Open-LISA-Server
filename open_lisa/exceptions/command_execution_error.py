from .base_exception import OpenLISAException


class CommandExecutionError(OpenLISAException):
    """
    Raised when command execution fails
    """

    def __init__(self, command, additional_info):
        message = "command {} execution failed, additional info: {}".format(
            command, additional_info)
        super().__init__(message)
