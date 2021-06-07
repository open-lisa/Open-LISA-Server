import pyvisa
from server.electronic_instrument_adapter.constants.instrument import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE


def InstrumentFactory(type, id):
    if type == "oscilloscope":
        from .oscilloscope.factory import OscilloscopeFactory
        return OscilloscopeFactory(id)


class Instrument:
    def __init__(self, id, brand, model):
        self.id = id
        self.brand = brand
        self.model = model
        self.device = None
        self.status = INSTRUMENT_STATUS_UNAVAILABLE

        self.set_status()

    def set_status(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        if resources.__contains__(self.id):
            self.device = rm.open_resource(self.id)
            self.status = INSTRUMENT_STATUS_AVAILABLE
        else:
            self.status = INSTRUMENT_STATUS_UNAVAILABLE

