import json
import logging
from ..instrument import Oscilloscope


class Tektronix_TDS1002B(Oscilloscope):
    def __init__(self, id, brand, model):
        with open('electronic_instrument_adapter/instrument/oscilloscope/configs/oscilloscope_tektronix_tds1002b.json') as file:
            cfg = json.load(file)
            self._available_acquisition_modes = [mode["value"] for mode in cfg["acquisition"]["mode"]]
            self._available_average_acquisition_mode_samples_amount =[amount["value"] for amount in cfg["acquisition"]["average_mode_samples_amount"]]
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

        self.set_acquisition_mode("AVErage")
        self.set_average_acquisition_mode_samples_amount("16")
        self.set_acquisition_memory_depth("64000")

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


    """
        BEGIN ACQUISITION PRIMITIVES
        Acquisition commands affect the acquisition of waveforms. These commands control mode, averaging, and single-waveform acquisition
    """
    def set_acquisition_mode(self, mode):
        """
        Sets the oscilloscope acquisition mode. This affects all live waveforms
        and is equivalent to setting the Mode option in the Acquire menu.

        Waveforms are the displayed data point values taken from acquisition intervals.
        Each acquisition interval represents a time duration that is determined by the horizontal scale (time per division).

        The oscilloscope sampling system can operate at a rate greater than that indicated by the horizontal scale.
        Therefore, an acquisition interval can include more than one sample.

        The acquisition mode, which you set using this ACQuire:MODe command, determines
        how the final value of the acquisition interval is generated from the many data samples.
        """
        mode = str(mode)
        if mode in self._available_acquisition_modes:
            self.device.write("ACQuire:MODe {}".format(mode))
        else:
            logging.warning("Acquisition mode {} is not supported".format(mode))

    def get_acquisition_mode(self):
        """
            Queries and returns the oscilloscope acquisition mode
        """
        return self.device.write("ACQuire:MODe?")

    def set_average_acquisition_mode_samples_amount(self, amount):
        """
            Sets the number of oscilloscope waveform acquisitions that make up an averaged waveform.
            This command is equivalent to setting the Averages option in the Acquire menu.
        """

        # Check is in 'AVErage' mode
        mode = self.get_acquisition_mode()
        if mode.lower() != "AVErage".lower():
            logging.warning("set_average_acquisition_mode_samples_amount should be called on 'average' acquisition mode but current is '{}'".format(mode))
            return

        if amount in self._available_average_acquisition_mode_samples_amount:
            self.device.write("ACQuire:NUMAVg {}".format(amount))
        else:
            logging.warning("Samples amount {} is not supported".format(amount))

    def set_acquisition_memory_depth(self, depth):
        logging.warning("set_acquisition_memory_depth primmitive is not supported")

