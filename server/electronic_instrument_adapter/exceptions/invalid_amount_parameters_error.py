from .base_exception import ElectronicInstrumentAdapterException

class InvalidAmountParametersError(ElectronicInstrumentAdapterException):
    def __init__(self, sent, required):
        self.parameters_amount_sent = sent
        self.parameters_amount_required = required
        message = "{} parameters has been sent, but {} are required.".format(sent, required)
        super().__init__(message)
