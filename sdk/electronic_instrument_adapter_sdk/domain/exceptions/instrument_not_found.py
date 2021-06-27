from .sdk_exception import ElectronicInstrumentAdapterException

DEFAULT_MESSAGE = "instrument not exists"


class InstrumentNotFoundException(ElectronicInstrumentAdapterException):
    """
    Raised when the requested instrument not exists
  """

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message
        super().__init__(self.message)
