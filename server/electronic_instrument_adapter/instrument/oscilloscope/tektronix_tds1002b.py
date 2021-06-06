from ..instrument import Oscilloscope


class Tektronix_TDS1002B(Oscilloscope):
    def __init__(self, id, brand, model):
        self._available_timebase_modes = ["YT", "XY"]
        self._available_channels = ["CH1", "CH2"]

        super(Tektronix_TDS1002B, self).__init__(id, brand, model)

    def set_initial_configuration(self):
        self.configuration.volts_scale = 0.5
        self.configuration.time_scale = 0.000200

        self.stop_acquisitions()
        self.clear_status()

        self.set_channel_probe(1, 1)
        self.set_channel_probe(2, 1)

        self.set_volts_scale(1, self.configuration.volts_scale)
        self.set_volts_scale(2, self.configuration.volts_scale)

        self.set_timebase_mode("YT")

        self.set_timebase_x_channel("CH1")
        self.set_timebase_y_channel("CH2")

        self.set_timebase_scale(self.configuration.time_scale)

        self.get_identification()

    def clear_status(self):
        self.device.write("*CLS")

    def reset_settings(self):
        self.device.write("*RST")

    def get_identification(self):
        return self.device.query("*IDN?")

    def stop_acquisitions(self):
        self.device.write("ACQuire:STATE STOP")

    def get_is_in_acquisitions_state(self):
        return self.device.query("*OPC?") == 1

    def set_volts_scale(self, channel, volts_scale):
        self.device.write('CH' + str(channel) + ':VOLts ' + str(volts_scale))

    def set_timebase_scale(self, seconds):
        self.device.write('HORizontal:MAIn:SCAle ' + str(seconds))

    def set_channel_probe(self, channel, probe):
        self.device.write('CH' + str(channel) + ':PRObe ' + str(probe))

    def set_timebase_mode(self, mode):
        if self._available_timebase_modes.__contains__(str(mode)):
            self.device.write('DISplay:FORMat ' + str(mode))

    def set_timebase_x_channel(self, channel):
        if self._available_channels.__contains__(str(channel)):
            self.device.write("MEASUrement:IMMed:SOUrce1 " + str(channel))

    def set_timebase_y_channel(self, channel):
        if self._available_channels.__contains__(str(channel)):
            self.device.write("MEASUrement:IMMed:SOUrce2 " + str(channel))

