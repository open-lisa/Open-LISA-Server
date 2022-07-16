from .base_exception import OpenLISAException

DEFAULT_MESSAGE = "instrument update error"


class InstrumentUpdateError(OpenLISAException):
    """
    Raised when instrument update fails
    """

    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)
