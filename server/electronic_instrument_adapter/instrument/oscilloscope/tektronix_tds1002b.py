from ..instrument import Oscilloscope


class Tektronix_TDS1002B(Oscilloscope):
    def __init__(self, id, brand, model):
        super(Tektronix_TDS1002B, self).__init__(id, brand, model)

    def set_volts_scale(self, channel, volts_scale):
        self.device.write('CH' + str(channel) + ':VOLts ' + str(volts_scale))

    def set_time_scale(self, seconds):
        self.device.write('HORizontal:MAIn:SCAle ' + str(seconds))
