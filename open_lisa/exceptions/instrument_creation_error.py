from .base_exception import OpenLISAException

DEFAULT_MESSAGE = "instrument creation error"


class InstrumentCreationError(OpenLISAException):
    """
    Raised when instrument creation fails
    """

    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)
