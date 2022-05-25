from .base_exception import OpenLISAException

DEFAULT_MESSAGE="command not found"

class CommandNotFoundError(OpenLISAException):
    """
    Raised when command does not exist
    """
    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)