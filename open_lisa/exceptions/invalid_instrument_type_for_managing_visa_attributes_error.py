from .base_exception import OpenLISAException

DEFAULT_MESSAGE = "invalid instrument type for managing VISA attributes"


class InvalidInstrumentTypeForManagingVisaAttributes(OpenLISAException):
    """
    Raised when setting or getting VISA attributes for a type of instrument that does not support it
    """

    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)
