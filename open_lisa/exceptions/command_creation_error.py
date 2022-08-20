from .base_exception import OpenLISAException

DEFAULT_MESSAGE = "command creation error"


class CommandCreationError(OpenLISAException):
    """
    Raised when command creation fails
    """

    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)
