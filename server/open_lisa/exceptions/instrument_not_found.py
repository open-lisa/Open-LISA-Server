from .base_exception import OpenLISAException

DEFAULT_MESSAGE="instrument not found"

class InstrumentNotFoundError(OpenLISAException):
    """
    Raised when instrument does not exist
    """
    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)