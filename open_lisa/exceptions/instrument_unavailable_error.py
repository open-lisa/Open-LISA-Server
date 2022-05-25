from .base_exception import OpenLISAException

DEFAULT_MESSAGE="instrument not available for sending command"

class InstrumentUnavailableError(OpenLISAException):
    """
    Raised when send command is called for a instrument not available
    """
    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)