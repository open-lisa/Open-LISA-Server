from ..instrument import Oscilloscope


class Tektronix_TDS1002B(Oscilloscope):
    def __init__(self, id, brand, model):
        super(Tektronix_TDS1002B, self).__init__(id, brand, model)

    def set_volts_scale(self, channel, volts_scale):
        self.device.write("CH{}:VOLts {}", channel, volts_scale)