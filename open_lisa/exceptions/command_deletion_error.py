from .base_exception import OpenLISAException

DEFAULT_MESSAGE = "command delete error"


class CommandDeletionError(OpenLISAException):
    """
    Raised when instrument delete fails
    """

    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)
