from .base_exception import ElectronicInstrumentAdapterException

DEFAULT_MESSAGE="instrument not found"

class InstrumentNotFoundError(ElectronicInstrumentAdapterException):
    """
    Raised when instrument does not exist
    """
    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)